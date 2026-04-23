import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import csv

# Connect to SQLite Database (if exists, else creates it)
conn = sqlite3.connect('university_department.db')
cursor = conn.cursor()

# Create necessary tables if they don't exist
def create_tables():
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        roll_number INTEGER PRIMARY KEY,
                        name TEXT,
                        address TEXT,
                        course_registered TEXT,
                        completed_courses TEXT,
                        backlogs TEXT,
                        semester_grades TEXT,
                        cgpa REAL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS department_inventory (
                        item_name TEXT,
                        item_type TEXT,
                        location TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS department_accounts (
                        income REAL,
                        expenditure REAL,
                        balance REAL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS research_projects (
                        project_name TEXT,
                        faculty_incharge TEXT,
                        details TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS publications (
                        faculty_name TEXT,
                        publication_title TEXT,
                        journal_name TEXT)''')
    
    conn.commit()

# Function to insert a student
def add_student(roll_number, name, address, course_registered):
    cursor.execute('''INSERT INTO students (roll_number, name, address, course_registered)
                      VALUES (?, ?, ?, ?)''', (roll_number, name, address, course_registered))
    conn.commit()
    messagebox.showinfo("Success", "Student added successfully!")

# Function to update student registration details
def update_student_registration(roll_number, completed_courses, backlogs):
    cursor.execute('''UPDATE students SET completed_courses=?, backlogs=? WHERE roll_number=?''',
                   (completed_courses, backlogs, roll_number))
    conn.commit()
    messagebox.showinfo("Success", "Student registration updated successfully!")

# Function to update grades and calculate GPA and CGPA
def update_grades(roll_number, grades):
    cursor.execute('''UPDATE students SET semester_grades=? WHERE roll_number=?''',
                   (grades, roll_number))
    
    # Calculate GPA for the semester
    cursor.execute('''SELECT semester_grades FROM students WHERE roll_number=?''', (roll_number,))
    grades_data = cursor.fetchone()
    grade_list = list(map(int, grades_data[0].split(',')))  # Split grades by commas and convert to integers
    gpa = sum(grade_list) / len(grade_list)  # Calculate GPA for the semester
    
    # Update the semester GPA
    cursor.execute('''UPDATE students SET cgpa=? WHERE roll_number=?''', (gpa, roll_number))
    conn.commit()
    messagebox.showinfo("Success", f"Semester grades updated! Semester GPA: {gpa}")

# Function to add inventory items
def add_inventory(item_name, item_type, location):
    cursor.execute('''INSERT INTO department_inventory (item_name, item_type, location)
                      VALUES (?, ?, ?)''', (item_name, item_type, location))
    conn.commit()
    messagebox.showinfo("Success", "Inventory item added successfully!")

# Function to update department accounts
def update_account(income, expenditure):
    cursor.execute('''SELECT * FROM department_accounts''')
    account_data = cursor.fetchone()
    if account_data:
        new_income = account_data[0] + income
        new_expenditure = account_data[1] + expenditure
        new_balance = new_income - new_expenditure
        cursor.execute('''UPDATE department_accounts SET income=?, expenditure=?, balance=?
                        WHERE rowid=1''', (new_income, new_expenditure, new_balance))
    else:
        balance = income - expenditure
        cursor.execute('''INSERT INTO department_accounts (income, expenditure, balance)
                          VALUES (?, ?, ?)''', (income, expenditure, balance))
    
    conn.commit()
    messagebox.showinfo("Success", "Department accounts updated successfully!")

# Function to add research project details
def add_research_project(project_name, faculty_incharge, details):
    cursor.execute('''INSERT INTO research_projects (project_name, faculty_incharge, details)
                      VALUES (?, ?, ?)''', (project_name, faculty_incharge, details))
    conn.commit()
    messagebox.showinfo("Success", "Research project added successfully!")

# Function to add publication details
def add_publication(faculty_name, publication_title, journal_name):
    cursor.execute('''INSERT INTO publications (faculty_name, publication_title, journal_name)
                      VALUES (?, ?, ?)''', (faculty_name, publication_title, journal_name))
    conn.commit()
    messagebox.showinfo("Success", "Publication added successfully!")

# Function to query and display student details
def query_student(roll_number):
    cursor.execute('''SELECT * FROM students WHERE roll_number=?''', (roll_number,))
    student_data = cursor.fetchone()
    if student_data:
        messagebox.showinfo("Student Details", f"Roll Number: {student_data[0]}\nName: {student_data[1]}\n"
                                              f"Address: {student_data[2]}\nCourse Registered: {student_data[3]}\n"
                                              f"Completed Courses: {student_data[4]}\nBacklogs: {student_data[5]}\n"
                                              f"Semester Grades: {student_data[6]}\nCGPA: {student_data[7]}")
    else:
        messagebox.showerror("Error", "Student not found!")

# Function to query and display department accounts
def query_department_accounts():
    cursor.execute('''SELECT * FROM department_accounts''')
    account_data = cursor.fetchone()
    if account_data:
        messagebox.showinfo("Department Accounts", f"Income: {account_data[0]}\nExpenditure: {account_data[1]}\n"
                                                 f"Balance: {account_data[2]}")
    else:
        messagebox.showerror("Error", "No account data found!")

# Function to import CSV data for students
def import_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:
                    cursor.execute('''INSERT INTO students (roll_number, name, address, course_registered)
                                      VALUES (?, ?, ?, ?)''', (int(row[0]), row[1], row[2], row[3]))
            conn.commit()
        messagebox.showinfo("Success", "Students imported from CSV successfully!")

# Function to export students to CSV
def export_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        cursor.execute('''SELECT * FROM students''')
        students = cursor.fetchall()
        with open(file_path, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Roll Number', 'Name', 'Address', 'Course Registered', 'Completed Courses', 
                             'Backlogs', 'Semester Grades', 'CGPA'])
            writer.writerows(students)
        messagebox.showinfo("Success", "Students exported to CSV successfully!")

# Initialize GUI
def main_gui():
    root = tk.Tk()
    root.title("University Department Information System")
    root.geometry("600x600")

    # Change font size globally
    default_font = ("Arial", 12)
    
    # Create frames
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # Add Student
    tk.Label(frame, text="Roll Number", font=default_font).grid(row=0, column=0)
    roll_number_entry = tk.Entry(frame, font=default_font)
    roll_number_entry.grid(row=0, column=1)
    
    tk.Label(frame, text="Name", font=default_font).grid(row=1, column=0)
    name_entry = tk.Entry(frame, font=default_font)
    name_entry.grid(row=1, column=1)
    
    tk.Label(frame, text="Address", font=default_font).grid(row=2, column=0)
    address_entry = tk.Entry(frame, font=default_font)
    address_entry.grid(row=2, column=1)
    
    tk.Label(frame, text="Course Registered", font=default_font).grid(row=3, column=0)
    course_entry = tk.Entry(frame, font=default_font)
    course_entry.grid(row=3, column=1)
    
    def add_student_button():
        roll_number = int(roll_number_entry.get())
        name = name_entry.get()
        address = address_entry.get()
        course = course_entry.get()
        add_student(roll_number, name, address, course)
    
    add_student_btn = tk.Button(frame, text="Add Student", font=default_font, command=add_student_button)
    add_student_btn.grid(row=4, column=0, columnspan=2)

    # Query Student
    def query_student_button():
        roll_number = int(roll_number_entry.get())
        query_student(roll_number)
    
    query_student_btn = tk.Button(frame, text="Query Student", font=default_font, command=query_student_button)
    query_student_btn.grid(row=5, column=0, columnspan=2)

    # Query Department Accounts
    def query_accounts_button():
        query_department_accounts()

    query_accounts_btn = tk.Button(frame, text="Query Department Accounts", font=default_font, command=query_accounts_button)
    query_accounts_btn.grid(row=6, column=0, columnspan=2)

    # Import/Export CSV
    import_csv_btn = tk.Button(frame, text="Import CSV", font=default_font, command=import_csv)
    import_csv_btn.grid(row=7, column=0, columnspan=2)

    export_csv_btn = tk.Button(frame, text="Export CSV", font=default_font, command=export_csv)
    export_csv_btn.grid(row=8, column=0, columnspan=2)

    # Run the application
    create_tables()
    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    main_gui()
