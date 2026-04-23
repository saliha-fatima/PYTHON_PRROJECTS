import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv

# Connect to SQLite Database
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

# Student Functions
def add_student(roll_number, name, address, course_registered, grades=None):
    # Ensure grades are a comma-separated string
    if grades:
        grades = ','.join(grades.split(','))  # Store as a comma-separated string
    cursor.execute('''INSERT INTO students (roll_number, name, address, course_registered, semester_grades)
                      VALUES (?, ?, ?, ?, ?)''', (roll_number, name, address, course_registered, grades))
    conn.commit()
    messagebox.showinfo("Success", "Student added successfully!")

def update_student_details(roll_number, new_name=None, new_address=None, new_course=None):
    if new_name:
        cursor.execute('''UPDATE students SET name=? WHERE roll_number=?''', (new_name, roll_number))
    if new_address:
        cursor.execute('''UPDATE students SET address=? WHERE roll_number=?''', (new_address, roll_number))
    if new_course:
        cursor.execute('''UPDATE students SET course_registered=? WHERE roll_number=?''', (new_course, roll_number))
    conn.commit()
    messagebox.showinfo("Success", "Student details updated successfully!")

def delete_student(roll_number):
    cursor.execute('''DELETE FROM students WHERE roll_number=?''', (roll_number,))
    conn.commit()
    messagebox.showinfo("Success", "Student deleted successfully!")

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

def view_all_students():
    cursor.execute('''SELECT * FROM students''')
    students = cursor.fetchall()
    if students:
        students_info = "\n".join([f"Roll Number: {student[0]}, Name: {student[1]}" for student in students])
        messagebox.showinfo("All Students", students_info)
    else:
        messagebox.showerror("Error", "No students found!")

def calculate_cgpa(grades):
    # Make sure grades are a list of numbers
    try:
        total_grades = sum(grades)
        cgpa = total_grades / len(grades)
        return round(cgpa, 2)  # Round to two decimal places
    except ZeroDivisionError:
        return 0  # Avoid division by zero if no grades are provided
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while calculating CGPA: {e}")
        return 0


def generate_cgpa_report():
    cursor.execute('''SELECT * FROM students''')
    students = cursor.fetchall()
    report = "CGPA Report:\n"
    for student in students:
        grades = student[6]  # Assuming semester grades are stored as a comma-separated string
        if grades:
            # Convert the comma-separated string into a list of float values
            grades_list = list(map(float, grades.split(',')))
            cgpa = calculate_cgpa(grades_list)
            report += f"Roll Number: {student[0]}, Name: {student[1]}, CGPA: {cgpa}\n"
        else:
            report += f"Roll Number: {student[0]}, Name: {student[1]}, CGPA: N/A\n"
    messagebox.showinfo("CGPA Report", report)

def add_inventory_item(item_name, item_type, location):
    cursor.execute('''INSERT INTO department_inventory (item_name, item_type, location)
                      VALUES (?, ?, ?)''', (item_name, item_type, location))
    conn.commit()
    messagebox.showinfo("Success", "Inventory item added successfully!")

# Inventory Functions
def delete_inventory_item(item_name):
    cursor.execute('''DELETE FROM department_inventory WHERE item_name=?''', (item_name,))
    conn.commit()
    messagebox.showinfo("Success", "Inventory item deleted successfully!")

# Accounts Functions
def update_account(income, expenditure):
    cursor.execute('''SELECT * FROM department_accounts''')
    account_data = cursor.fetchone()
    if account_data:
        new_income = account_data[0] + income
        new_expenditure = account_data[1] + expenditure
        new_balance = new_income - new_expenditure
        cursor.execute('''UPDATE department_accounts SET income=?, expenditure=?, balance=? WHERE rowid=1''',
                       (new_income, new_expenditure, new_balance))
    else:
        balance = income - expenditure
        cursor.execute('''INSERT INTO department_accounts (income, expenditure, balance) VALUES (?, ?, ?)''',
                       (income, expenditure, balance))
    conn.commit()
    messagebox.showinfo("Success", "Department accounts updated successfully!")

def generate_financial_report():
    cursor.execute('''SELECT * FROM department_accounts''')
    account_data = cursor.fetchone()
    if account_data:
        income, expenditure, balance = account_data
        report = f"Income: {income}\nExpenditure: {expenditure}\nBalance: {balance}"
        messagebox.showinfo("Financial Report", report)
    else:
        messagebox.showerror("Error", "No account data found!")

# Research Functions
def add_research_project(project_name, faculty_incharge, details):
    cursor.execute('''INSERT INTO research_projects (project_name, faculty_incharge, details)
                      VALUES (?, ?, ?)''', (project_name, faculty_incharge, details))
    conn.commit()
    messagebox.showinfo("Success", "Research project added successfully!")

# Publication Functions
def add_publication(faculty_name, publication_title, journal_name):
    cursor.execute('''INSERT INTO publications (faculty_name, publication_title, journal_name)
                      VALUES (?, ?, ?)''', (faculty_name, publication_title, journal_name))
    conn.commit()
    messagebox.showinfo("Success", "Publication added successfully!")

# CSV Functions
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

# Add scrollable frame functionality
class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

def main_gui():
    root = tk.Tk()
    root.title("University Department Information System")
    root.geometry("700x700")
    default_font = ("Arial", 10)

    # Add scrollable frame
    scrollable_container = ScrollableFrame(root)
    scrollable_container.pack(fill="both", expand=True, padx=10, pady=10)

    frame = scrollable_container.scrollable_frame

    # Section: Student Management
    student_label = ttk.Label(frame, text="Student Management", font=("Arial", 12, "bold"))
    student_label.grid(row=0, column=0, columnspan=2, pady=10)

    ttk.Label(frame, text="Roll Number:").grid(row=1, column=0, sticky="e", padx=5)
    roll_number_entry = ttk.Entry(frame)
    roll_number_entry.grid(row=1, column=1, sticky="w", padx=5)

    ttk.Label(frame, text="Name:").grid(row=2, column=0, sticky="e", padx=5)
    name_entry = ttk.Entry(frame)
    name_entry.grid(row=2, column=1, sticky="w", padx=5)

    ttk.Label(frame, text="Address:").grid(row=3, column=0, sticky="e", padx=5)
    address_entry = ttk.Entry(frame)
    address_entry.grid(row=3, column=1, sticky="w", padx=5)

    ttk.Label(frame, text="Course Registered:").grid(row=4, column=0, sticky="e", padx=5)
    course_entry = ttk.Entry(frame)
    course_entry.grid(row=4, column=1, sticky="w", padx=5)

    ttk.Label(frame, text="Grades (comma-separated):").grid(row=5, column=0, sticky="e", padx=5)
    grades_entry = ttk.Entry(frame)
    grades_entry.grid(row=5, column=1, sticky="w", padx=5)

    # Ensure the Add Student button is placed correctly
    ttk.Button(frame, text="Add Student", command=lambda: add_student(
        int(roll_number_entry.get()), name_entry.get(), address_entry.get(), course_entry.get(), grades_entry.get())
    ).grid(row=6, column=0, columnspan=2, pady=10)

    ttk.Button(frame, text="View All Students", command=view_all_students).grid(row=7, column=0, columnspan=2, pady=5)
    ttk.Button(frame, text="Query Student", command=lambda: query_student(int(roll_number_entry.get()))).grid(row=8, column=0, columnspan=2, pady=5)
    ttk.Button(frame, text="Generate CGPA Report", command=generate_cgpa_report).grid(row=9, column=0, columnspan=2, pady=5)
    ttk.Button(frame, text="Delete Student", command=lambda: delete_student(int(roll_number_entry.get()))).grid(row=10, column=0, columnspan=2, pady=5)

    # Section: Research Management
    research_label = ttk.Label(frame, text="Research Management", font=("Arial", 12, "bold"))
    research_label.grid(row=10, column=0, columnspan=2, pady=10)

    ttk.Label(frame, text="Project Name:").grid(row=11, column=0, sticky="e", padx=5)
    project_name_entry = ttk.Entry(frame)
    project_name_entry.grid(row=11, column=1, sticky="w", padx=5)

    ttk.Label(frame, text="Faculty Incharge:").grid(row=12, column=0, sticky="e", padx=5)
    faculty_entry = ttk.Entry(frame)
    faculty_entry.grid(row=12, column=1, sticky="w", padx=5)

    ttk.Label(frame, text="Details:").grid(row=13, column=0, sticky="e", padx=5)
    details_entry = ttk.Entry(frame)
    details_entry.grid(row=13, column=1, sticky="w", padx=5)

    ttk.Button(frame, text="Add Research Project", command=lambda: add_research_project(
        project_name_entry.get(), faculty_entry.get(), details_entry.get())
    ).grid(row=14, column=0, columnspan=2, pady=5)

    # Section: Publication Management
    publication_label = ttk.Label(frame, text="Publications Management", font=("Arial", 12, "bold"))
    publication_label.grid(row=15, column=0, columnspan=2, pady=10)

    ttk.Label(frame, text="Faculty Name:").grid(row=16, column=0, sticky="e", padx=5)
    publication_faculty_entry = ttk.Entry(frame)
    publication_faculty_entry.grid(row=16, column=1, sticky="w", padx=5)

    ttk.Label(frame, text="Publication Title:").grid(row=17, column=0, sticky="e", padx=5)
    publication_title_entry = ttk.Entry(frame)
    publication_title_entry.grid(row=17, column=1, sticky="w", padx=5)

    ttk.Label(frame, text="Journal Name:").grid(row=18, column=0, sticky="e", padx=5)
    journal_name_entry = ttk.Entry(frame)
    journal_name_entry.grid(row=18, column=1, sticky="w", padx=5)

    ttk.Button(frame, text="Add Publication", command=lambda: add_publication(
        publication_faculty_entry.get(), publication_title_entry.get(), journal_name_entry.get())
    ).grid(row=19, column=0, columnspan=2, pady=5)

     # Section: Accounts Management
    accounts_label = ttk.Label(frame, text="Account Management", font=("Arial", 12, "bold"))
    accounts_label.grid(row=23, column=0, columnspan=2, pady=10)

    ttk.Label(frame, text="Income:").grid(row=24, column=0, sticky="e", padx=5)
    income_entry = ttk.Entry(frame)
    income_entry.grid(row=24, column=1, sticky="w", padx=5)

    ttk.Label(frame, text="Expenditure:").grid(row=25, column=0, sticky="e", padx=5)
    expenditure_entry = ttk.Entry(frame)
    expenditure_entry.grid(row=25, column=1, sticky="w", padx=5)

    ttk.Button(frame, text="Update Account", command=lambda: update_account(
        float(income_entry.get()), float(expenditure_entry.get()))
    ).grid(row=26, column=0, columnspan=2, pady=5)

    ttk.Button(frame, text="Generate Financial Report", command=generate_financial_report).grid(row=27, column=0, columnspan=2, pady=5)

   # Section: Inventory Management
    inventory_label = ttk.Label(frame, text="Inventory Management", font=("Arial", 12, "bold"))
    inventory_label.grid(row=28, column=0, columnspan=2, pady=10)

# Add input fields foar inventory item details
    ttk.Label(frame, text="Item Name:").grid(row=29, column=0, sticky="e", padx=5)
    item_name_entry = ttk.Entry(frame)
    item_name_entry.grid(row=29, column=1, sticky="w", padx=5)

    ttk.Label(frame, text="Item Type:").grid(row=30, column=0, sticky="e", padx=5)
    item_type_entry = ttk.Entry(frame)
    item_type_entry.grid(row=30, column=1, sticky="w", padx=5)

    ttk.Label(frame, text="Location:").grid(row=31, column=0, sticky="e", padx=5)
    location_entry = ttk.Entry(frame)
    location_entry.grid(row=31, column=1, sticky="w", padx=5)

# Button to add inventory item
    ttk.Button(frame, text="Add Inventory Item", command=lambda: add_inventory_item(
    item_name_entry.get(), item_type_entry.get(), location_entry.get())
    ).grid(row=32, column=0, columnspan=2, pady=10)

# Correcting row index for "Delete Inventory Item"
    ttk.Button(frame, text="Delete Inventory Item", command=lambda: delete_inventory_item(item_name_entry.get())).grid(row=33, column=0, columnspan=2, pady=5)

# Section: CSV Operations
    csv_label = ttk.Label(frame, text="CSV Operations", font=("Arial", 12, "bold"))
    csv_label.grid(row=20, column=0, columnspan=2, pady=10)

    ttk.Button(frame, text="Import CSV", command=import_csv).grid(row=21, column=0, columnspan=2, pady=5)
    ttk.Button(frame, text="Export CSV", command=export_csv).grid(row=22, column=0, columnspan=2, pady=5)
# Add Exit Button at the end of the GUI
    ttk.Button(frame, text="Exit", command=root.quit).grid(row=34, column=0, columnspan=2, pady=10)


    root.mainloop()

# Run the application
create_tables()
main_gui()
