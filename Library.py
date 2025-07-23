import os
from datetime import datetime, timedelta
from models import User, Book, Borrow
from fileManager import count_users, count_books, count_borrows, ensure_files_exist, load_users, load_books, load_borrows
from globals import users_list, book_list, borrows_list


adminUserName = 'admin'
adminPassword = 'admin'


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_borrowed_books_admin(): # admin
    if not borrows_list:
        clear_console()
        print("No borrowed books found.")
        input("Press Enter to continue...")
        clear_console()
        return

    print("Borrowed Books History:")
    print("-" * 80)
    
    for borrow in borrows_list:
        # یافتن اطلاعات کتاب
        book_found = None
        for book in book_list:
            if book.bookId == borrow.bookId:
                book_found = book
                break

        # یافتن اطلاعات کاربر
        user_found = None
        for user in users_list:
            if user.userId == borrow.userId:
                user_found = user
                break

        # نمایش اطلاعات در صورت موجود بودن کتاب و کاربر
        if book_found and user_found:
            return_status = "Returned" if borrow.isBookReturned == "True" else f"Due Date: {borrow.dueDate}"
            print(f"User: {user_found.name}, Book: {book_found.title}, Author: {book_found.author}, "
                  f"Borrow Date: {borrow.borrowDate}, {return_status}")
    print("-" * 80)
    input("Press Enter to continue...")
    clear_console()

def return_book(userId): # user 

    clear_console()
    # نمایش کتاب‌های قرضی که کاربر قرض کرده است
    borrowed_books = []
    for i in borrows_list:
        if i.userId == userId and not i.isBookReturned:
            borrowed_books.append(i)

    if not borrowed_books:
        print("You have no books to return.")
        input("Press Enter to continue...")
        clear_console()
        return

    
    print("Your borrowed books:")
    
    x = 1  
    for borrow in borrowed_books:
        book_found = None
        for i in book_list:
            if i.bookId == borrow.bookId:
                book_found = i
                break

        if book_found:
            print(f"{x}. BookID: {book_found.bookId}, Title: {book_found.title}, "
                f"Author: {book_found.author}, Due Date: {borrow.dueDate}")
            x += 1  

    # انتخاب کتاب برای بازگشت
    try:
        book_index = int(input("Enter the number of the book you want to return: ")) - 1
        selected_borrow = borrowed_books[book_index]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    selected_borrow.isBookReturned = True

    # افزایش موجودی کتاب
    book_found = None
    for i in book_list:
        if i.bookId == selected_borrow.bookId:
          book_found = i
          break

    if book_found:
        book_found.availableCount = str(int(book_found.availableCount) + 1)

    # ذخیره‌سازی تغییرات در فایل‌های مربوطه
    try:
        with open("borrows.txt", "w", encoding="utf-8") as file:
            for borrow in borrows_list:
                file.write(f"{borrow.borrowId},{borrow.userId},{borrow.bookId},{borrow.borrowDate},{borrow.dueDate},{borrow.isBookReturned}\n")
    except IOError as e:
        print(f"Error saving borrows: {e}")

    try:
        with open("books.txt", "w", encoding="utf-8") as file:
            for book in book_list:
                file.write(f"{book.bookId},{book.title},{book.author},{book.availableCount},{book.dateAdded}\n")
    except IOError as e:
        print(f"Error saving books: {e}")

    print(f"Book '{book_found.title}' returned successfully!")
    input("Press Enter to continue...")
    clear_console()

def show_borrowed_books(userId):  # user
    clear_console()
    borrowed_books = []
    for borrow in borrows_list:
        if borrow.userId == userId and borrow.isBookReturned != "True":
            borrowed_books.append(borrow)

    if not borrowed_books:
        print("You have not borrowed any books or all books have been returned.")
        input("Press Enter to go back...")
        clear_console()
        return

    print("List of borrowed books:")
    print("-" * 50)
    for borrow in borrowed_books:
        book_found = None
        for book in book_list:
            if book.bookId == borrow.bookId:  # تطابق ID کتاب‌ها
                book_found = book
                break

        if book_found:
            return_status = f"Due Date: {borrow.dueDate}"
            print(f"BookID: {book_found.bookId}, Title: {book_found.title}, Author: {book_found.author}, "
                  f"Borrow Date: {borrow.borrowDate}, {return_status}")
    print("-" * 50)
    input("Press Enter to continue...")
    clear_console()

def search_books(): # user
    clear_console()
    print("=== Search Books ===")
    
    if not book_list:
        print("No books available.")
        input("Press Enter to go back...")
        clear_console()
        return

    search_term = input("Enter the book title or author to search (leave blank for all available books): ").lower()
    
    # فیلتر کردن کتاب‌ها بر اساس عنوان یا نویسنده
    available_books = []
    for i in book_list:
        if int(i.availableCount) > 0 and (search_term in i.title.lower() or search_term in i.author.lower()):
            available_books.append(i)
            
    clear_console()
    print("=== Search Results ===")
    if not available_books:
        print("⚠️ No available books found.")
    else:
        print("Available books found:")
        print("-" * 50)
        for i in available_books:
            print(f"BookID: {i.bookId}, Title: {i.title}, Author: {i.author}, Available Count: {i.availableCount}")
        print("-" * 50)
        
    input("Press Enter to go back...")
    clear_console()

def borrow_book(userId): # user
    clear_console()
    
    bookId = input("Enter the Book ID you want to borrow: ")

    # بررسی اینکه آیا کتاب وارد شده موجود است یا خیر
    book_found = None
    for i in book_list:
        if i.bookId == bookId:
            book_found = i
            break
    if book_found is None:
        print("Error: Book not found.")
        input("Press Enter to continue...")
        clear_console()
        return

    # بررسی موجودی
    if int(book_found.availableCount) <= 0:
        print(f"Sorry, '{book_found.title}' is currently unavailable.")
        input("Press Enter to continue...")
        clear_console()
        return

    # بررسی اینکه آیا کاربر قبلاً این کتاب را قرض گرفته است
    borrowId = f"{userId}-{bookId}"
    for i in borrows_list:
        if i.borrowId == borrowId:
            print("Error: You have already borrowed this book.")
            input("Press Enter to continue...")
            clear_console()
            return
    
    
    # ثبت اطلاعات قرض کتاب
    borrowDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dueDate = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    isBookReturned = False

    borrow = Borrow(borrowId, userId, bookId, borrowDate, dueDate, isBookReturned)
    
    # اضافه کردن اطلاعات قرض به لیست
    borrows_list.append(borrow)

    # کاهش موجودی کتاب
    book_found.availableCount = str(int(book_found.availableCount) - 1)
    
    # به‌روزرسانی فایل کتاب‌ها با موجودی جدید
    try:
        with open("books.txt", "w", encoding="utf-8") as file:
            for book in book_list:
                file.write(f"{book.bookId},{book.title},{book.author},{book.availableCount},{book.dateAdded}\n")
    except IOError as e:
        print(f"Error updating books file: {e}")
        return

    # ذخیره‌سازی تغییرات در فایل قرض‌ها
    try:
        with open("borrows.txt", "w", encoding="utf-8") as file:
            for borrow in borrows_list:
                file.write(
                    f"{borrow.borrowId},{borrow.userId},{borrow.bookId},{borrow.borrowDate},{borrow.dueDate},{borrow.isBookReturned}\n"
                )
    except IOError as e:
        print(f"Error saving borrows: {e}")

    print(f"Book '{book_found.title}' borrowed successfully! Due date: {dueDate}")
    input("Press Enter to go back...")
    clear_console()
        
def remove_books(): # admin
    bookId = input("Enter book ID to remove: ")

    # جستجو در لیست کتاب
    book_to_remove = None  
    for i in book_list:
        if i.bookId == bookId:
            book_to_remove = i
            break

    if book_to_remove is None:
        print("Error: Book not found.")
        input("Press Enter to continue...")
        return

    # حذف کتاب از لیست
    book_list.remove(book_to_remove)
    print(f"Book ({bookId}) removed successfully!")  

    # به‌روزرسانی فایل با حذف کتاب
    with open("books.txt", "w", encoding="utf-8") as file:
        for book in book_list:
            file.write(f"{book.bookId},{book.title},{book.author},{book.availableCount},{book.dateAdded}\n")

    print("Books file updated successfully.")

def show_books(): # admin
    clear_console()
    print("=== List of Books ===")
    if not book_list:
        print("No books found.")
        return


    print("-" * 50)
    for book in book_list:
        print(f"BookID: {book.bookId}, Title: {book.title}, Author: {book.author}, Available Count: {book.availableCount}")
    print("-" * 50)

def add_book(): # admin
    clear_console()
    bookId = input("Enter Book ID: ")
    
    # بررسی تکراری بودن
    with open("books.txt", "r") as file:
        for i in file:
            existing_bookId = i.split(",")[0]
            if bookId == existing_bookId:
                print("Error: Book ID already exists. Please try again.")
                input("Press Enter to continue...")
                clear_console()
                return 

    title = input("Enter book title: ")
    author = input("Enter book author: ")
    
    while True:
        available_count = input("Enter available count: ")
        if  available_count.isdigit() and int(available_count) > 0:
            break
        else:
            print("Please enter a number\n")
    dateAdded = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # اضافه به لیست کتاب‌
    new_book = Book(bookId, title, author, available_count, dateAdded)  
    book_list.append(new_book)
    
    # ریختن توی فایل
    with open("books.txt", "a", encoding="utf-8") as file:
        file.write(f"{bookId},{title},{author},{available_count},{dateAdded}\n")  
    
    print("Book added successfully!")
    input("Press Enter to continue...")
    clear_console()

def add_user(): # admin
    clear_console()
    userId = input("Enter user ID: ")
    
    # بررسی تکراری بودن
    with open("users.txt", "r") as file:
        for i in file:
            userTekrari = i.split(",")[0]
            if userId == userTekrari:
                print("Error: User ID already exists. Please try again.")
                input("Press Enter to try again...")
                clear_console()
                return 

    password = input("Enter password: ")
    name = input("Enter name: ")
    dateJoined = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # اضافه به لیست کاربران
    new_user = User(userId, password, name, dateJoined)
    users_list.append(new_user)
    
    # ریختن توی فایل
    with open("users.txt", "a") as file:
        file.write(f"{userId},{password},{name},{dateJoined}\n")

    clear_console()
    print("User added successfully!")

def remove_user(): # admin
    clear_console()
    userId = input("Enter user ID to remove: ")

    user_to_remove = None
    # جستجو در لیست کاربران
    for i in users_list:
        if i.userId == userId:
            user_to_remove = i
            break

    if user_to_remove is None:
        print("Error: User not found.")
        input("Press Enter to continue...")
        clear_console()
        return

    # حذف کاربر از لیست
    users_list.remove(user_to_remove)
    print(f"User ({userId}) removed successfully!")
    input("Press Enter to continue...")
    clear_console()
    
    # به‌روزرسانی فایل با حذف کاربر
    with open("users.txt", "w") as file:
        for user in users_list:
            file.write(f"{user.userId},{user.password},{user.name},{user.dateJoined}\n")

def show_users():  # admin
    clear_console()
    if not users_list:  # بررسی خالی بودن لیست یوزر
        print("No users found.")
        input("Press Enter to continue...")
        return

    print("List of users:")
    print("-" * 50)
    for i in users_list:
        print(f"UserID: {i.userId}, Name: {i.name}, Date Joined: {i.dateJoined}")
    print("-" * 50)
    input("Press Enter to continue...")
    clear_console()

def manage_users(): # admin
    clear_console()
    while True:
        print("-------------------")
        x = input("1. Add user\n2. Remove user\n3. Show users\n0. Back\n")
        if x == '1':
            add_user()
        elif x == '2':
            remove_user()
        elif x == '3':
            show_users()
        elif x == '0':
            clear_console()
            break
        else:
            clear_console()
            print("Invalid number.")
            input("Press Enter to continue...")
            clear_console()

def manage_books(): # admin
    clear_console()
    while True:
        print("-------------------")
        x = input("1. Add book\n2. Remove book\n3. Show books\n0. Back\n")
        if x == '1':
            add_book()
        elif x == '2':
            remove_books()
        elif x == '3':
            show_books()
        elif x == '0':
            clear_console()
            break
        else:
            clear_console()
            print("Invalid number.")
            input("Press Enter to continue...")
            
def admin_menu():
    clear_console()
    while True:
        x = input("Welcome admin\n1. Manage users\n2. Manage books\n3. See borrowed books\n0. Log out\n")
        if x == '1':
            manage_users()
        elif x == '2':
            manage_books()
        elif x == '3':
            show_borrowed_books_admin()
        elif x == '0':
            main()
        else:
            clear_console()
            print("Invalid number.")
            input("Press Enter to continue...")
            clear_console()
            
def user_menu(user):
    clear_console()
    while True:
        x = input(f"Welcome {user.name}\n1. Search available books\n2. Borrow book\n3. See borrowed books\n4. Return book\n0. Log out\n")
        if x == '1':
            search_books()
        elif x == '2':
            borrow_book(user.userId)
        elif x == '3':
            show_borrowed_books(user.userId)  
        elif x == '4':
            return_book(user.userId)
        elif x == '0':
            clear_console()
            break
        else:
            clear_console()
            print("Invalid number.")
            input("Press Enter to continue...")

def main():
    
    ensure_files_exist()
    load_users()
    load_books()
    load_borrows()

 
    totalUsers = count_users()
    totalBooks = count_books()
    totalBorrows = count_borrows()
        
    clear_console()
    print("\n*** Welcome to the Libary ***")
    print(f"Total Users: {totalUsers}")
    print(f"Total Books: {totalBooks}")
    print(f"Total Borrows: {totalBorrows}\n")
    
    while True:
        
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        if username == adminUserName and password == adminPassword:
            admin_menu()
        else:
            user_found = None
            for i in users_list:
                if i.userId.strip().lower() == username.strip().lower() and i.password.strip() == password.strip():
                    user_found = i
                    break
        
        if user_found:
            user_menu(user_found)
        else:
            clear_console()
            print("Incorrect username or password")
            input("Press Enter to try again...")
            clear_console()

main()