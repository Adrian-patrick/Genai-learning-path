from employee import Employee


def main():
    employee = Employee()

    while True:
        print(
            """
Employee Management System
Choose an option:
1: Add an employee
2: View all employees
3: Update employee salary
4: Delete employee
5: Exit
"""
        )

        try:
            option = int(input("Enter an option: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if option == 1:
            employee.add_employee()
        elif option == 2:
            employee.view_employees()
        elif option == 3:
            employee.update_employee()
        elif option == 4:
            employee.delete_employee()
        elif option == 5:
            print("Exiting...")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()

"""
improvements:
employee created once
better formatting
input validation
"""
