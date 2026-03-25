from pydantic import BaseModel,Field,field_validator,EmailStr
from fastapi import HTTPException
from enum import Enum
import datetime

class Userrequest(BaseModel):
    id : int 
    name : str
    email : EmailStr

    #@field_validator("email")
    #def validate_email(cls,value):
        #users = get_all_users()
        #for email in users:
            #if value == email:
                #raise HTTPException(detail="email already exists")
            
class Status(str,Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class Priority(int,Enum):
    low = 1
    medium = 2
    high = 3


class Taskrequest(BaseModel):
    id : int
    title : str
    description : str
    status : Status
    priority : Priority
    assigned_to : int
    due_date : datetime.date
    created_at : datetime.date


