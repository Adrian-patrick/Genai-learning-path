import pymysql

def connect_db():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="root123",
        database="library"
    )