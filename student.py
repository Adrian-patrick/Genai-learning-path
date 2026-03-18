from database import connect_db
from datetime import date

class StudentActions:

    def view_books(self):
        con = connect_db()
        cur = con.cursor()

        cur.execute("SELECT * FROM Books")
        for row in cur.fetchall():
            print(row)

        con.close()

    def borrow_book(self, uid):
        con = connect_db()
        cur = con.cursor()

        bid = input("Enter Book ID: ")

        # check limit
        cur.execute("SELECT COUNT(*) FROM IssuedBooks WHERE UserID=%s", (uid,))
        total = cur.fetchone()[0]

        if total >= 3:
            print("Limit reached")
            con.close()
            return

        # check stock
        cur.execute("SELECT Count FROM Inventory WHERE BookID=%s", (bid,))
        res = cur.fetchone()

        if res is None or res[0] <= 0:
            print("Book not available")
            con.close()
            return

        cur.execute("INSERT INTO IssuedBooks VALUES (%s,%s,%s)",
                    (bid, uid, date.today()))

        cur.execute("UPDATE Inventory SET Count = Count - 1 WHERE BookID=%s", (bid,))

        con.commit()
        con.close()
        print("Book borrowed")

    def return_book(self, uid):
        con = connect_db()
        cur = con.cursor()

        bid = input("Enter Book ID: ")

        cur.execute("SELECT * FROM IssuedBooks WHERE BookID=%s AND UserID=%s", (bid, uid))
        if not cur.fetchone():
            print("You didn't borrow this")
            con.close()
            return

        cur.execute("DELETE FROM IssuedBooks WHERE BookID=%s AND UserID=%s", (bid, uid))
        cur.execute("UPDATE Inventory SET Count = Count + 1 WHERE BookID=%s", (bid,))

        con.commit()
        con.close()
        print("Book returned")