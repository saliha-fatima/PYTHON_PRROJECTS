import tkinter as tk
from tkinter import messagebox
from tkinter import font
import csv

# Sample Data for Demonstration
students = {}
staff = {}
complaints = {}
financials = {'mess_charges': 0, 'room_rent': 0, 'amenities_charge': 0}
expenses = []
staff_salary = {}

# Function to Add Student
def add_student(name, address, contact, photo, hall, room):
    student_id = len(students) + 1
    students[student_id] = {'name': name, 'address': address, 'contact': contact, 'photo': photo, 'hall': hall, 'room': room}
    messagebox.showinfo("Success", f"Student {name} added successfully!")

# Function to Add Mess Charge
def add_mess_charge(student_id, amount):
    if student_id in students:
        students[student_id]['mess_charge'] = amount
        messagebox.showinfo("Success", "Mess charge added successfully!")
    else:
        messagebox.showerror("Error", "Student not found!")

# Function to Calculate Due
def calculate_due(student_id):
    if student_id in students:
        mess_charge = students[student_id].get('mess_charge', 0)
        amenities_charge = financials.get('amenities_charge', 0)
        room_rent = financials.get('room_rent', 0)
        total_due = mess_charge + amenities_charge + room_rent
        return total_due
    else:
        return "Student not found!"

# Function to Register Complaint
def register_complaint(student_id, complaint_text):
    complaint_id = len(complaints) + 1
    complaints[complaint_id] = {'student_id': student_id, 'complaint': complaint_text, 'status': 'Pending'}
    messagebox.showinfo("Success", "Complaint registered successfully!")

# Function to View Complaints
def view_complaints():
    complaints_text = ""
    for complaint_id, complaint_data in complaints.items():
        complaints_text += f"ID: {complaint_id}, Student ID: {complaint_data['student_id']}, Complaint: {complaint_data['complaint']}, Status: {complaint_data['status']}\n"
    messagebox.showinfo("Complaints", complaints_text)

# Function to Add Staff
def add_staff(name, daily_pay):
    staff_id = len(staff) + 1
    staff[staff_id] = {'name': name, 'daily_pay': daily_pay}
    staff_salary[staff_id] = {'leave_days': 0}
    messagebox.showinfo("Success", f"Staff {name} added successfully!")

# Function to Record Staff Leave
def record_staff_leave(staff_id, leave_days):
    if staff_id in staff_salary:
        staff_salary[staff_id]['leave_days'] = leave_days
        messagebox.showinfo("Success", f"Leave recorded for staff {staff[staff_id]['name']}!")
    else:
        messagebox.showerror("Error", "Staff not found!")

# Function to Generate Salary
def generate_salary():
    salary_report = ""
    for staff_id, details in staff.items():
        daily_pay = details['daily_pay']
        leave_days = staff_salary[staff_id]['leave_days']
        total_salary = (30 - leave_days) * daily_pay
        salary_report += f"Staff Name: {details['name']}, Salary: {total_salary}\n"
    messagebox.showinfo("Salary Report", salary_report)

# Function to Enter Expense
def enter_expense(description, amount):
    expenses.append({'description': description, 'amount': amount})
    messagebox.showinfo("Success", "Expense entered successfully!")

# Function to View Financial Statement
def view_financial_statement():
    financial_report = "Expenses:\n"
    total_expense = 0
    for expense in expenses:
        financial_report += f"{expense['description']}: {expense['amount']}\n"
        total_expense += expense['amount']
    financial_report += f"Total Expenses: {total_expense}\n"
    financial_report += f"Total Mess Charges: {financials['mess_charges']}\n"
    financial_report += f"Total Room Rent: {financials['room_rent']}\n"
    financial_report += f"Total Amenities Charges: {financials['amenities_charge']}\n"
    messagebox.showinfo("Financial Statement", financial_report)

# Function to Export Data to CSV
def export_to_csv():
    with open("students.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Student ID", "Name", "Address", "Contact", "Photo", "Hall", "Room"])
        for student_id, student_data in students.items():
            writer.writerow([student_id, student_data['name'], student_data['address'], student_data['contact'], student_data['photo'], student_data['hall'], student_data['room']])
    messagebox.showinfo("Success", "Data exported to students.csv successfully!")

# Main Application GUI
class HMCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IIT Students' Hall Management Center")

        # Set font for modern look
        self.font_style = font.Font(family="Helvetica", size=12)

        # Add Student Frame
        self.add_student_frame = tk.Frame(self.root)
        self.add_student_frame.pack(pady=10)

        self.student_name_label = tk.Label(self.add_student_frame, text="Student Name:", font=self.font_style)
        self.student_name_label.grid(row=0, column=0)
        self.student_name_entry = tk.Entry(self.add_student_frame, font=self.font_style)
        self.student_name_entry.grid(row=0, column=1)

        self.student_address_label = tk.Label(self.add_student_frame, text="Address:", font=self.font_style)
        self.student_address_label.grid(row=1, column=0)
        self.student_address_entry = tk.Entry(self.add_student_frame, font=self.font_style)
        self.student_address_entry.grid(row=1, column=1)

        self.student_contact_label = tk.Label(self.add_student_frame, text="Contact:", font=self.font_style)
        self.student_contact_label.grid(row=2, column=0)
        self.student_contact_entry = tk.Entry(self.add_student_frame, font=self.font_style)
        self.student_contact_entry.grid(row=2, column=1)

        self.student_photo_label = tk.Label(self.add_student_frame, text="Photo:", font=self.font_style)
        self.student_photo_label.grid(row=3, column=0)
        self.student_photo_entry = tk.Entry(self.add_student_frame, font=self.font_style)
        self.student_photo_entry.grid(row=3, column=1)

        self.student_hall_label = tk.Label(self.add_student_frame, text="Hall:", font=self.font_style)
        self.student_hall_label.grid(row=4, column=0)
        self.student_hall_entry = tk.Entry(self.add_student_frame, font=self.font_style)
        self.student_hall_entry.grid(row=4, column=1)

        self.student_room_label = tk.Label(self.add_student_frame, text="Room:", font=self.font_style)
        self.student_room_label.grid(row=5, column=0)
        self.student_room_entry = tk.Entry(self.add_student_frame, font=self.font_style)
        self.student_room_entry.grid(row=5, column=1)

        self.add_student_button = tk.Button(self.add_student_frame, text="Add Student", font=self.font_style, command=self.add_student)
        self.add_student_button.grid(row=6, column=0, columnspan=2)

        # Export Data Button
        self.export_button = tk.Button(self.root, text="Export to CSV", font=self.font_style, command=export_to_csv)
        self.export_button.pack(pady=10)

    def add_student(self):
        name = self.student_name_entry.get()
        address = self.student_address_entry.get()
        contact = self.student_contact_entry.get()
        photo = self.student_photo_entry.get()
        hall = self.student_hall_entry.get()
        room = self.student_room_entry.get()
        add_student(name, address, contact, photo, hall, room)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = HMCApp(root)
    root.mainloop()
