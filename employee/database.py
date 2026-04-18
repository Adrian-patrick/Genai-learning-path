import pymysql

def connect():
    return pymysql.connect(
        host="your_host",
        user="your_user",
        password="your_pass",
        database="your_db"
    )

db = connect()
cur = db.cursor()

cur.execute("create database company")
cur.execute("use company")
cur.execute("create table employee( id int primary key, name varchar(50), salary decimal(10,2))")
cur.commit()
cur.close()
