import os
from models import User, Book, Borrow
from globals import users_list, book_list, borrows_list

        
def count_users(): 
    try:
        with open("users.txt", "r", encoding="utf-8") as f:
            count = 0
            for line in f:
                if line.strip():
                    count += 1
            return count
            
    except FileNotFoundError:
        return 0

def count_books(): 
    try:
        with open("books.txt", "r", encoding="utf-8") as f:
            count = 0
            for line in f:
                if line.strip():  # بررسی می‌کند که خط خالی نباشد
                    count += 1
            return count
    except FileNotFoundError:
        return 0

def count_borrows(): 
    try:
        with open("borrows.txt", "r", encoding="utf-8") as f:
            count = 0
            for line in f:
                if line.strip():  # بررسی می‌کند که خط خالی نباشد
                    count += 1
            return count
    except FileNotFoundError:
        return 0

def ensure_files_exist():
    files = ["users.txt", "books.txt", "borrows.txt"]  
    for file_name in files:
        if not os.path.exists(file_name):  # بررسی می‌کند که فایل وجود دارد یا نه
            with open(file_name, "w", encoding="utf-8") as f:
                f.write("")  # ایجاد یک فایل خالی در صورت نبودن
    
def load_users(): 
    from globals import users_list 
    users_list.clear()  
    try:
        with open("users.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                        userId, password, name, dateJoined = line.split(",")
                        user = User(userId.strip(), password.strip(), name.strip(), dateJoined.strip())
                        users_list.append(user)
    except FileNotFoundError:
        print("No users found, starting with an empty list.")

def load_books():
    global book_list
    book_list.clear()  # پاک کردن لیست برای جلوگیری از داده‌های تکراری
    try:
        with open("books.txt", "r", encoding="utf-8") as file:
            for line in file:
                if line.strip():  
                    bookId, title, author, available_count, dateAdded = line.strip().split(",")
                    book = Book(
                        bookId.strip(),
                        title.strip(),
                        author.strip(),
                        int(available_count.strip()),
                        dateAdded.strip()
                    )
                    book_list.append(book)
    except FileNotFoundError:
        print("Error: books.txt not found. Starting with an empty book list.")
    except ValueError as e:
        print(f"Error in books.txt format: {e}")

def load_borrows():
    global borrows_list
    borrows_list.clear()  # پاک کردن لیست برای جلوگیری از داده‌های تکراری
    try:
        with open("borrows.txt", "r", encoding="utf-8") as file:
            for line in file:
                if line.strip():  # بررسی اینکه خط خالی نباشد
                    borrowId, userId, bookId, borrowDate, dueDate, isBookReturned = line.strip().split(",")
                    borrow = Borrow(
                        borrowId.strip(),
                        userId.strip(),
                        bookId.strip(),
                        borrowDate.strip(),
                        dueDate.strip(),
                        isBookReturned.strip() == "True"
                    )
                    borrows_list.append(borrow)
    except FileNotFoundError:
        print("Error: borrows.txt not found. Starting with an empty borrows list.")
    except ValueError as e:
        print(f"Error in borrows.txt format: {e}")
