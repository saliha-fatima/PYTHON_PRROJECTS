import datetime
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import csv

# Data Storage
complaints = []
repair_schedule = []
available_resources = {
    "raw_material": {},
    "machines": {},
    "manpower": {}
}
utilization_stats = {
    "repairs": [],
    "usage": []
}

# Add a complaint
def add_complaint(area, description):
    complaints.append({
        "id": len(complaints) + 1,
        "area": area,
        "description": description,
        "date": datetime.date.today(),
        "status": "Pending"
    })

def print_complaints_by_area():
    area_complaints = {}
    for complaint in complaints:
        if complaint['status'] == "Pending":
            if complaint['area'] not in area_complaints:
                area_complaints[complaint['area']] = []
            area_complaints[complaint['area']].append(complaint)
    return area_complaints

# Assign priority and resources
def prioritize_and_schedule(complaint_id, priority, raw_material, machines, manpower):
    for complaint in complaints:
        if complaint['id'] == complaint_id:
            complaint['priority'] = priority
            complaint['status'] = "Scheduled"
            repair_schedule.append({
                "id": complaint_id,
                "area": complaint['area'],
                "priority": priority,
                "raw_material": raw_material,
                "machines": machines,
                "manpower": manpower,
                "date_scheduled": datetime.date.today()
            })
            break

# Update availability of resources
def update_resources(resource_type, resource_name, quantity):
    if resource_type in available_resources:
        available_resources[resource_type][resource_name] = quantity
        reschedule_all()

# Reschedule repairs if resources change
def reschedule_all():
    global repair_schedule
    repair_schedule = []
    for complaint in complaints:
        if complaint['status'] == "Scheduled":
            prioritize_and_schedule(complaint['id'], complaint['priority'], {}, {}, {})

# Import complaints from CSV
def import_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                add_complaint(row["Area"], row["Description"])
        messagebox.showinfo("Success", "Complaints imported successfully!")
        show_complaints()
    else:
        messagebox.showerror("Error", "No file selected!")

# Generate statistics
def repair_statistics(start_date, end_date):
    completed = [r for r in utilization_stats['repairs'] if start_date <= r['completion_date'] <= end_date]
    outstanding = [r for r in repair_schedule if start_date <= r['date_scheduled'] <= end_date]
    return completed, outstanding

# GUI Functions
def submit_complaint():
    area = area_entry.get()
    description = description_entry.get()
    if area and description:
        add_complaint(area, description)
        messagebox.showinfo("Success", "Complaint added successfully!")
        area_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        show_complaints()
    else:
        messagebox.showerror("Error", "All fields are required!")

def show_complaints():
    area_complaints = print_complaints_by_area()
    complaints_text.delete(1.0, tk.END)
    for area, comp_list in area_complaints.items():
        complaints_text.insert(tk.END, f"Complaints for {area}:\n")
        for comp in comp_list:
            complaints_text.insert(tk.END, f"  ID: {comp['id']}, Description: {comp['description']}, Date: {comp['date']}\n")

def update_resource():
    resource_type = resource_type_var.get()
    resource_name = resource_name_entry.get()
    quantity = resource_quantity_entry.get()
    if resource_type and resource_name and quantity.isdigit():
        update_resources(resource_type, resource_name, int(quantity))
        messagebox.showinfo("Success", "Resource updated successfully!")
        resource_name_entry.delete(0, tk.END)
        resource_quantity_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "All fields are required and quantity must be a number!")

# GUI Setup
root = tk.Tk()
root.title("Road Repair and Tracking System")
root.configure(padx=20, pady=20)

# Font Configuration
font_large = ("Helvetica", 12)

# Add Complaint Section
tk.Label(root, text="Add Complaint", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
tk.Label(root, text="Area:", font=font_large).grid(row=1, column=0, sticky=tk.W, pady=5)
tk.Label(root, text="Description:", font=font_large).grid(row=2, column=0, sticky=tk.W, pady=5)
area_entry = tk.Entry(root, font=font_large)
area_entry.grid(row=1, column=1)
description_entry = tk.Entry(root, font=font_large)
description_entry.grid(row=2, column=1)
submit_button = tk.Button(root, text="Submit", command=submit_complaint, font=font_large)
submit_button.grid(row=3, column=0, columnspan=2, pady=10)

# Show Complaints Section
tk.Label(root, text="Pending Complaints", font=("Helvetica", 14, "bold")).grid(row=4, column=0, columnspan=2, pady=10)
complaints_text = tk.Text(root, height=10, width=50, font=font_large)
complaints_text.grid(row=5, column=0, columnspan=2)
show_complaints_button = tk.Button(root, text="Show Complaints", command=show_complaints, font=font_large)
show_complaints_button.grid(row=6, column=0, columnspan=2, pady=10)

# Import CSV Section
import_csv_button = tk.Button(root, text="Import Complaints (CSV)", command=import_csv, font=font_large)
import_csv_button.grid(row=7, column=0, columnspan=2, pady=10)

# Update Resources Section
tk.Label(root, text="Update Resources", font=("Helvetica", 14, "bold")).grid(row=8, column=0, columnspan=2, pady=10)
tk.Label(root, text="Resource Type:", font=font_large).grid(row=9, column=0, sticky=tk.W, pady=5)
tk.Label(root, text="Resource Name:", font=font_large).grid(row=10, column=0, sticky=tk.W, pady=5)
tk.Label(root, text="Quantity:", font=font_large).grid(row=11, column=0, sticky=tk.W, pady=5)
resource_type_var = ttk.Combobox(root, values=["raw_material", "machines", "manpower"], font=font_large)
resource_type_var.grid(row=9, column=1)
resource_name_entry = tk.Entry(root, font=font_large)
resource_name_entry.grid(row=10, column=1)
resource_quantity_entry = tk.Entry(root, font=font_large)
resource_quantity_entry.grid(row=11, column=1)
update_resource_button = tk.Button(root, text="Update Resource", command=update_resource, font=font_large)
update_resource_button.grid(row=12, column=0, columnspan=2, pady=10)

root.mainloop()
