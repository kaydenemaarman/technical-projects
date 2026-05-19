"""
This code performs various SQLite operations using Python.
It connects to or creates a database file, creates a table,
inserts multiple records, retrieves and updates data, and
deletes a record.
"""

import sqlite3

# Connect to or create a SQLite database file
db = sqlite3.connect('programmers_db.db')

# Get a cursor object to interact with the database
cursor = db.cursor()

# Create the python_programming table if it does not exist
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS python_programming (
        id INTEGER PRIMARY KEY,
        name TEXT,
        grade INTEGER
    )
    '''
)

# Commit the changes to save the table creation
db.commit()

# Define data for programmers
programmers_data = [
    (55, 'Carl Davis', 61),
    (66, 'Dennis Fredrickson', 88),
    (77, 'Jane Richards', 78),
    (12, 'Peyton Sawyer', 45),
    (2, 'Lucas Brooke', 99)
]

# Insert multiple programmers into the table
cursor.executemany(
    '''
    INSERT INTO python_programming(id, name, grade)
    VALUES(?, ?, ?)
    ''',
    programmers_data
)
print('Multiple programmers inserted.\n')

# Commit the changes to save the inserted data
db.commit()

# Select all records with a grade between 60 and 80
cursor.execute('''SELECT * FROM python_programming WHERE grade BETWEEN ? AND ?''', (60, 80))

# Fetch all matching records
records = cursor.fetchall()

print('Programmers with grades between 60 and 80:')
for record in records:
    print(record)

# Update Carl Davis
cursor.execute('''UPDATE python_programming SET grade = ? WHERE name = ?''', (65, 'Carl Davis'))

# Commit the changes to save the updated data
db.commit()

print("Carl Davis's grade updated.\n")

# Delete Dennis Fredrickson
cursor.execute('''DELETE FROM python_programming WHERE name = ?''', ('Dennis Fredrickson',))

# Commit the changes to save the deletion
db.commit()

print("Dennis Fredrickson deleted from the database.\n")

# Update grades for programmers with id greater than 55
cursor.execute('''UPDATE python_programming SET grade = ? WHERE id > ?''', (80, 55))

# Commit the changes to save the updated data
db.commit()

print("Grades updated for programmers with id greater than 55.\n")

# Close the database connection
db.close()
