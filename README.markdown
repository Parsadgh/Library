# Library Management System 📚

Welcome to the **Library Management System**, a command-line application built in Python using object-oriented programming. This system lets **admins** manage users & books, while **regular users** can search for, borrow, and return books. All data is persisted in text files, so your users, books, and borrow history stay intact—even if you close and reopen the app!

---

## 🚀 Table of Contents

1. [Features](#features)  
2. [Prerequisites](#prerequisites)  
3. [Installation](#installation)  
4. [Usage](#usage)  
   - [Admin Access](#admin-access)  
   - [User Access](#user-access)  
5. [File Structure](#file-structure)  
6. [Data Storage](#data-storage)  
7. [Contributing](#contributing)  
8. [License](#license)  
9. [Contact](#contact)  

---

## Features

### Admin Capabilities
- **Manage Users**:
  - Add new users with a unique ID, password, and name.
  - Remove users by their ID.
  - View a list of all users with their IDs, names, and join dates.
- **Manage Books**:
  - Add new books with a unique ID, title, author, and available count.
  - Remove books by their ID.
  - View a list of all books in the library.
- **View Borrowed Books**:
  - Access a detailed history of all borrowed books, including user names, book titles, borrow dates, due dates, and return status.

### User Capabilities
- **Search Available Books**:
  - Search for books by title or author, or list all available books.
- **Borrow Books**:
  - Borrow a book by entering its ID, with checks for availability and prevention of duplicate borrows.
- **View Borrowed Books**:
  - See a list of your currently borrowed books with their due dates.
- **Return Books**:
  - Return a borrowed book, updating its availability in the system.

### Additional Features
- **Persistent Storage**: Data is saved in text files (`users.txt`, `books.txt`, `borrows.txt`) and reloaded on startup.
- **User Authentication**: Secure login system for both admins and users.
- **Error Handling**: Robust input validation and clear error messages for file operations and user actions.
- **Dynamic Due Dates**: Books are borrowed for 7 days, with dates automatically calculated.

---

## Prerequisites

- **Python 3.x**: Ensure Python 3 is installed. Download it from [python.org](https://www.python.org/downloads/) if needed.

No external libraries are required—just the Python standard library!

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/library-management-system.git
   ```
2. Navigate to the project directory:
   ```bash
   cd library-management-system
   ```

---

## Usage

1. Run the program:
   ```bash
   python Library.py
   ```
2. The system displays a welcome message with statistics (total users, books, and borrows) and prompts for login credentials.

### Admin Access
- **Username**: `admin`
- **Password**: `admin`

The admin menu provides:
```
Welcome admin
1. Manage users
2. Manage books
3. See borrowed books
0. Log out
```

- **Manage Users**:
  - **Add**: Enter a unique user ID, password, and name.
  - **Remove**: Enter the user ID to delete.
  - **Show**: View all users with their IDs, names, and join dates.
- **Manage Books**:
  - **Add**: Enter a unique book ID, title, author, and available count.
  - **Remove**: Enter the book ID to delete.
  - **Show**: View all books with IDs, titles, authors, and counts.
- **See Borrowed Books**: Displays a history of all borrows with user and book details.

### User Access
- Log in with a user ID and password (created by the admin).
- The user menu provides:
```
Welcome [Your Name]
1. Search available books
2. Borrow book
3. See borrowed books
4. Return book
0. Log out
```

- **Search Available Books**: Enter a title or author (or leave blank for all available books).
- **Borrow Book**: Enter a book ID to borrow (if available and not already borrowed by you).
- **See Borrowed Books**: View your current borrows with due dates.
- **Return Book**: Select a book from your borrows to return.

---

## File Structure

- **`models.py`**: Defines the core classes:
  - `User`: Stores user ID, password, name, and join date.
  - `Book`: Stores book ID, title, author, available count, and add date.
  - `Borrow`: Stores borrow ID, user ID, book ID, borrow date, due date, and return status.
- **`globals.py`**: Contains global lists (`users_list`, `book_list`, `borrows_list`) for in-memory data.
- **`fileManager.py`**: Handles file operations:
  - Creates text files if they don’t exist.
  - Loads and counts data from `users.txt`, `books.txt`, and `borrows.txt`.
- **`Library.py`**: The main application file with:
  - Admin and user menus.
  - Functions for managing users, books, borrowing, and returning.

---

## Data Storage

Data is stored in three text files, automatically created and updated:
- **`users.txt`**: Format: `userId,password,name,dateJoined`
- **`books.txt`**: Format: `bookId,title,author,availableCount,dateAdded`
- **`borrows.txt`**: Format: `borrowId,userId,bookId,borrowDate,dueDate,isBookReturned`

Example entries:
```
# users.txt
u1,pass123,John Doe,2023-10-15 12:00:00

# books.txt
b1,The Great Gatsby,F. Scott Fitzgerald,2,2023-10-15 12:00:00

# borrows.txt
u1-b1,u1,b1,2023-10-15 12:00:00,2023-10-22,False
```

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a clear description of your changes.

Please report issues via the GitHub Issues tab.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

For questions or feedback, reach out at [your email or contact info].

---

Enjoy managing your library with this system! Star the repo if you find it useful! 🌟