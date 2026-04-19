from fastapi import FastAPI
from models import *
from agents import agent
import asyncio 

api = FastAPI()

@api.get('/health')
def get_health():
    return {"status": "OK"}

@api.post('/predict',response_model=ResponseModel)
async def prediction(info:RequestModel):

    print("Predicting...")
    response = await agent.run(info.email_text)
    print("Predicted")

    return response.output
