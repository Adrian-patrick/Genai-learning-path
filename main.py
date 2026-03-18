from fastapi import FastAPI,Path
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

api = FastAPI()
model_information = {1: {"model name" :"gpt4","type": "Multimodal Foundation Model", "Context Window": "128k tokens"},2: {"model name":"claude3.5","type": "Large Language Model", "Context Window": "200k tokens"}}
class Modelname(str,Enum):
    gpt4 = "gpt4"
    claude35 = "claude3.5"


class Inputmodel(BaseModel):
    model: str = Field(..., description="model name", examples=["gpt4"])
    text: str = Field(..., description="content to infer", examples=["can you explain what is a supercar?"])
    temperature: Optional[float] = Field(default=0.7, description="higher values make the output more random")

class Outputmodel(Inputmodel):
    status : str = "OK"
    response: Optional[str] = Field(..., description="generated response")
    

@api.get('/health')
def get_health():
    return {"status" : "OK"}

@api.get('/model')
def model_get_id(model_id: int = None):
    return model_information.get(model_id,{"status":"invalid id provided "})



from fastapi import HTTPException

@api.post('/predict', response_model=Outputmodel)
def model_inference(info: Inputmodel):
    # flag=0 will make this return None
    response = simulated_api_call(info.text, flag=1)
    
    if response is None:
        # Stop the code here and return a real 400 or 500 error
        raise HTTPException(status_code=500, detail="Model failed to generate a response")

    return {
        "status": "success",
        "model": info.model,
        "text": info.text,
        "response": response, # Key must match Outputmodel field name
        "temperature": info.temperature
    }


def simulated_api_call(content : str,flag=0):
    if flag:
        return "simulated response"
    return None

