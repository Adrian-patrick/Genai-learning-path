# 📚 Library Management System

This is a simple Library Management System developed using Python.
It uses Object-Oriented Programming (OOP) concepts and MySQL database for storing data.

---

## 🚀 Features

### 👨‍🏫 Librarian

* Add new books
* View all books
* Delete books
* Add users

### 🎓 Student

* View available books
* Borrow books (maximum 3)
* Return books

---

## 🏗️ Project Structure

* `main.py` → Main program (menu + login)
* `database.py` → Database connection
* `models.py` → Classes (User, Student, Librarian, Book)
* `librarian.py` → Librarian functions
* `student.py` → Student functions
* `test.py` → Test database connection

---

## 🗂️ Database Tables

### Books

* BookID
* Title
* Author

### Users

* UserID
* Password
* Role

### Inventory

* BookID
* Count

### IssuedBooks

* BookID
* UserID
* IssueDate

---

## ⚙️ Rules

* A student can borrow **maximum 3 books**
* Book count decreases when borrowed and increases when returned
* Admin login is:

  * **User ID:** admin
  * **Password:** admin

---

## 🛠️ Setup Instructions

### 1. Install dependency

```bash
pip install pymysql
```

### 2. Create database

```sql
CREATE DATABASE library;
```

### 3. Create tables

```sql
CREATE TABLE Books (
    BookID VARCHAR(10) PRIMARY KEY,
    Title VARCHAR(100),
    Author VARCHAR(100)
);

CREATE TABLE Users (
    UserID VARCHAR(10) PRIMARY KEY,
    Password VARCHAR(50),
    Role VARCHAR(20)
);

CREATE TABLE Inventory (
    BookID VARCHAR(10),
    Count INT
);

CREATE TABLE IssuedBooks (
    BookID VARCHAR(10),
    UserID VARCHAR(10),
    IssueDate DATE
);
```

### 4. Update database credentials

Open `database.py` and change:

```python
password="your_password"
```

---

### 5. Run the project

```bash
python main.py
```

---

## 📌 Requirements

* Python 3.x
* MySQL
* pymysql

---

## 📖 Description

This project demonstrates:

* Object-Oriented Programming (OOP)
* Database connectivity using MySQL
* Basic CRUD operations
* Simple command-line interface

---
