from database import connect_db
from librarian import LibrarianActions
from student import StudentActions
from models import Student, Librarian

def login():
    con = connect_db()
    cur = con.cursor()

    uid = input("User ID: ")
    pwd = input("Password: ")

    # admin login
    if uid == "admin" and pwd == "admin":
        return Librarian(uid, pwd)

    cur.execute("SELECT * FROM Users WHERE UserID=%s AND Password=%s", (uid, pwd))
    user = cur.fetchone()

    con.close()

    if user:
        return Student(uid, pwd)
    else:
        print("Invalid login")
        return None


def main():
    user = login()

    if not user:
        return

    if user.role == "librarian":
        lib = LibrarianActions()

        while True:
            print("\n1.Add Book\n2.View Books\n3.Delete Book\n4.Add User\n5.Exit")
            ch = input("Choice: ")

            if ch == "1":
                lib.add_book()
            elif ch == "2":
                lib.view_books()
            elif ch == "3":
                lib.delete_book()
            elif ch == "4":
                lib.add_user()
            else:
                break

    else:
        stu = StudentActions()

        while True:
            print("\n1.View Books\n2.Borrow\n3.Return\n4.Exit")
            ch = input("Choice: ")

            if ch == "1":
                stu.view_books()
            elif ch == "2":
                stu.borrow_book(user.uid)
            elif ch == "3":
                stu.return_book(user.uid)
            else:
                break


if __name__ == "__main__":
    main()