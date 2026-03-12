import pymysql

def connect():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="root123",
        database="company"
    )

db = connect()
cur = db.cursor()

cur.execute("create database company")
cur.execute("use company")
cur.execute("create table employee( id int primary key, name varchar(50), salary decimal(10,2))")
cur.commit()
cur.close()