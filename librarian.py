from database import connect_db
from models import Book

class LibrarianActions:

    def add_book(self):
        con = connect_db()
        cur = con.cursor()

        book = Book(
            input("Book ID: "),
            input("Title: "),
            input("Author: ")
        )
        count = int(input("Quantity: "))

        cur.execute("SELECT * FROM Books WHERE BookID=%s", (book.bid,))
        if cur.fetchone():
            print("Book already exists")
            con.close()
            return

        cur.execute("INSERT INTO Books VALUES (%s,%s,%s)",
                    (book.bid, book.title, book.author))

        cur.execute("INSERT INTO Inventory VALUES (%s,%s)",
                    (book.bid, count))

        con.commit()
        con.close()
        print("Book added")

    def view_books(self):
        con = connect_db()
        cur = con.cursor()

        cur.execute("SELECT * FROM Books")
        for row in cur.fetchall():
            print(row)

        con.close()

    def delete_book(self):
        con = connect_db()
        cur = con.cursor()

        bid = input("Enter Book ID: ")

        cur.execute("SELECT * FROM Books WHERE BookID=%s", (bid,))
        if not cur.fetchone():
            print("Book not found")
            con.close()
            return

        cur.execute("DELETE FROM Books WHERE BookID=%s", (bid,))
        cur.execute("DELETE FROM Inventory WHERE BookID=%s", (bid,))
        cur.execute("DELETE FROM IssuedBooks WHERE BookID=%s", (bid,))

        con.commit()
        con.close()
        print("Book deleted")

    def add_user(self):
        con = connect_db()
        cur = con.cursor()

        uid = input("User ID: ")
        pwd = input("Password: ")

        cur.execute("INSERT INTO Users VALUES (%s,%s,'student')", (uid, pwd))

        con.commit()
        con.close()
        print("User added")