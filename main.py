from fastapi import FastAPI,Path,HTTPException
from pydantic import BaseModel, Field,field_validator
from typing import Optional
from enum import Enum

api = FastAPI()
model_information = {1: {"model name" :"gpt4","type": "Multimodal Foundation Model", "Context Window": "128k tokens"},2: {"model name":"claude3.5","type": "Large Language Model", "Context Window": "200k tokens"}}
class Modelname(str,Enum):
    gpt4 = "gpt4"
    claude35 = "claude3.5"

class Statusname(str,Enum):
    success = "success"
    error = "error"

class Requestmodel(BaseModel):
    model: Modelname = Field(..., description="model name", examples=["gpt4"])
    text: str = Field(...,min_length=10,max_length=1000, description="content to infer", examples=["can you explain what is a supercar?"])
    temperature: Optional[float] = Field(default=0.7,ge=0,le=1 ,description="higher values make the output more random")
    max_tokens : Optional[int] = Field(default = 100,ge=1,le=500,description="max tokens")

    @field_validator('text')
    def validate_text(cls,value):
        if value.strip() == "":
            raise ValueError("text cannot be empty")
        return value

class Data(BaseModel):
    response : str
    model_used : str
    tokens_used : int

class Metadata(BaseModel):
    temperature : float
    max_tokens : int

class Responsemodel(BaseModel):
    status : Statusname = Field(default= Statusname.success, description="status")
    data: Data = Field(..., description="data from the model")
    metadata : Metadata = Field(..., description="metadata from the model")
    

@api.get('/health')
def get_health():
    return {"status" : "OK"}

@api.get('/model-info/{model_id}')
def model_get_id(model_id : int):
    if model_id not in model_information:
        raise HTTPException(status_code=404, detail=f"Model {model_id} not found")
    return model_information.get(model_id)  

@api.post('/predict', response_model=Responsemodel)
def model_inference(info: Requestmodel):
    response_text,tokens_used = simulated_api_call(info.text,info.temperature,info.max_tokens, flag=1)
    
    if response_text is None or tokens_used is None:
        raise HTTPException(status_code=500, detail="Model failed to generate a response")
    data = Data(
        response = response_text,
        model_used = info.model.value,
        tokens_used = tokens_used,
        )
    metadata = Metadata(
        temperature = info.temperature,
        max_tokens = info.max_tokens,
        )
    return {
        "status": Statusname.success,
        "data": data,
        "metadata": metadata
    }


def simulated_api_call(content : str,temperature : float,max_tokens :int,flag=0):
    if flag:
        return "simulated response",100
    return None,None

