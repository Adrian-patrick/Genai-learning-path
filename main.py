from datetime import datetime, timezone
from pathlib import Path
from threading import Lock

from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from agents import PlannerNode, State, graph
from database import Base, engine, get_db
from models import RequestModel, ResponseModel, Conversation

# Changed: create ORM tables at startup import so inserts don't fail on missing table.
Base.metadata.create_all(bind=engine)

# Changed: add a tiny migration step so existing databases also get created_at without manual SQL.
inspector = inspect(engine)
existing_columns = {col["name"] for col in inspector.get_columns("conversations")}
if "created_at" not in existing_columns:
    with engine.begin() as conn:
        conn.execute(
            text(
                "ALTER TABLE conversations "
                "ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP"
            )
        )

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

# Changed: in-memory graph status store used by frontend polling to show current step.
GRAPH_STATUS = {
    "current_step": "idle",
    "timeline": [],
    "updated_at": None,
}
GRAPH_STATUS_LOCK = Lock()

@app.get("/")
def frontend() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/health")
def get_health():
    return {"status": "ok"}

@app.post("/query")
async def handle_query(request: RequestModel, db: Session = Depends(get_db)):
    def set_graph_step(step: str) -> None:
        # Changed: record live graph progress so frontend can show exact current step.
        with GRAPH_STATUS_LOCK:
            GRAPH_STATUS["current_step"] = step
            GRAPH_STATUS["updated_at"] = datetime.now(timezone.utc).isoformat()
            GRAPH_STATUS["timeline"].append(
                f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] {step}"
            )

    with GRAPH_STATUS_LOCK:
        GRAPH_STATUS["current_step"] = "request: started"
        GRAPH_STATUS["updated_at"] = datetime.now(timezone.utc).isoformat()
        GRAPH_STATUS["timeline"] = [
            f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] request: started"
        ]

    # Changed: Graph.run requires a start node instance, not just raw state.
    run_result = await graph.run(
        PlannerNode(state=State(query=request.query, progress_hook=set_graph_step))
    )

    # Changed: GraphRunResult stores final node End payload in .output, not final_output.output.
    answer = run_result.output

    db.add(Conversation(query=request.query, answer=answer))
    db.commit()

    set_graph_step("request: completed")

    return ResponseModel(answer=answer)


@app.get("/history")
def get_history(limit: int = 10, db: Session = Depends(get_db)):
    # Changed: expose recent conversations so frontend can display persisted history.
    rows = db.query(Conversation).order_by(Conversation.id.desc()).limit(limit).all()
    return [
        {
            "id": row.id,
            "query": row.query,
            "answer": row.answer,
            "created_at": row.created_at.isoformat() if row.created_at else None,
        }
        for row in rows
    ]


@app.get("/graph-status")
def graph_status():
    # Changed: lightweight endpoint used by frontend polling for live step visibility.
    with GRAPH_STATUS_LOCK:
        return {
            "current_step": GRAPH_STATUS["current_step"],
            "timeline": list(GRAPH_STATUS["timeline"]),
            "updated_at": GRAPH_STATUS["updated_at"],
        }





