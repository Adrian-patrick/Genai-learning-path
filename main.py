from fastapi import FastAPI,HTTPException,Request,Depends
from typing import Annotated
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field,field_validator
from typing import Optional
from enum import Enum
import time

class Version(int,Enum):
    v1 = 1
    v2 = 2

class Modelservice():
    def __init__(self):
        #llm loading logic
        pass

    def predict(self,content : str,temperature : float,max_tokens :int,version:Version,flag=0):
        time.sleep(1)
        if flag:
            if version.value == 1:
                return "simulated response of version 1",100
            if version.value == 2:
                return "simulated response of version 2",100
        return None,None

@asynccontextmanager
async def lifespan(app : FastAPI):
    app.state.model = Modelservice()
    yield
    del app.state.model

api = FastAPI(lifespan=lifespan)

def get_model(request:Request):
    return request.app.state.model

model_dependency = Annotated[Modelservice,Depends(get_model)]

model_information = {1: {"model name" :"gpt4","type": "Multimodal Foundation Model",
                          "Context Window": "128k tokens"},
                          2: {"model name":"claude3.5","type": "Large Language Model",
                               "Context Window": "200k tokens"}}
class Modelname(str,Enum):
    gpt4 = "gpt4"
    claude35 = "claude3.5"

class Statusname(str,Enum):
    success = "success"
    error = "error"

class Requestmodel(BaseModel):
    model: Modelname = Field(..., description="model name", examples=["gpt4"])
    text: str = Field(...,max_length=1000, description="content to infer", 
                      examples=["can you explain what is a supercar?"])
    temperature: Optional[float] = Field(default=0.7,ge=0,le=1 ,
                                        description="higher values make the output more random")
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

class Debug(BaseModel):
    input_length : int
    version : Version

class Metadata(BaseModel):
    temperature : float
    max_tokens : int
    debug_info : Optional[Debug]

class Responsemodel(BaseModel):
    status : Statusname = Field(default= Statusname.success, description="status")
    data: Data  = Field(..., description="data from the model")
    metadata : Optional[Metadata] = Field(description="metadata from the model")

class Modelupdate(BaseModel):
    model_name : Optional[str] = Field(description="model name",examples=['gpt4'])
    type : Optional[str] = Field(description="model type",examples=['llm'])
    context_window : Optional[str] = Field(description="context window",examples=['200 k'])

    
#middleware

@api.middleware("http")
async def log_request_time(request : Request ,call_next):
    start_time = time.time()
    try : 
        response = await call_next(request)
        return response
    finally:
        end_time = time.time()
        print(f"[LOG] {request.method} {request.url.path} | Execution Time : {int((end_time-start_time)*1000)}ms")

#api endpoints
@api.get('/health')
async def get_health():
    return {"status" : "OK"}

@api.get('/model-info/{model_id}')
async def model_get_id(model_id : int):
    if model_id not in model_information:
        raise HTTPException(status_code=404, detail=f"Model id : {model_id} not found")
    return model_information.get(model_id)  

@api.post('/predict', response_model=Responsemodel)
async def model_inference(model : model_dependency,info: Requestmodel,include_debug : bool = False,
                    include_metadata :bool = True,version :Version = Version.v1):

    response_text,tokens_used = model.predict(info.text,info.temperature,
                                              info.max_tokens,version, flag=1)
    
    if response_text is None or tokens_used is None:
        raise HTTPException(status_code=500, detail="Model failed to generate a response")
    data = Data(
        response = response_text,
        model_used = info.model.value,
        tokens_used = tokens_used,
        )
    if include_debug:
        debug = Debug(
            input_length = len(info.text),
            version = version,
    )
    else:
        debug = None
    if include_metadata :
        metadata = Metadata(
            temperature = info.temperature,
            max_tokens = info.max_tokens,
            debug_info= debug 
            )
    else :
        metadata = None
    return {
        "status": Statusname.success,
        "data": data,
        "metadata": metadata 
    }

@api.patch('/model-info/{model_id}')
async def update_model(model_id : int ,info : Modelupdate):
    if model_id not in model_information:
        raise HTTPException(status_code=404,detail=f"model id {model_id} not found")
    model = model_information[model_id]
    if info.model_name is not None:
        model["model name"] =info.model_name
    if info.type is not None:
        model["type"] = info.type
    if info.context_window is not None:
        model["Context Window"] = info.context_window

    return {"status" : Statusname.success , "data" : model_information[model_id]}

@api.delete('/model-info/{model_id}')
async def delete_model(model_id : int ):
    if model_id not in model_information:
        raise HTTPException(status_code=404,detail=f"model id {model_id} not found")
    deleted_data  = model_information[model_id].copy()
    del model_information[model_id]
    return {"status" : Statusname.success , "data" : deleted_data}




