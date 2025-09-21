
# Library Management System

This documentation describes a Python application for managing a library system. 
The application uses SQLite to handle book and member data and includes the following features:

## Features

1. **Book Management**: Add, remove, and lend/return books.
2. **Member Management**: Add, remove, and display member information.
3. **Database Management**: Save book and member data using JSON files.

## Classes and Methods

### `readDatabase()`
Reads and returns the database. Returns `False` if the file is missing.

### `Book`
Stores book details:
- `name`: Book name
- `author`: Author name
- `year`: Publication year
- `publisher`: Publisher

### `Member`
Stores member details:
- `name`: Member name
- `phoneNumber`: Phone number
- `email`: Email address
- `address`: Address

### `Library`
Main class for library management.

#### Methods:
- `addBook()`: Adds a new book.
- `removeBook(bookID)`: Removes a book.
- `addMember()`: Adds a new member.
- `deleteMember(MemberID)`: Deletes a member.
- `lendBook(MemberID, bookID)`: Lends a book.
- `returnBook(MemberID, bookID)`: Returns a book.
- `validate(object, id)`: Checks the existence of a book or member.

## Menu Options

- **0**: Book List
- **1**: Member List
- **2**: Add Book
- **3**: Remove Book
- **4**: Add Member
- **5**: Delete Member
- **6**: Lend Book
- **7**: Return Book
- **8**: Exit

### Example Usage
```python
library = Library()
library.addBook()
library.lendBook(1, 1001)
library.returnBook(1, 1001)
```

