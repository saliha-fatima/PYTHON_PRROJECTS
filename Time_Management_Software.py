import datetime
from collections import defaultdict
from tkinter import messagebox, simpledialog, font
import tkinter as tk
import csv

# Initialize the main data structures
def init_tms():
    global schedules, email_addresses, projects, leave_periods, statistics
    schedules = defaultdict(list)  # Key: executive, Value: list of appointments
    email_addresses = {}  # Key: executive, Value: email address
    projects = defaultdict(list)  # Key: project, Value: list of meetings
    leave_periods = defaultdict(list)  # Key: executive, Value: list of leave periods
    statistics = defaultdict(lambda: defaultdict(int))  # For tracking time stats

# Register an appointment
def register_appointment(executive, person, venue, start_time, duration, purpose, project=None):
    global schedules, projects, statistics
    end_time = start_time + datetime.timedelta(minutes=duration)
    schedules[executive].append({
        'person': person,
        'venue': venue,
        'start_time': start_time,
        'end_time': end_time,
        'purpose': purpose,
        'project': project
    })
    if project:
        projects[project].append((executive, start_time, end_time))
    statistics[executive]['meetings'] += duration
    if project:
        statistics[project]['man_hours'] += duration

# Daily schedule emails
def daily_schedule_emails():
    for executive, appointments in schedules.items():
        body = "Today's Appointments:\n"
        for app in appointments:
            body += f"Meeting with {app['person']} at {app['venue']} from {app['start_time']} to {app['end_time']}\n"
        if executive in email_addresses:
            print(f"Email to {executive}:\n{body}")  # Replace with email sending logic

# Calculate statistics
def calculate_statistics():
    stats = ""
    for executive, data in statistics.items():
        stats += f"Executive {executive}: {data['meetings']} minutes in meetings.\n"
    for project, data in statistics.items():
        stats += f"Project {project}: {data['man_hours']} man-hours devoted.\n"
    return stats

# Export schedules to a CSV file
def export_to_csv():
    try:
        with open("schedules.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Executive", "Person", "Venue", "Start Time", "End Time", "Purpose", "Project"])
            for executive, appointments in schedules.items():
                for app in appointments:
                    writer.writerow([
                        executive,
                        app['person'],
                        app['venue'],
                        app['start_time'],
                        app['end_time'],
                        app['purpose'],
                        app['project'] or "N/A"
                    ])
        messagebox.showinfo("Success", "Schedules exported to 'schedules.csv'")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export CSV: {e}")

# GUI for TMS with separate buttons for Add Appointment fields
def tms_gui():
    def show_message(title, message):
        messagebox.showinfo(title, message)

    def add_appointment():
        # Use a dictionary to store shared variables
        appointment_data = {
            "executive": None,
            "person": None,
            "venue": None,
            "start_time": None,
            "duration": None,
            "purpose": None,
            "project": None,
        }

        def get_executive():
            appointment_data["executive"] = simpledialog.askstring("Input", "Enter executive name:")

        def get_person():
            appointment_data["person"] = simpledialog.askstring("Input", "Enter person to meet:")

        def get_venue():
            appointment_data["venue"] = simpledialog.askstring("Input", "Enter venue:")

        def get_start_time():
            try:
                time_str = simpledialog.askstring("Input", "Enter start time (YYYY-MM-DD HH:MM):")
                appointment_data["start_time"] = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
            except Exception as e:
                show_message("Error", f"Invalid time format: {e}")

        def get_duration():
            appointment_data["duration"] = simpledialog.askinteger("Input", "Enter duration (minutes):")

        def get_purpose():
            appointment_data["purpose"] = simpledialog.askstring("Input", "Enter purpose:")

        def get_project():
            appointment_data["project"] = simpledialog.askstring("Input", "Enter project (optional):")

        def submit_appointment():
            try:
                register_appointment(
                    appointment_data["executive"],
                    appointment_data["person"],
                    appointment_data["venue"],
                    appointment_data["start_time"],
                    appointment_data["duration"],
                    appointment_data["purpose"],
                    appointment_data["project"],
                )
                show_message("Success", "Appointment added successfully!")
            except Exception as e:
                show_message("Error", f"Failed to add appointment: {e}")

        root = tk.Toplevel()
        root.title("Add Appointment")

        # Font settings
        button_font = font.Font(size=12)

        tk.Button(root, text="Enter Executive", font=button_font, command=get_executive).pack(pady=5)
        tk.Button(root, text="Enter Person", font=button_font, command=get_person).pack(pady=5)
        tk.Button(root, text="Enter Venue", font=button_font, command=get_venue).pack(pady=5)
        tk.Button(root, text="Enter Start Time", font=button_font, command=get_start_time).pack(pady=5)
        tk.Button(root, text="Enter Duration", font=button_font, command=get_duration).pack(pady=5)
        tk.Button(root, text="Enter Purpose", font=button_font, command=get_purpose).pack(pady=5)
        tk.Button(root, text="Enter Project", font=button_font, command=get_project).pack(pady=5)
        tk.Button(root, text="Submit Appointment", font=button_font, command=submit_appointment).pack(pady=5)

    def view_schedule():
        executive = simpledialog.askstring("Input", "Enter executive name to view schedule:")
        if executive in schedules:
            schedule = ""
            for app in schedules[executive]:
                schedule += f"Meeting with {app['person']} at {app['venue']} from {app['start_time']} to {app['end_time']}\n"
            show_message("Schedule", schedule)
        else:
            show_message("Error", "No schedule found for this executive.")

    def send_daily_emails():
        try:
            daily_schedule_emails()
            show_message("Success", "Daily emails sent successfully!")
        except Exception as e:
            show_message("Error", f"Failed to send emails: {e}")

    def show_statistics():
        stats = calculate_statistics()
        show_message("Statistics", stats)

    root = tk.Tk()
    root.title("Time Management Software")

    # Font settings
    button_font = font.Font(size=12)

    tk.Button(root, text="Add Appointment", font=button_font, command=add_appointment).pack(pady=5)
    tk.Button(root, text="View Schedule", font=button_font, command=view_schedule).pack(pady=5)
    tk.Button(root, text="Send Daily Emails", font=button_font, command=send_daily_emails).pack(pady=5)
    tk.Button(root, text="View Statistics", font=button_font, command=show_statistics).pack(pady=5)
    tk.Button(root, text="Export to CSV", font=button_font, command=export_to_csv).pack(pady=5)
    tk.Button(root, text="Exit", font=button_font, command=root.quit).pack(pady=5)

    root.mainloop()

# Initialize TMS system
init_tms()
tms_gui()
