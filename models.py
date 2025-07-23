class User:  
    def __init__(self, userId, password, name, dateJoined):
        self.userId = userId
        self.password = password
        self.name = name
        self.dateJoined = dateJoined


class Book:  
    def __init__(self, bookId, title, author, availableCount, dateAdded = None):
        self.bookId = bookId
        self.title = title
        self.author = author
        self.availableCount = availableCount
        self.dateAdded = dateAdded

class Borrow:  
    def __init__(self, borrowId, userId, bookId, borrowDate, dueDate, isBookReturned):
        self.borrowId = borrowId
        self.userId = userId
        self.bookId = bookId
        self.borrowDate = borrowDate
        self.dueDate = dueDate
        self.isBookReturned = isBookReturned
        

