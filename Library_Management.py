import tkinter as tk
from tkinter import messagebox, Toplevel
from datetime import datetime, timedelta
import sqlite3

# Database connection
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create or modify tables to ensure all columns exist
# If the column "rack" doesn't exist, we add it.
cursor.execute('''PRAGMA foreign_keys=off;''')  # Disable foreign keys temporarily to allow modification

cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                    isbn TEXT PRIMARY KEY,
                    title TEXT,
                    author TEXT,
                    rack TEXT,
                    copies INTEGER,
                    available_copies INTEGER,
                    publisher TEXT,
                    publication_year INTEGER,
                    publication_date TEXT
                )''')

# Enable foreign keys again after the changes
cursor.execute('''PRAGMA foreign_keys=on;''')

cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    category TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS issued_books (
                    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    isbn TEXT,
                    member_id INTEGER,
                    issue_date TEXT,
                    return_date TEXT,
                    status TEXT
                )''')

# Commit the changes to ensure tables are created
conn.commit()

# Global variables for entry fields
isbn_entry, title_entry, author_entry, rack_entry, copies_entry = None, None, None, None, None
member_id_entry = None

import csv

def export_data_to_csv():
    try:
        cursor.execute(''' 
            SELECT books.isbn, books.title, books.author, books.rack, books.publisher, books.copies, 
                   books.available_copies, books.publication_date 
            FROM books
        ''')
        books = cursor.fetchall()

        # Open a CSV file in write mode
        with open('library_books_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            # Write the header row
            writer.writerow(["ISBN", "Title", "Author", "Rack", "Publisher", "Copies", "Available Copies", "Publication Date"])
            
            # Write book data
            for book in books:
                writer.writerow(book)

        messagebox.showinfo("Success", "Data has been successfully exported to 'library_books_data.csv'")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while exporting data: {e}")

# Register Member GUI
def create_member_gui():
    def create_member():
        name = name_entry.get()
        category = category_var.get()
        if not name or not category:
            messagebox.showerror("Error", "All fields are required!")
            return
        cursor.execute('INSERT INTO members (name, category) VALUES (?, ?)', (name, category))
        conn.commit()
        member_id = cursor.lastrowid
        messagebox.showinfo("Success", f"Member registered successfully!\nMember ID: {member_id}")
        member_window.destroy()

    member_window = Toplevel(root)
    member_window.title("Register Member")
    tk.Label(member_window, text="Name", font=("Helvetica", 14) ).pack(pady=5)
    name_entry = tk.Entry(member_window, font=("Helvetica", 12))
    name_entry.pack(pady=5)
    tk.Label(member_window, text="Category", font=("Helvetica", 14) ).pack(pady=5)
    category_var = tk.StringVar(value="undergraduate")
    category_menu = tk.OptionMenu(member_window, category_var, "undergraduate", "postgraduate", "research", "faculty")
    category_menu.config(font=("Helvetica", 12), bg="#add8e6")
    category_menu.pack(pady=5)
    tk.Button(member_window, text="Register", font=("Helvetica", 12) , command=create_member).pack(pady=10)

# Function to ensure the publisher column is added
def add_publisher_column_if_missing():
    try:
        cursor.execute("PRAGMA foreign_keys=off;")  # Disable foreign keys temporarily
        
        # Check if the publisher column exists
        cursor.execute("PRAGMA table_info(books);")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'publisher' not in columns:
            # Add publisher column if it does not exist
            cursor.execute('''ALTER TABLE books ADD COLUMN publisher TEXT;''')
            conn.commit()
            print("Publisher column added successfully.")
        
        cursor.execute("PRAGMA foreign_keys=on;")  # Enable foreign keys again
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"An error occurred while modifying the database: {e}")

# Call the function to ensure the publisher column is added
add_publisher_column_if_missing()

def add_publication_date_column_if_missing():
    try:
        cursor.execute("PRAGMA foreign_keys=off;")  # Disable foreign keys temporarily
        
        # Check if the publication_date column exists
        cursor.execute("PRAGMA table_info(books);")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'publication_date' not in columns:
            # Add publication_date column if it does not exist
            cursor.execute('''ALTER TABLE books ADD COLUMN publication_date TEXT;''')
            conn.commit()
            print("Publication date column added successfully.")
        
        cursor.execute("PRAGMA foreign_keys=on;")  # Enable foreign keys again
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"An error occurred while modifying the database: {e}")

# Call the function to ensure the publication_date column is added
add_publication_date_column_if_missing()

def add_book_gui():
    def add_book():
        isbn = isbn_entry.get()
        title = title_entry.get()
        author = author_entry.get()
        rack = rack_entry.get()
        publisher = publisher_entry.get()  # New publisher entry field
        copies = copies_entry.get()
        pub_year = pub_year_entry.get()
        pub_month = pub_month_entry.get()
        pub_day = pub_day_entry.get()

        # Check for empty or invalid inputs
        if not (isbn and title and author and rack and publisher and copies.isdigit() and pub_year.isdigit() and pub_month.isdigit() and pub_day.isdigit()):
            messagebox.showerror("Error", "All fields must be filled with valid data!")
            return

        try:
            # Check if the book already exists
            cursor.execute('SELECT * FROM books WHERE isbn = ?', (isbn,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Book with this ISBN already exists!")
                return

            # Combine the year, month, and day into a single publication date
            publication_date = f"{pub_year}-{pub_month.zfill(2)}-{pub_day.zfill(2)}"

            # Insert the book into the database
            cursor.execute('INSERT INTO books (isbn, title, author, rack, publisher, copies, available_copies, publication_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                           (isbn, title, author, rack, publisher, int(copies), int(copies), publication_date))
            conn.commit()

            messagebox.showinfo("Success", "Book added successfully!")
            book_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    book_window = Toplevel(root)
    book_window.title("Add Book")
 

    tk.Label(book_window, text="ISBN", font=("Helvetica", 14) ).pack(pady=5)
    isbn_entry = tk.Entry(book_window, font=("Helvetica", 12))
    isbn_entry.pack(pady=5)

    tk.Label(book_window, text="Title", font=("Helvetica", 14) ).pack(pady=5)
    title_entry = tk.Entry(book_window, font=("Helvetica", 12))
    title_entry.pack(pady=5)

    tk.Label(book_window, text="Author", font=("Helvetica", 14) ).pack(pady=5)
    author_entry = tk.Entry(book_window, font=("Helvetica", 12))
    author_entry.pack(pady=5)

    tk.Label(book_window, text="Rack Number", font=("Helvetica", 14) ).pack(pady=5)
    rack_entry = tk.Entry(book_window, font=("Helvetica", 12))
    rack_entry.pack(pady=5)

    tk.Label(book_window, text="Publisher", font=("Helvetica", 14) ).pack(pady=5)
    publisher_entry = tk.Entry(book_window, font=("Helvetica", 12))  # New publisher entry field
    publisher_entry.pack(pady=5)

    tk.Label(book_window, text="Copies", font=("Helvetica", 14) ).pack(pady=5)
    copies_entry = tk.Entry(book_window, font=("Helvetica", 12))
    copies_entry.pack(pady=5)

    tk.Label(book_window, text="Publication Year", font=("Helvetica", 14) ).pack(pady=5)
    pub_year_entry = tk.Entry(book_window, font=("Helvetica", 12))
    pub_year_entry.pack(pady=5)

    tk.Label(book_window, text="Publication Month", font=("Helvetica", 14) ).pack(pady=5)
    pub_month_entry = tk.Entry(book_window, font=("Helvetica", 12))
    pub_month_entry.pack(pady=5)

    tk.Label(book_window, text="Publication Day", font=("Helvetica", 14) ).pack(pady=5)
    pub_day_entry = tk.Entry(book_window, font=("Helvetica", 12))
    pub_day_entry.pack(pady=5)

    tk.Button(book_window, text="Add Book", font=("Helvetica", 12) , command=add_book).pack(pady=10)

def issue_book_gui():
    def issue_book():
        isbn = isbn_entry.get()
        member_id = member_id_entry.get()

        if not isbn or not member_id:
            messagebox.showerror("Error", "ISBN and Member ID are required!")
            return

        try:
            cursor.execute('SELECT available_copies FROM books WHERE isbn = ?', (isbn,))
            book = cursor.fetchone()
            if not book:
                messagebox.showerror("Error", "Book not found!")
                return
            if book[0] <= 0:
                messagebox.showerror("Error", "Book not available!")
                return

            cursor.execute('SELECT * FROM members WHERE member_id = ?', (member_id,))
            member = cursor.fetchone()
            if not member:
                messagebox.showerror("Error", "Member not found!")
                return
            
            current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Store both date and time
            return_datetime = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')  # 30 days from now with time
            
            cursor.execute('INSERT INTO issued_books (isbn, member_id, issue_date, return_date, status) VALUES (?, ?, ?, ?, ?)',
                           (isbn, member_id, current_datetime, return_datetime, 'issued'))
            cursor.execute('UPDATE books SET available_copies = available_copies - 1 WHERE isbn = ?', (isbn,))
            conn.commit()
            messagebox.showinfo("Success", "Book issued successfully!")
            issue_window.destroy()  # Destroy the window

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    issue_window = Toplevel(root)  # Define issue_window here
    issue_window.title("Issue Book")

    # ISBN Entry
    tk.Label(issue_window, text="ISBN", font=("Helvetica", 14)).pack(pady=5)
    isbn_entry = tk.Entry(issue_window, font=("Helvetica", 12))
    isbn_entry.pack(pady=5)

    # Member ID Entry
    tk.Label(issue_window, text="Member ID", font=("Helvetica", 14)).pack(pady=5)
    member_id_entry = tk.Entry(issue_window, font=("Helvetica", 12))
    member_id_entry.pack(pady=5)

    # Button to issue the book
    tk.Button(issue_window, text="Issue Book", font=("Helvetica", 12), command=issue_book).pack(pady=10)

def return_book_gui():
    def return_book():
        isbn = isbn_entry.get()
        member_id = member_id_entry.get()

        if not isbn or not member_id:
            messagebox.showerror("Error", "ISBN and Member ID are required!")
            return

        try:
            cursor.execute('SELECT return_date FROM issued_books WHERE isbn = ? AND member_id = ? AND status = "issued"',
                           (isbn, member_id))
            issued = cursor.fetchone()
            if not issued:
                messagebox.showerror("Error", "This book is not issued to this member!")
                return

            return_datetime = datetime.strptime(issued[0], '%Y-%m-%d %H:%M:%S')
            overdue_days = (datetime.now() - return_datetime).days
            if overdue_days > 0:
                penalty = overdue_days * 0.5
                messagebox.showinfo("Overdue", f"Book is overdue by {overdue_days} days. Penalty: ${penalty}")
            
            current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Store current date and time
            
            cursor.execute('UPDATE issued_books SET status = "returned", return_date = ? WHERE isbn = ? AND member_id = ?',
                           (current_datetime, isbn, member_id))
            cursor.execute('UPDATE books SET available_copies = available_copies + 1 WHERE isbn = ?', (isbn,))
            conn.commit()
            messagebox.showinfo("Success", "Book returned successfully!")
            return_window.destroy()  # Destroy the window

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    return_window = Toplevel(root)  # Define return_window here
    return_window.title("Return Book")

    # ISBN Entry
    tk.Label(return_window, text="ISBN", font=("Helvetica", 14)).pack(pady=5)
    isbn_entry = tk.Entry(return_window, font=("Helvetica", 12))
    isbn_entry.pack(pady=5)

    # Member ID Entry
    tk.Label(return_window, text="Member ID", font=("Helvetica", 14)).pack(pady=5)
    member_id_entry = tk.Entry(return_window, font=("Helvetica", 12))
    member_id_entry.pack(pady=5)

    # Button to return the book
    tk.Button(return_window, text="Return Book", font=("Helvetica", 12), command=return_book).pack(pady=10)

import tkinter as tk
from tkinter import ttk
from datetime import datetime

def display_books_status():
    def update_book_list():
        # Retrieve the data for total books, available books, reserved books, and issue time
        cursor.execute(''' 
            SELECT books.title, books.author, books.copies, books.available_copies, 
                   (books.copies - books.available_copies) AS reserved, books.publication_date,
                   issued_books.issue_date
            FROM books
            LEFT JOIN issued_books ON books.isbn = issued_books.isbn AND issued_books.status = "issued"
        ''')
        books = cursor.fetchall()

        # Clear the table before displaying updated data
        for row in book_treeview.get_children():
            book_treeview.delete(row)
        
        # Insert book details into the treeview table
        for book in books:
            title, author, total_copies, available_copies, reserved_copies, publication_date, issue_date = book
            if issue_date:
                issue_time = datetime.strptime(issue_date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            else:
                issue_time = "Not Issued"

            # Add each row to the treeview
            book_treeview.insert("", "end", values=(title, author, total_copies, available_copies, reserved_copies, publication_date, issue_time))

    # Create a new window to display the book status
    status_window = Toplevel(root)
    status_window.title("Books Status")
    
    tk.Label(status_window, text="Books Status", font=("Helvetica", 16, 'bold')).pack(pady=10)

    # Treeview to display books' details in a table-like format
    columns = ("Title", "Author", "Total Copies", "Available Copies", "Reserved Copies", "Publication Date", "Issue Date")
    book_treeview = ttk.Treeview(status_window, columns=columns, show="headings", height=15)

    # Define the column headings
    for col in columns:
        book_treeview.heading(col, text=col)
        book_treeview.column(col, width=150)

    book_treeview.pack(pady=20)

    # Button to update the list of books
    tk.Button(status_window, text="Refresh", font=("Helvetica", 12), command=update_book_list).pack(pady=10)

    # Update the list initially
    update_book_list()



# Main Window
root = tk.Tk()
root.title("Library Management System")

tk.Button(root, text="Register Member", font=("Helvetica", 14), command=create_member_gui).pack(pady=10)
tk.Button(root, text="Add Book", font=("Helvetica", 14), command=add_book_gui).pack(pady=10)
tk.Button(root, text="Issue Book", font=("Helvetica", 14), command=issue_book_gui).pack(pady=10)
tk.Button(root, text="Return Book", font=("Helvetica", 14), command=return_book_gui).pack(pady=10)
tk.Button(root, text="View Books Status", font=("Helvetica", 14), command=display_books_status).pack(pady=10)
tk.Button(root, text="Exit", font=("Helvetica", 14), command=root.quit).pack(pady=10)
tk.Button(root, text="Export Data to CSV", font=("Helvetica", 14), command=export_data_to_csv).pack(pady=10)

root.mainloop()
