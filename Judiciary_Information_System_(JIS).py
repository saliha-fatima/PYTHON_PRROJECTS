import tkinter as tk
from tkinter import messagebox, filedialog
import datetime
import csv

# Court case storage
court_cases = {}
user_accounts = {}

# Generate a unique case ID (CIN)
def generate_case_id():
    return len(court_cases) + 1

# Add a new case
def add_case():
    case_id = generate_case_id()
    defendant_name = entry_defendant_name.get()
    defendant_address = entry_defendant_address.get()
    crime_type = entry_crime_type.get()
    crime_date = entry_crime_date.get()
    location = entry_location.get()
    arresting_officer = entry_arresting_officer.get()
    arrest_date = entry_arrest_date.get()
    hearing_date = entry_hearing_date.get()
    judge_name = entry_judge_name.get()
    prosecutor_name = entry_prosecutor_name.get()
    trial_start_date = entry_trial_start_date.get()
    expected_end_date = entry_expected_end_date.get()

    court_cases[case_id] = {
        'defendant_name': defendant_name,
        'defendant_address': defendant_address,
        'crime_type': crime_type,
        'crime_date': crime_date,
        'location': location,
        'arresting_officer': arresting_officer,
        'arrest_date': arrest_date,
        'hearing_date': hearing_date,
        'judge_name': judge_name,
        'prosecutor_name': prosecutor_name,
        'trial_start_date': trial_start_date,
        'expected_end_date': expected_end_date,
        'status': 'pending',
        'adjournments': [],
        'judgment_summary': '',
        'lawyers': [],
    }
    messagebox.showinfo("Success", f"Case with CIN {case_id} added successfully!")

# Import cases from a CSV file
def import_cases():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return
    
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            case_id = generate_case_id()
            court_cases[case_id] = row
    messagebox.showinfo("Success", "Cases imported successfully!")

# Export cases to a CSV file
def export_cases():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return
    
    with open(file_path, "w", newline="") as file:
        fieldnames = ['defendant_name', 'defendant_address', 'crime_type', 'crime_date', 'location',
                      'arresting_officer', 'arrest_date', 'hearing_date', 'judge_name', 'prosecutor_name',
                      'trial_start_date', 'expected_end_date', 'status', 'adjournments', 'judgment_summary', 'lawyers']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for case in court_cases.values():
            writer.writerow(case)
    messagebox.showinfo("Success", "Cases exported successfully!")

# GUI Window with Font Adjustment
root = tk.Tk()
root.title("Judiciary Information System")
font_style = ("Arial", 12)  # Increased Font Size

# Create tabs and frames
frame_main = tk.Frame(root)
frame_main.pack(padx=10, pady=10)

frame_case = tk.LabelFrame(root, text="Add Case", font=font_style)
frame_case.pack(padx=10, pady=10)

frame_search = tk.LabelFrame(root, text="Search & Update Cases", font=font_style)
frame_search.pack(padx=10, pady=10)

frame_user = tk.LabelFrame(root, text="User Management", font=font_style)
frame_user.pack(padx=10, pady=10)

# Labels and Entries for adding a case
fields = [
    "Defendant Name", "Defendant Address", "Crime Type", "Crime Date", "Location", 
    "Arresting Officer", "Arrest Date", "Hearing Date", "Judge Name", 
    "Prosecutor Name", "Trial Start Date", "Expected End Date"
]
entries = []
for idx, field in enumerate(fields):
    tk.Label(frame_case, text=field, font=font_style).grid(row=idx, column=0, sticky="w")
    entry = tk.Entry(frame_case, font=font_style)
    entry.grid(row=idx, column=1)
    entries.append(entry)

(entry_defendant_name, entry_defendant_address, entry_crime_type, entry_crime_date,
 entry_location, entry_arresting_officer, entry_arrest_date, entry_hearing_date,
 entry_judge_name, entry_prosecutor_name, entry_trial_start_date, entry_expected_end_date) = entries

tk.Button(frame_case, text="Add Case", font=font_style, command=add_case).grid(row=len(fields), column=0, columnspan=2)

# Import/Export Buttons
tk.Button(frame_case, text="Import Cases (CSV)", font=font_style, command=import_cases).grid(row=len(fields)+1, column=0)
tk.Button(frame_case, text="Export Cases (CSV)", font=font_style, command=export_cases).grid(row=len(fields)+1, column=1)

# Search Panel
tk.Label(frame_search, text="Search Pending Cases", font=font_style).grid(row=0, column=0)
tk.Button(frame_search, text="Search", font=font_style, command=lambda: messagebox.showinfo("Not Implemented", "Search Pending Cases")).grid(row=0, column=1)

# Result Text Area
result_text = tk.Text(root, height=10, width=80, font=font_style)
result_text.pack(padx=10, pady=10)

root.mainloop()
