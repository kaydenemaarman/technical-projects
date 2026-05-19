"""
Shelf Track Program
-------------------
This program is used by a bookstore clerk to manage book inventory.

Functionality:
- Add new books
- Update author information for a book
- Delete books
- Search for books
- View details of all books (title, author name, country)

Database:
- SQLite database: ebookstore.db
- Tables: book, author
"""

import sqlite3


# =================================================
# DATABASE HELPER FUNCTIONS
# =================================================

def get_connection():
    """
    Create and return a connection to the SQLite database.
    Using a function improves modularity and maintainability.
    """
    return sqlite3.connect("ebookstore.db")


def validate_four_digit_id(value, field_name):
    """
    Validate that the given value is a 4-digit numeric ID.
    Raises ValueError if validation fails.
    """
    if not value.isdigit() or len(value) != 4:
        raise ValueError(f"{field_name} must be exactly 4 digits.")
    return int(value)


def create_tables(cursor):
    """
    Create the book and author tables if they do not already exist.
    """

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS author (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            authorID INTEGER NOT NULL,
            qty INTEGER NOT NULL,
            FOREIGN KEY (authorID) REFERENCES author(id)
        )
    """)


def populate_tables(cursor):
    """
    Populate the database with initial author and book data.
    INSERT OR IGNORE prevents duplicate entries.
    """

    authors = [
        (1290, "Charles Dickens", "England"),
        (8937, "J.K. Rowling", "England"),
        (2356, "C.S. Lewis", "Ireland"),
        (6380, "J.R.R. Tolkien", "South Africa"),
        (5620, "Lewis Carroll", "England"),
        (4562, "The Brothers Grimm", "Germany"),
        (7854, "Joseph Jacobs", "England"),
        (1254, "Charles Perrault", "France")
    ]

    books = [
        (3001, "A Tale of Two Cities", 1290, 30),
        (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
        (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
        (3004, "The Lord of the Rings", 6380, 37),
        (3005, "Alice's Adventures in Wonderland", 5620, 12),
        (3006, "Rapunzel", 4562, 20),
        (3007, "The Three Little Pigs", 7854, 16),
        (3008, "Little Red Riding Hood", 1254, 5)
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO author VALUES (?, ?, ?)",
        authors
    )

    cursor.executemany(
        "INSERT OR IGNORE INTO book VALUES (?, ?, ?, ?)",
        books
    )


# =================================================
# DATABASE INITIALISATION
# =================================================

print("Welcome to The Cozy Chapter!")

with get_connection() as db:
    cursor = db.cursor()
    create_tables(cursor)
    populate_tables(cursor)


# =================================================
# MENU FUNCTIONS
# =================================================

def enter_book():
    """
    Add a new book to the database with validated input.
    """
    try:
        book_id = validate_four_digit_id(
            input("Enter 4-digit book ID: "), "Book ID"
        )
        title = input("Enter book title: ").strip()
        author_id = validate_four_digit_id(
            input("Enter 4-digit author ID: "), "Author ID"
        )
        qty = int(input("Enter quantity: "))

        cursor.execute(
            "INSERT INTO book VALUES (?, ?, ?, ?)",
            (book_id, title, author_id, qty)
        )
        db.commit()
        print("Book added successfully.\n")

    except ValueError as error:
        print(f"Input error: {error}\n")

    except sqlite3.IntegrityError:
        print("Error: Book ID already exists or author does not exist.\n")


def update_book():
    """
    Update the author name and/or country for a selected book.
    Uses INNER JOIN to retrieve related data.
    """
    try:
        book_id = validate_four_digit_id(
            input("Enter the 4-digit book ID to update: "), "Book ID"
        )

        cursor.execute("""
            SELECT book.title, author.id, author.name, author.country
            FROM book
            INNER JOIN author ON book.authorid = author.id
            WHERE book.id = ?
        """, (book_id,))

        record = cursor.fetchone()

        if not record:
            print("Book not found.\n")
            return

        title, author_id, name, country = record

        print("\nCurrent Details")
        print(f"Title: {title}")
        print(f"Author Name: {name}")
        print(f"Author Country: {country}")

        new_name = input("New author name (press Enter to keep current): ")
        new_country = input("New author country (press Enter to keep current): ")

        new_name = new_name if new_name else name
        new_country = new_country if new_country else country

        cursor.execute("""
            UPDATE author
            SET name = ?, country = ?
            WHERE id = ?
        """, (new_name, new_country, author_id))

        db.commit()
        print("Author details updated successfully.\n")

    except ValueError as error:
        print(f"Input error: {error}\n")


def delete_book():
    """
    Delete a book from the database using its ID.
    """
    try:
        book_id = validate_four_digit_id(
            input("Enter the 4-digit book ID to delete: "), "Book ID"
        )

        cursor.execute("DELETE FROM book WHERE id = ?", (book_id,))
        db.commit()

        if cursor.rowcount == 0:
            print("No book found with that ID.\n")
        else:
            print("Book deleted successfully.\n")

    except ValueError as error:
        print(f"Input error: {error}\n")


def search_book():
    """
    Search for books by title keyword.
    """
    keyword = input("Enter title keyword to search: ")

    cursor.execute(
        "SELECT * FROM book WHERE title LIKE ?",
        (f"%{keyword}%",)
    )

    results = cursor.fetchall()

    if not results:
        print("No matching books found.\n")
    else:
        print("\nSearch Results:")
        for book in results:
            print(book)
        print()


def view_book_details():
    """
    Displays book title, author name, and author country
    in a user-friendly format.
    Demonstrates the use of zip().
    """

    # Fetch book titles and author IDs
    cursor.execute("SELECT title, authorID FROM book")
    books = cursor.fetchall()

    # Fetch author details
    cursor.execute("SELECT id, name, country FROM author")
    authors = cursor.fetchall()

    # Convert authors list to a dictionary for quick lookup
    author_dict = {author_id: (name, country) for author_id, name, country in authors}

    print("\nDetails")
    print("-" * 50)

    # Use zip() to iterate over titles and author IDs together
    titles = [book[0] for book in books]
    author_ids = [book[1] for book in books]

    for title, author_id in zip(titles, author_ids):
        if author_id in author_dict:
            name, country = author_dict[author_id]

            print(f"Title: {title}")
            print(f"Author's Name: {name}")
            print(f"Author's Country: {country}")
            print("-" * 50)


# =================================================
# MAIN MENU
# =================================================

def main_menu():
    """
    Display the main menu and handle user choices.
    """
    while True:
        print("\n--- Menu ---")
        print("1. Enter book")
        print("2. Update book")
        print("3. Delete book")
        print("4. Search books")
        print("5. View details of all books")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            enter_book()
        elif choice == "2":
            update_book()
        elif choice == "3":
            delete_book()
        elif choice == "4":
            search_book()
        elif choice == "5":
            view_book_details()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


# =================================================
# PROGRAM ENTRY POINT
# =================================================

if __name__ == "__main__":
    try:
        main_menu()
    except Exception as error:
        print(f"An error occurred: {error}")


# References:
# Python Official Documentation: https://docs.python.org/3/library/functions.html#zip