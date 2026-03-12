# Employee Management System

A simple **Python CLI-based Employee Management System** that allows users to manage employee records stored in a database.

This project demonstrates basic **CRUD operations (Create, Read, Update, Delete)** using Python and SQL.

---

## Features

* Add a new employee
* View all employees
* Update employee salary
* Delete an employee
* Simple command line interface

---

## Project Structure

```
employee-management-system/
│
├── main.py          # Entry point of the application
├── employee.py      # Employee class with CRUD operations
├── database.py      # Database connection setup
└── README.md
```

---

## Requirements

Make sure you have the following installed:

* Python 3.8+
* A SQL database (e.g., MySQL / PostgreSQL)
* Required Python database driver

Example for MySQL:

```
pip install mysql-connector-python
```

---

## Database Setup

Create the database table before running the program.

Example SQL:

```sql
CREATE TABLE employee (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    salary INT
);
```

---

## Running the Application

Run the program using:

```
python main.py
```

You will see a menu like this:

```
Employee Management System

1: Add an employee
2: View all employees
3: Update employee salary
4: Delete employee
5: Exit
```

Choose an option and follow the prompts.

---

## Example Usage

### Add Employee

```
Enter id: 1
Enter name: Alice
Enter salary: 50000
```

### View Employees

```
id: 1 | name: Alice | salary: 50000
```

### Update Salary

```
Enter id to update: 1
Enter new salary: 60000
```

### Delete Employee

```
Enter id: 1
```

---

## Concepts Demonstrated

* Python classes
* SQL CRUD operations
* Database connections
* Command line interfaces
* Basic program structure

---

## Possible Improvements

Future improvements could include:

* Input validation
* Error handling
* Logging
* Database connection pooling
* Using an ORM like SQLAlchemy
* Adding a REST API using FastAPI
* Writing unit tests

---

