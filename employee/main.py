from employee import Employee

def main():
    while True:
        print("""
              employee management system
              choose an option :
              1 : add an employee
              2 : view all employees
              3 : update employee salary
              4 : delete employee
              5 : exit
              """)
        employee = Employee()
        option = int(input("enter an option : "))
        if option == 1 :
            employee.add_employee()
        elif option == 2 :
            employee.view_employees()
        elif option == 3:
            employee.update_employee()
        elif option == 4 :
            employee.delete_employee()
        elif option == 5 :
            print("exiting ...")
            exit()
        else:
            print("invalid input")
        
if __name__ == "__main__":
    main()