import pymysql

def connect_db():
    return pymysql.connect(
        host="your_host",
        user="your_user",
        password="your_pass",
        database="your_db"
    )
