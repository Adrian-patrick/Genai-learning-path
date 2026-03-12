from database import connect


class Employee:
    def __init__(self):
        self.db = connect()
        self.cur = self.db.cursor()

    def add_employee(self):
        emp_id = input("Enter id: ")
        name = input("Enter name: ")
        salary = input("Enter salary: ")

        self.cur.execute(
            "INSERT INTO employee VALUES (%s, %s, %s)",
            (emp_id, name, salary),
        )
        self.db.commit()

        print("Employee added successfully")

    def view_employees(self):
        self.cur.execute("SELECT * FROM employee")

        rows = self.cur.fetchall()
        for row in rows:
            print(f"id: {row[0]} | name: {row[1]} | salary: {row[2]}")

    def update_employee(self):
        emp_id = input("Enter id to update: ")
        salary = input("Enter new salary: ")

        self.cur.execute(
            "UPDATE employee SET salary = %s WHERE id = %s",
            (salary, emp_id),
        )
        self.db.commit()

        print("Salary updated")

    def delete_employee(self):
        emp_id = input("Enter id: ")

        self.cur.execute(
            "DELETE FROM employee WHERE id = %s",
            (emp_id,),
        )
        self.db.commit()

        print("Employee deleted")

"""
improvements 
proper sql syntax
no overshadowing variables
"""