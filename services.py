import pymysql
from models import *

def connect():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="root123",
        database="task_management"
    )

db = connect()
cur = db.cursor()

def check_user_id(user_id :int):
    check_query = "select * from users where id = %s "
    cur.execute(check_query,user_id)
    data = cur.fetchall()
    print(data)
    if not data :
        return False
    return True

def db_get_all_users():
    cur.execute("select * from users")
    data = cur.fetchall()
    return data

def db_add_user(info : Userrequest):
    if check_user_id(info.id):
        raise ValueError("id already exists")
    try:
        query = "insert into users values(%s,%s,%s)"
        val = (info.id,info.name,info.email)
        cur.execute(query,val)     
        db.commit() 
    except Exception as e:
        print(e)
    return

def db_delete_user(user_id : int ):
    if not check_user_id(user_id):
        raise ValueError("id not found")
    try:
        query = "delete from users where id = %s"
        cur.execute(query,user_id)     
        db.commit() 
    except Exception as e:
        print(e)
    return



