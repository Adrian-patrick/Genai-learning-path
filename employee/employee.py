from database import connect

class Employee:
    def __init__(self):
        self.db = connect()
        self.cur = self.db.cursor()

    def add_employee(self):
        id = input("enter id : ")
        name = input("enter name : ")
        salary = input("enter salary : ")

        self.cur.execute("insert into employee values(%s,%s,%s)",(id,name,salary),)
        self.db.commit()
        print("added successfully")

    def view_employees(self):
        self.cur.execute("select * from employee")

        data = self.cur.fetchall()
        for row in data:
            print(f"id : {row[0]} name : {row[1]} salary : {row[2]}")


    def update_employee(self):
        id = input("enter id to update : ")
        salary = input("enter salary to update : ")
        self.cur.execute("update employee set salary = %s where id = %s",(salary,id),)
        self.db.commit()
        print("updated salary")

    def delete_employee(self):
        id = input("eneter the id : ")
        self.cur.execute("delete from employee where id = %s;",(id),)
        self.db.commit()
        print("deleted employee")
