from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from agents import agent
from database import Base, engine, get_db
from models import PredictionLog, PredictionLogOut, RequestModel, ResponseModel

Base.metadata.create_all(bind=engine)

api = FastAPI()

@api.get("/health")
def get_health():
    return {"status": "OK"}

@api.post("/predict", response_model=ResponseModel)
async def prediction(info: RequestModel, db: Session = Depends(get_db)):
    response = await agent.run(info.email_text)

    db_row = PredictionLog(
        email_text=info.email_text,
        category=response.output.category.value,
        reason=response.output.reason,
    )
    db.add(db_row)
    db.commit()

    return response.output


@api.get("/predictions", response_model=list[PredictionLogOut])
def get_all_predictions(db: Session = Depends(get_db)):
    # Step 1: start a query on the prediction_logs table.
    prediction_query = db.query(PredictionLog)

    # Step 2: sort by newest records first.
    ordered_query = prediction_query.order_by(PredictionLog.created_at.desc())

    # Step 3: execute the query and load all rows.
    predictions = ordered_query.all()

    # Step 4: return rows; FastAPI/Pydantic handles response serialization.
    return predictions
