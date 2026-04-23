import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime, timedelta
import sqlite3
import csv
import smtplib
from email.mime.text import MIMEText

def send_email_notification(member_email, subject, body):
    """
    Sends an email notification to the specified member.
    """
    sender_email = "your_email@example.com"
    sender_password = "your_password"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = member_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"Notification sent to {member_email}")
    except Exception as e:
        print(f"Error sending notification: {e}")

def notify_due_dates():
    """
    Notifies members about upcoming due dates for issued books.
    """
    cursor.execute("SELECT member_id, isbn, return_date FROM issued_books WHERE status = 'issued'")
    issued_books = cursor.fetchall()

    for book in issued_books:
        member_id, isbn, return_date = book
        due_date = datetime.strptime(return_date, "%Y-%m-%d")
        days_left = (due_date - datetime.now()).days

        if 0 <= days_left <= 3:  # Notify if the due date is within 3 days
            cursor.execute("SELECT name, email FROM members WHERE member_id = ?", (member_id,))
            member = cursor.fetchone()
            if member:
                name, email = member
                subject = "Library Book Due Reminder"
                body = f"Dear {name},\n\nYour borrowed book (ISBN: {isbn}) is due on {return_date}. Please return it on time to avoid penalties.\n\nThank you!"
                send_email_notification(email, subject, body)

def notify_penalties():
    """
    Notifies members about penalties incurred for overdue books.
    """
    cursor.execute("SELECT penalties.member_id, penalties.isbn, penalties.penalty_amount, members.email FROM penalties "
                   "JOIN members ON penalties.member_id = members.member_id")
    penalties = cursor.fetchall()

    for penalty in penalties:
        member_id, isbn, penalty_amount, email = penalty
        subject = "Overdue Book Penalty Notification"
        body = f"Dear Member,\n\nYou have incurred a penalty of ${penalty_amount} for the overdue book (ISBN: {isbn}). Please clear your dues.\n\nThank you!"
        send_email_notification(email, subject, body)

def notify_reserved_books():
    """
    Notifies members about the availability of reserved books.
    """
    cursor.execute("SELECT reserved_books.member_id, reserved_books.isbn, members.email FROM reserved_books "
                   "JOIN books ON reserved_books.isbn = books.isbn AND books.copies_available > 0 "
                   "JOIN members ON reserved_books.member_id = members.member_id")
    available_reservations = cursor.fetchall()

    for reservation in available_reservations:
        member_id, isbn, email = reservation
        subject = "Reserved Book Available"
        body = f"Dear Member,\n\nThe reserved book (ISBN: {isbn}) is now available for issue. Please visit the library to collect it.\n\nThank you!"
        send_email_notification(email, subject, body)

def browse_catalog(filter_by="title", keyword=""):
    """
    Allows members to browse the catalog with an optional filter.
    """
    query = f"SELECT isbn, title, author, copies_available FROM books WHERE {filter_by} LIKE ?"
    cursor.execute(query, (f"%{keyword}%",))
    return cursor.fetchall()

def reserve_from_catalog(isbn, member_id):
    """
    Allows members to reserve a book directly from the online catalog.
    """
    cursor.execute("SELECT copies_available FROM books WHERE isbn = ?", (isbn,))
    result = cursor.fetchone()
    if result[0] > 0:
        return "Book is available for issue; no need to reserve."
    else:
        cursor.execute("INSERT INTO reserved_books (isbn, member_id, reserved_date) VALUES (?, ?, ?)",
                       (isbn, member_id, datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        return "Book reserved successfully!"

def calculate_and_notify_penalties():
    """
    Automatically calculates penalties for overdue books and notifies members.
    """
    cursor.execute("SELECT * FROM issued_books WHERE status = 'issued'")
    issued_books = cursor.fetchall()
    penalty_rate = 0.5  # Penalty per overdue day

    for book in issued_books:
        isbn, member_id, issue_date, return_date, _ = book
        overdue_days = (datetime.now() - datetime.strptime(return_date, "%Y-%m-%d")).days
        if overdue_days > 0:
            penalty_amount = overdue_days * penalty_rate
            cursor.execute("INSERT OR IGNORE INTO penalties (isbn, member_id, overdue_days, penalty_amount) VALUES (?, ?, ?, ?)",
                           (isbn, member_id, overdue_days, penalty_amount))
            cursor.execute("SELECT email FROM members WHERE member_id = ?", (member_id,))
            member_email = cursor.fetchone()[0]
            if member_email:
                subject = "Penalty for Overdue Book"
                body = f"Dear Member,\n\nYou have incurred a penalty of ${penalty_amount} for the overdue book (ISBN: {isbn}). Please clear your dues at the earliest.\n\nThank you!"
                send_email_notification(member_email, subject, body)

    conn.commit()



# Initialize the database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create the tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS books (
    isbn TEXT PRIMARY KEY,
    title TEXT,
    author TEXT,
    rack_number TEXT,
    copies_available INTEGER,
    total_copies INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS issued_books (
    isbn TEXT,
    member_id INTEGER,
    issue_date DATE,
    return_date DATE,
    status TEXT,
    FOREIGN KEY(isbn) REFERENCES books(isbn),
    FOREIGN KEY(member_id) REFERENCES members(member_id)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS reserved_books (
    isbn TEXT,
    member_id INTEGER,
    reserved_date DATE,
    FOREIGN KEY(isbn) REFERENCES books(isbn),
    FOREIGN KEY(member_id) REFERENCES members(member_id)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS penalties (
    isbn TEXT,
    member_id INTEGER,
    overdue_days INTEGER,
    penalty_amount REAL,
    FOREIGN KEY(isbn) REFERENCES books(isbn),
    FOREIGN KEY(member_id) REFERENCES members(member_id)
)''')

conn.commit()

def toggle_dark_mode(root):
    """
    Toggles dark mode for the main application window and all child widgets.
    """
    root.configure(bg="black")
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            toggle_dark_mode(widget)  # Apply recursively to child windows
        else:
            widget.configure(bg="black", fg="white")
    messagebox.showinfo("Dark Mode", "Dark mode activated!")

def register_member(name, category):
    cursor.execute('INSERT INTO members (name, category) VALUES (?, ?)', (name, category))
    conn.commit()
    cursor.execute('SELECT member_id FROM members WHERE name = ? AND category = ? ORDER BY member_id DESC LIMIT 1', (name, category))
    member_id = cursor.fetchone()[0]
    return member_id


def create_member_gui():
   def create_member():
    name = name_entry.get()
    category = category_var.get()
    member_id = register_member(name, category)  # Capture the returned member ID
    messagebox.showinfo("Member Registration", f"Member registered successfully!\nMember ID: {member_id}")

    
    member_window = tk.Toplevel(root)
    member_window.title("Register Member")

    name_label = tk.Label(member_window, text="Name", font=("Arial", 12))
    name_label.pack()
    name_entry = tk.Entry(member_window, font=("Arial", 12))
    name_entry.pack()

    category_label = tk.Label(member_window, text="Category", font=("Arial", 12))
    category_label.pack()
    category_var = tk.StringVar()
    category_menu = tk.OptionMenu(member_window, category_var, "undergraduate", "postgraduate", "research", "faculty")
    category_menu.config(font=("Arial", 12))
    category_menu.pack()

    submit_button = tk.Button(member_window, text="Register", font=("Arial", 12), command=create_member)
    submit_button.pack()


# Helper functions
def add_book(isbn, title, author, rack_number, copies):
    cursor.execute('INSERT INTO books VALUES (?, ?, ?, ?, ?, ?)', (isbn, title, author, rack_number, copies, copies))
    conn.commit()



def issue_book(isbn, member_id):
    cursor.execute('SELECT copies_available FROM books WHERE isbn = ?', (isbn,))
    result = cursor.fetchone()
    if result[0] > 0:
        # Determine allowed books based on member category
        cursor.execute('SELECT category FROM members WHERE member_id = ?', (member_id,))
        category = cursor.fetchone()[0]

        max_books = {'undergraduate': 2, 'postgraduate': 4, 'research': 6, 'faculty': 10}
        issue_duration = {'undergraduate': 30, 'postgraduate': 30, 'research': 90, 'faculty': 180}

        # Issue the book
        cursor.execute('INSERT INTO issued_books (isbn, member_id, issue_date, return_date, status) VALUES (?, ?, ?, ?, ?)',
                       (isbn, member_id, datetime.now().strftime('%Y-%m-%d'), (datetime.now() + timedelta(days=issue_duration[category])).strftime('%Y-%m-%d'), 'issued'))
        
        cursor.execute('UPDATE books SET copies_available = copies_available - 1 WHERE isbn = ?', (isbn,))
        conn.commit()
        messagebox.showinfo("Success", "Book issued successfully!")
    else:
        messagebox.showwarning("Unavailable", "Book is not available for issue.")

def return_book(isbn, member_id):
    cursor.execute('SELECT return_date FROM issued_books WHERE isbn = ? AND member_id = ? AND status = "issued"', (isbn, member_id))
    result = cursor.fetchone()
    if result:
        return_date = datetime.strptime(result[0], '%Y-%m-%d')
        overdue_days = (datetime.now() - return_date).days
        if overdue_days > 0:
            penalty_rate = 0.5  # Example penalty rate per day
            penalty_amount = overdue_days * penalty_rate
            cursor.execute('INSERT INTO penalties (isbn, member_id, overdue_days, penalty_amount) VALUES (?, ?, ?, ?)',
                           (isbn, member_id, overdue_days, penalty_amount))
            conn.commit()
            messagebox.showinfo("Penalty", f"Penalty charge: ${penalty_amount}")
        
        cursor.execute('UPDATE books SET copies_available = copies_available + 1 WHERE isbn = ?', (isbn,))
        cursor.execute('UPDATE issued_books SET status = "returned" WHERE isbn = ? AND member_id = ? AND status = "issued"', (isbn, member_id))
        conn.commit()
        messagebox.showinfo("Success", "Book returned successfully!")
    else:
        messagebox.showwarning("Error", "This book is not issued to you.")

def check_availability(isbn):
    cursor.execute('SELECT title, rack_number, copies_available FROM books WHERE isbn = ?', (isbn,))
    result = cursor.fetchone()
    if result:
        messagebox.showinfo("Availability", f"Book: {result[0]}\nRack: {result[1]}\nAvailable copies: {result[2]}")
    else:
        messagebox.showwarning("Not Found", "Book not found.")

def reserve_book(isbn, member_id):
    cursor.execute('SELECT copies_available FROM books WHERE isbn = ?', (isbn,))
    result = cursor.fetchone()
    if result[0] > 0:
        messagebox.showwarning("Unavailable", "Book is available for issue. No need to reserve.")
    else:
        cursor.execute('INSERT INTO reserved_books (isbn, member_id, reserved_date) VALUES (?, ?, ?)',
                       (isbn, member_id, datetime.now().strftime('%Y-%m-%d')))
        conn.commit()
        messagebox.showinfo("Reserved", "Book reserved successfully!")

def import_books_from_csv():
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if filepath:
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # Avoid empty rows
                    try:
                        isbn, title, author, rack_number, copies = row
                        add_book(isbn, title, author, rack_number, int(copies))
                    except Exception as e:
                        messagebox.showwarning("CSV Error", f"Error importing row: {row}. {e}")
        messagebox.showinfo("Success", "Books imported successfully!")

# GUI Functions
def create_member_gui():
    def create_member():
        name = name_entry.get()
        category = category_var.get()
        register_member(name, category)
        messagebox.showinfo("Member Registration", "Member registered successfully!")
    
    member_window = tk.Toplevel(root)
    member_window.title("Register Member")

    name_label = tk.Label(member_window, text="Name", font=("Arial", 12))
    name_label.pack()
    name_entry = tk.Entry(member_window, font=("Arial", 12))
    name_entry.pack()

    category_label = tk.Label(member_window, text="Category", font=("Arial", 12))
    category_label.pack()
    category_var = tk.StringVar()
    category_menu = tk.OptionMenu(member_window, category_var, "undergraduate", "postgraduate", "research", "faculty")
    category_menu.config(font=("Arial", 12))
    category_menu.pack()

    submit_button = tk.Button(member_window, text="Register", font=("Arial", 12), command=create_member)
    submit_button.pack()

def add_book_gui():
    def add_new_book():
        isbn = isbn_entry.get()
        title = title_entry.get()
        author = author_entry.get()
        rack_number = rack_entry.get()
        copies = int(copies_entry.get())
        add_book(isbn, title, author, rack_number, copies)
        messagebox.showinfo("Add Book", "Book added successfully!")
    
    book_window = tk.Toplevel(root)
    book_window.title("Add New Book")

    isbn_label = tk.Label(book_window, text="ISBN", font=("Arial", 12))
    isbn_label.pack()
    isbn_entry = tk.Entry(book_window, font=("Arial", 12))
    isbn_entry.pack()

    title_label = tk.Label(book_window, text="Title", font=("Arial", 12))
    title_label.pack()
    title_entry = tk.Entry(book_window, font=("Arial", 12))
    title_entry.pack()

    author_label = tk.Label(book_window, text="Author", font=("Arial", 12))
    author_label.pack()
    author_entry = tk.Entry(book_window, font=("Arial", 12))
    author_entry.pack()

    rack_label = tk.Label(book_window, text="Rack Number", font=("Arial", 12))
    rack_label.pack()
    rack_entry = tk.Entry(book_window, font=("Arial", 12))
    rack_entry.pack()

    copies_label = tk.Label(book_window, text="Total Copies", font=("Arial", 12))
    copies_label.pack()
    copies_entry = tk.Entry(book_window, font=("Arial", 12))
    copies_entry.pack()

    add_button = tk.Button(book_window, text="Add Book", font=("Arial", 12), command=add_new_book)
    add_button.pack()

def issue_book_gui():
    def issue_book_action():
        isbn = isbn_entry.get()
        member_id = int(member_id_entry.get())
        issue_book(isbn, member_id)
    
    issue_window = tk.Toplevel(root)
    issue_window.title("Issue Book")

    isbn_label = tk.Label(issue_window, text="ISBN", font=("Arial", 12))
    isbn_label.pack()
    isbn_entry = tk.Entry(issue_window, font=("Arial", 12))
    isbn_entry.pack()

    member_id_label = tk.Label(issue_window, text="Member ID", font=("Arial", 12))
    member_id_label.pack()
    member_id_entry = tk.Entry(issue_window, font=("Arial", 12))
    member_id_entry.pack()

    issue_button = tk.Button(issue_window, text="Issue Book", font=("Arial", 12), command=issue_book_action)
    issue_button.pack()

def return_book_gui():
    def return_book_action():
        isbn = isbn_entry.get()
        member_id = int(member_id_entry.get())
        return_book(isbn, member_id)
    
    return_window = tk.Toplevel(root)
    return_window.title("Return Book")

    isbn_label = tk.Label(return_window, text="ISBN", font=("Arial", 12))
    isbn_label.pack()
    isbn_entry = tk.Entry(return_window, font=("Arial", 12))
    isbn_entry.pack()

    member_id_label = tk.Label(return_window, text="Member ID", font=("Arial", 12))
    member_id_label.pack()
    member_id_entry = tk.Entry(return_window, font=("Arial", 12))
    member_id_entry.pack()

    return_button = tk.Button(return_window, text="Return Book", font=("Arial", 12), command=return_book_action)
    return_button.pack()

def check_availability_gui():
    def check_availability_action():
        isbn = isbn_entry.get()
        check_availability(isbn)
    
    availability_window = tk.Toplevel(root)
    availability_window.title("Check Availability")

    isbn_label = tk.Label(availability_window, text="ISBN", font=("Arial", 12))
    isbn_label.pack()
    isbn_entry = tk.Entry(availability_window, font=("Arial", 12))
    isbn_entry.pack()

    check_button = tk.Button(availability_window, text="Check Availability", font=("Arial", 12), command=check_availability_action)
    check_button.pack()

def reserve_book_gui():
    def reserve_book_action():
        isbn = isbn_entry.get()
        member_id = int(member_id_entry.get())
        reserve_book(isbn, member_id)
    
    reserve_window = tk.Toplevel(root)
    reserve_window.title("Reserve Book")

    isbn_label = tk.Label(reserve_window, text="ISBN", font=("Arial", 12))
    isbn_label.pack()
    isbn_entry = tk.Entry(reserve_window, font=("Arial", 12))
    isbn_entry.pack()

    member_id_label = tk.Label(reserve_window, text="Member ID", font=("Arial", 12))
    member_id_label.pack()
    member_id_entry = tk.Entry(reserve_window, font=("Arial", 12))
    member_id_entry.pack()

    reserve_button = tk.Button(reserve_window, text="Reserve Book", font=("Arial", 12), command=reserve_book_action)
    reserve_button.pack()

# Main GUI setup
root = tk.Tk()
root.title("Library Information System")

# Main Menu
menu = tk.Menu(root)

# Book Management
book_menu = tk.Menu(menu, tearoff=0)
book_menu.add_command(label="Add Book", font=("Arial", 12), command=add_book_gui)
book_menu.add_command(label="Issue Book", font=("Arial", 12), command=issue_book_gui)
book_menu.add_command(label="Return Book", font=("Arial", 12), command=return_book_gui)
book_menu.add_command(label="Check Availability", font=("Arial", 12), command=check_availability_gui)
book_menu.add_command(label="Reserve Book", font=("Arial", 12), command=reserve_book_gui)
book_menu.add_command(label="Import Books from CSV", font=("Arial", 12), command=import_books_from_csv)
menu.add_cascade(label="Books", menu=book_menu)

# Member Management
member_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Members", menu=member_menu)
member_menu.add_command(label="Register Member", font=("Arial", 12), command=create_member_gui)


root.config(menu=menu)

root.mainloop()

conn.close()
