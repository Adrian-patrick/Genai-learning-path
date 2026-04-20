from datetime import datetime, timezone
from threading import Lock

from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
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

# Changed: in-memory graph status store used by frontend polling to show current step.
GRAPH_STATUS = {
    "current_step": "idle",
    "timeline": [],
    "updated_at": None,
}
GRAPH_STATUS_LOCK = Lock()


@app.get("/", response_class=HTMLResponse)
def frontend() -> str:
        # Changed: simple frontend UI so users can submit a query and see API response in browser.
        return """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Trip Planner Assistant</title>
    <style>
        :root {
            --bg: #f7f4ee;
            --panel: #fffdf9;
            --ink: #1e2a2f;
            --muted: #5b6b72;
            --accent: #0f766e;
            --accent-soft: #d6f3ef;
            --border: #d9d4c7;
        }
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            color: var(--ink);
            background: radial-gradient(circle at top right, #e8f6f3 0%, var(--bg) 45%);
            min-height: 100vh;
            display: grid;
            place-items: center;
            padding: 24px;
        }
        .card {
            width: min(900px, 100%);
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
        }
        h1 { margin: 0 0 8px; font-size: 1.5rem; }
        p { margin: 0 0 16px; color: var(--muted); }
        textarea {
            width: 100%;
            min-height: 120px;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 12px;
            font: inherit;
            resize: vertical;
            background: #fff;
        }
        .actions {
            margin-top: 12px;
            display: flex;
            gap: 10px;
            align-items: center;
        }
        button {
            border: 0;
            border-radius: 10px;
            padding: 10px 14px;
            background: var(--accent);
            color: white;
            font-weight: 600;
            cursor: pointer;
        }
        button:disabled { opacity: 0.6; cursor: not-allowed; }
        .status {
            color: var(--muted);
            font-size: 0.9rem;
        }
        .result {
            margin-top: 16px;
            border: 1px solid var(--border);
            background: var(--accent-soft);
            border-radius: 12px;
            padding: 14px;
            white-space: pre-wrap;
            line-height: 1.45;
            min-height: 80px;
        }
    </style>
</head>
<body>
    <main class="card">
        <h1>Trip Planner Assistant</h1>
        <p>Ask your travel question and the multi-node workflow will generate a plan.</p>

        <textarea id="query" placeholder="Example: Plan a trip to Paris for 5 days with budget options"></textarea>

        <div class="actions">
            <button id="send">Generate Plan</button>
            <button id="history" type="button">Load History</button>
            <span class="status" id="status">Ready</span>
        </div>

        <section class="result" id="result">Response will appear here.</section>
        <section class="result" id="graphStep" style="margin-top:12px;">Graph step status will appear here.</section>
        <section class="result" id="historyBox" style="margin-top:12px;">History will appear here.</section>
    </main>

    <script>
        const queryEl = document.getElementById('query');
        const sendBtn = document.getElementById('send');
        const historyBtn = document.getElementById('history');
        const statusEl = document.getElementById('status');
        const resultEl = document.getElementById('result');
        const graphStepEl = document.getElementById('graphStep');
        const historyEl = document.getElementById('historyBox');
        let stepPoller = null;

        async function refreshGraphStatus() {
            const response = await fetch('/graph-status');
            if (!response.ok) {
                return;
            }
            const data = await response.json();
            const timelineText = (data.timeline || []).join('\\n');
            graphStepEl.textContent = `Current: ${data.current_step || 'unknown'}\n\nTimeline:\n${timelineText || 'No steps yet.'}`;
        }

        function startGraphPolling() {
            if (stepPoller) {
                clearInterval(stepPoller);
            }
            stepPoller = setInterval(() => {
                refreshGraphStatus().catch(() => {});
            }, 700);
        }

        function stopGraphPolling() {
            if (stepPoller) {
                clearInterval(stepPoller);
                stepPoller = null;
            }
        }

        async function submitQuery() {
            const query = queryEl.value.trim();
            if (!query) {
                statusEl.textContent = 'Please enter a query.';
                return;
            }

            sendBtn.disabled = true;
            statusEl.textContent = 'Running...';
            resultEl.textContent = 'Working on your request...';
            graphStepEl.textContent = 'Initializing graph status...';
            startGraphPolling();

            try {
                const response = await fetch('/query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(errorText || 'Request failed');
                }

                const data = await response.json();
                resultEl.textContent = data.answer;
                await refreshGraphStatus();
                statusEl.textContent = 'Done';
            } catch (err) {
                resultEl.textContent = 'Error: ' + err.message;
                statusEl.textContent = 'Failed';
            } finally {
                stopGraphPolling();
                sendBtn.disabled = false;
            }
        }

        async function loadHistory() {
            historyBtn.disabled = true;
            statusEl.textContent = 'Loading history...';

            try {
                const response = await fetch('/history?limit=10');
                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(errorText || 'Failed to load history');
                }

                const rows = await response.json();
                if (!rows.length) {
                    historyEl.textContent = 'No history found yet.';
                    statusEl.textContent = 'Done';
                    return;
                }

                const text = rows
                    .map((row, idx) => `${idx + 1}. Created: ${row.created_at}\nQuery: ${row.query}\nAnswer: ${row.answer}`)
                    .join('\\n\\n');
                historyEl.textContent = text;
                statusEl.textContent = 'Done';
            } catch (err) {
                historyEl.textContent = 'Error: ' + err.message;
                statusEl.textContent = 'Failed';
            } finally {
                historyBtn.disabled = false;
            }
        }

        sendBtn.addEventListener('click', submitQuery);
        historyBtn.addEventListener('click', loadHistory);
    </script>
</body>
</html>
        """

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





