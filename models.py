from pydantic import BaseModel,Field
from enum import Enum

class Category(str,Enum):
    spam = "spam"
    important = "important"
    promotion = "promotion"
    general = "general"


class RequestModel(BaseModel):
    email_text : str

class ResponseModel(BaseModel):
    category : Category
    reason : str = Field(...,max_length=200)