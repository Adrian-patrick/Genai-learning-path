from fastapi import FastAPI,HTTPException
from models import Taskrequest,Userrequest
from services import db_get_all_users,db_add_user,db_delete_user


app = FastAPI()


@app.get("/users")
def get_users():
    all_users = db_get_all_users()
    return all_users
        
    
@app.post("/users/add-user")
def add_user(info : Userrequest):
    try:
        db_add_user(info)
    except Exception as e:
        raise HTTPException(status_code=500,detail="user already exists")
    return {"status" : "added new user"}

@app.delete("/users/{user_id}")
def delete_user(user_id : int):
    try:
        db_delete_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=500,detail="user not found")
    return {"status" : "deleted user"}






