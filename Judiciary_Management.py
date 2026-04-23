import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk  # Import ttk for scrollbar
import datetime
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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

# Search for pending cases
def search_pending_cases():
    pending_cases = {case_id: case for case_id, case in court_cases.items() if case['status'] == 'pending'}
    
    if not pending_cases:
        messagebox.showinfo("No Results", "No pending cases found.")
        return

    result_text.delete(1.0, tk.END)  # Clear previous results

    for case_id, case in pending_cases.items():
        result_text.insert(tk.END, f"Case ID: {case_id}\n")
        result_text.insert(tk.END, f"Defendant Name: {case['defendant_name']}\n")
        result_text.insert(tk.END, f"Crime Type: {case['crime_type']}\n")
        result_text.insert(tk.END, f"Crime Date: {case['crime_date']}\n")
        result_text.insert(tk.END, f"Status: {case['status']}\n")
        result_text.insert(tk.END, "-" * 40 + "\n")

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

# Generate case report (PDF)
def generate_case_report(case_id):
    if case_id not in court_cases:
        messagebox.showerror("Error", "Case ID not found!")
        return
    
    case = court_cases[case_id]
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if not file_path:
        return
    
    c = canvas.Canvas(file_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    
    y_position = 750
    for key, value in case.items():
        c.drawString(30, y_position, f"{key.replace('_', ' ').title()}: {value}")
        y_position -= 20
    
    c.save()
    messagebox.showinfo("Success", f"Case {case_id} report generated successfully!")

# Scrollable Frame Class
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

# Exit Button
tk.Button(root, text="Exit", font=font_style, command=root.quit).pack(pady=10, side="bottom")


# Search Panel
tk.Label(frame_search, text="Search Pending Cases", font=font_style).grid(row=0, column=0)
tk.Button(frame_search, text="Search", font=font_style, command=search_pending_cases).grid(row=0, column=1)

# Add scrollable frame
scrollable_container = ScrollableFrame(root)
scrollable_container.pack(fill="both", expand=True, padx=10, pady=10)

# Adding result_text to the scrollable frame
result_text = tk.Text(scrollable_container.scrollable_frame, height=10, width=80, font=font_style, wrap=tk.WORD)
result_text.pack()

# Update scroll region after adding the text widget
scrollable_container.scrollable_frame.update_idletasks()

root.mainloop()
