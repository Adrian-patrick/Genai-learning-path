from fastapi import FastAPI
import uvicorn

from api.expense_routes import router
from database.database import create_tables
from utils.seed_data import seed_dummy_expenses

create_tables()
seed_dummy_expenses()

app = FastAPI()

app.include_router(router)


@app.get("/")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8020, reload=False)
