class User:
    def __init__(self, uid, password, role):
        self.uid = uid
        self.password = password
        self.role = role


class Student(User):
    def __init__(self, uid, password):
        super().__init__(uid, password, "student")


class Librarian(User):
    def __init__(self, uid, password):
        super().__init__(uid, password, "librarian")


class Book:
    def __init__(self, bid, title, author):
        self.bid = bid
        self.title = title
        self.author = author