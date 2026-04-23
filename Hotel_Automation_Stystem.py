import tkinter as tk
from tkinter import messagebox, ttk
import datetime

# Data Storage
SEASONS = {
    "Summer": {"rate_multiplier": 1.2},
    "Winter": {"rate_multiplier": 0.9},
    "Default": {"rate_multiplier": 1.0},
}

MONTHLY_RATE_MULTIPLIERS = {
    "January": 1.0, "February": 1.1, "March": 1.0, "April": 1.2,
    "May": 1.3, "June": 1.5, "July": 1.5, "August": 1.3,
    "September": 1.2, "October": 1.1, "November": 1.0, "December": 1.4
}

FOOD_MENU = {
    "Breakfast": {
        "Timings": "7:00 AM - 10:00 AM",
        "Items": {
            "Pancakes": 5,
            "Omelette": 3,
            "Paratha": 2,
            "Tea": 1,
            "Juice": 2,
            "Toast": 2,
            "Coffee": 2,
        }
    },
    "Lunch": {
        "Timings": "12:00 PM - 3:00 PM",
        "Items": {
            "Biryani": 10,
            "Burger": 8,
            "Pasta": 9,
            "Soup": 4,
            "Salad": 5,
            "Grilled Chicken": 12,
            "Rice and Curry": 11,
        }
    },
    "Dinner": {
        "Timings": "7:00 PM - 10:00 PM",
        "Items": {
            "Steak": 15,
            "Pizza": 12,
            "Chinese Rice": 10,
            "Noodles": 8,
            "Dessert": 6,
            "Garlic Bread": 4,
            "Barbecue Ribs": 18,
        }
    }
}

# Users and booking data
users = {}
current_user = None
current_season = "Default"
current_month = datetime.datetime.now().strftime("%B")

# Rooms and rates
rooms = {}
room_types = ["Single Non-AC", "Single AC", "Double Non-AC", "Double AC"]
base_rates = [1000, 1500, 2000, 3000]
for i in range(1, 17):
    room_type = room_types[(i - 1) % len(room_types)]
    base_rate = base_rates[(i - 1) % len(base_rates)]
    rooms[f"{100 + i}"] = {"type": room_type, "base_rate": base_rate, "status": "Available"}

guests = {}  # token_number: guest_data
guest_token_counter = 1001
occupancy_data = {"total_days": 0, "occupied_days": 0}
catering_orders = []  # List of (token_number, food_item, quantity, price)

# Create the main window
root = tk.Tk()
root.title("Hotel Automation System")

# Functions
def register_user():
    def save_user():
        username = username_var.get()
        password = password_var.get()
        if username in users:
            messagebox.showerror("Error", "Username already exists!")
            return
        users[username] = password
        messagebox.showinfo("Success", "Registration successful! Please login.")
        reg_window.destroy()

    reg_window = tk.Toplevel()
    reg_window.title("Register")

    tk.Label(reg_window, text="Username:", font=("Arial", 12)).grid(row=0, column=0)
    username_var = tk.StringVar()
    tk.Entry(reg_window, textvariable=username_var, font=("Arial", 12)).grid(row=0, column=1)

    tk.Label(reg_window, text="Password:", font=("Arial", 12)).grid(row=1, column=0)
    password_var = tk.StringVar()
    tk.Entry(reg_window, textvariable=password_var, show="*", font=("Arial", 12)).grid(row=1, column=1)

    tk.Button(reg_window, text="Register", command=save_user, font=("Arial", 12)).grid(row=2, columnspan=2)

def login_user():
    def authenticate_user():
        global current_user
        username = username_var.get()
        password = password_var.get()
        if username in users and users[username] == password:
            current_user = username
            messagebox.showinfo("Success", "Login successful!")
            login_window.destroy()
            show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    login_window = tk.Toplevel()
    login_window.title("Login")

    tk.Label(login_window, text="Username:", font=("Arial", 12)).grid(row=0, column=0)
    username_var = tk.StringVar()
    tk.Entry(login_window, textvariable=username_var, font=("Arial", 12)).grid(row=0, column=1)

    tk.Label(login_window, text="Password:", font=("Arial", 12)).grid(row=1, column=0)
    password_var = tk.StringVar()
    tk.Entry(login_window, textvariable=password_var, show="*", font=("Arial", 12)).grid(row=1, column=1)

    tk.Button(login_window, text="Login", command=authenticate_user, font=("Arial", 12)).grid(row=2, columnspan=2)

def display_food_menu():
    menu_window = tk.Toplevel()
    menu_window.title("Food Menu")

    row = 0
    for meal_time, data in FOOD_MENU.items():
        tk.Label(menu_window, text=f"{meal_time} ({data['Timings']}):", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2)
        row += 1

        for food_item, price in data["Items"].items():
            tk.Label(menu_window, text=f"{food_item}: ${price}", font=("Arial", 12)).grid(row=row, column=0, sticky="w")
            row += 1

# List to store complaints
complaints = []

def file_complaint():
    def submit_complaint():
        guest_name = name_entry.get()
        contact_email = email_entry.get()
        contact_number = phone_entry.get()
        complaint_text = complaint_entry.get("1.0", "end-1c")
        room_number = room_number_entry.get()
        check_in_date = check_in_entry.get()
        check_out_date = check_out_entry.get()

        if not guest_name or not contact_email or not contact_number or not complaint_text or not room_number or not check_in_date or not check_out_date:
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        try:
            check_in = datetime.datetime.strptime(check_in_date, "%d-%m-%Y")
            check_out = datetime.datetime.strptime(check_out_date, "%d-%m-%Y")
            days_of_stay = (check_out - check_in).days
            if days_of_stay < 0:
                raise ValueError("Check-out date cannot be earlier than check-in date.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid date format or error: {e}")
            return

        complaint = {
            "name": guest_name,
            "email": contact_email,
            "phone": contact_number,
            "complaint": complaint_text,
            "room_number": room_number,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "days_of_stay": days_of_stay,
        }
        complaints.append(complaint)
        messagebox.showinfo("Complaint Submitted", "Thank you for your feedback! We will address your complaint as soon as possible.")
        complaint_window.destroy()

    complaint_window = tk.Toplevel()
    complaint_window.title("File a Complaint")

    tk.Label(complaint_window, text="Your Name:", font=("Arial", 12)).grid(row=0, column=0, pady=10)
    name_entry = tk.Entry(complaint_window, font=("Arial", 12))
    name_entry.grid(row=0, column=1, pady=10)

    tk.Label(complaint_window, text="Contact Email:", font=("Arial", 12)).grid(row=1, column=0, pady=10)
    email_entry = tk.Entry(complaint_window, font=("Arial", 12))
    email_entry.grid(row=1, column=1, pady=10)

    tk.Label(complaint_window, text="Contact Number:", font=("Arial", 12)).grid(row=2, column=0, pady=10)
    phone_entry = tk.Entry(complaint_window, font=("Arial", 12))
    phone_entry.grid(row=2, column=1, pady=10)

    tk.Label(complaint_window, text="Room Number:", font=("Arial", 12)).grid(row=3, column=0, pady=10)
    room_number_entry = tk.Entry(complaint_window, font=("Arial", 12))
    room_number_entry.grid(row=3, column=1, pady=10)

    tk.Label(complaint_window, text="Check-in Date (DD-MM-YYYY):", font=("Arial", 12)).grid(row=4, column=0, pady=10)
    check_in_entry = tk.Entry(complaint_window, font=("Arial", 12))
    check_in_entry.grid(row=4, column=1, pady=10)

    tk.Label(complaint_window, text="Check-out Date (DD-MM-YYYY):", font=("Arial", 12)).grid(row=5, column=0, pady=10)
    check_out_entry = tk.Entry(complaint_window, font=("Arial", 12))
    check_out_entry.grid(row=5, column=1, pady=10)

    tk.Label(complaint_window, text="Complaint:", font=("Arial", 12)).grid(row=6, column=0, pady=10)
    complaint_entry = tk.Text(complaint_window, font=("Arial", 12), width=40, height=6)
    complaint_entry.grid(row=6, column=1, pady=10)

    tk.Button(complaint_window, text="Submit Complaint", command=submit_complaint, font=("Arial", 12)).grid(row=7, columnspan=2, pady=20)


# Add 'File Complaint' option to the main menu
def show_main_menu():
    for widget in root.winfo_children():
        widget.grid_forget()

    button_list = [
        ("Select Season", select_season),
        ("Display Room Rates", display_room_rates),
        ("Book Room", book_room),
        ("Display Food Menu", display_food_menu),
        ("Manage Catering", manage_catering),
        ("Checkout", checkout),
        ("File Complaint", file_complaint),  # New button for filing complaints
    ]

    for idx, (button_text, command) in enumerate(button_list):
        tk.Button(root, text=button_text, command=command, font=("Arial", 12)).grid(row=idx, column=0, pady=10)


def select_season():
    def apply_season():
        global current_season
        current_season = season_var.get()
        update_room_rates()
        season_window.destroy()

    season_window = tk.Toplevel()
    season_window.title("Select Season")

    tk.Label(season_window, text="Select Season:", font=("Arial", 12)).grid(row=0, column=0)
    season_var = tk.StringVar(value=current_season)
    seasons = list(SEASONS.keys())
    ttk.Combobox(season_window, textvariable=season_var, values=seasons, font=("Arial", 12)).grid(row=0, column=1)

    tk.Button(season_window, text="Apply Season", command=apply_season, font=("Arial", 12)).grid(row=1, columnspan=2)

def update_room_rates():
    month_multiplier = MONTHLY_RATE_MULTIPLIERS[current_month]
    season_multiplier = SEASONS[current_season]["rate_multiplier"]

    for room_num, room in rooms.items():
        room["rate"] = room["base_rate"] * season_multiplier * month_multiplier

def display_room_rates():
    rate_window = tk.Toplevel()
    rate_window.title("Room Rates")

    # Display the month and season names
    month_name = current_month  # Using the global variable for current month
    season_name = current_season  # Using the global variable for current season
    tk.Label(rate_window, text=f"Room Rates for {month_name} ({season_name} season):", font=("Arial", 12)).grid(row=0, column=0, columnspan=2)

    for idx, (room_num, room) in enumerate(rooms.items()):
        tk.Label(rate_window, text=f"Room {room_num}: {room['type']} - ${room['rate']:.2f} ({room['status']})", font=("Arial", 12)).grid(row=idx + 1, column=0, columnspan=2)

import datetime

def book_room():
    def process_booking():
        global guest_token_counter
        guest_name = name_entry.get()
        room_type = room_type_var.get()
        ac_status = ac_var.get()
        full_room_type = f"{room_type} {'AC' if ac_status == 'Yes' else 'Non-AC'}"
        check_in_date = check_in_date_entry.get()
        num_days = int(days_entry.get())

        try:
            # Validate the check-in date format
            check_in_date_obj = datetime.datetime.strptime(check_in_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid Check-in Date format. Use YYYY-MM-DD.")
            return

        # Calculate the check-out date
        check_out_date_obj = check_in_date_obj + datetime.timedelta(days=num_days)
        check_out_date = check_out_date_obj.strftime("%Y-%m-%d")

        # Check if the selected room type is available
        available_room = None
        for room_num, room in rooms.items():
            if room["type"] == full_room_type and room["status"] == "Available":
                available_room = room_num
                break

        if available_room:
            # Book the room
            rooms[available_room]["status"] = "Occupied"
            guests[guest_token_counter] = {
                "name": guest_name,
                "room": available_room,
                "room_type": full_room_type,
                "rate": rooms[available_room]["rate"],
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                "num_days": num_days
            }
            messagebox.showinfo("Booking Confirmed", f"Room {available_room} booked successfully for {guest_name}! Token: {guest_token_counter}\nCheck-in: {check_in_date}\nCheck-out: {check_out_date}")
            guest_token_counter += 1
            show_main_menu()
        else:
            messagebox.showerror("Error", "No rooms available of the selected type!")

    # Clear existing widgets in the root window before adding new ones
    for widget in root.winfo_children():
        widget.grid_forget()

    tk.Label(root, text="Guest Name:", font=("Arial", 12)).grid(row=0, column=0, pady=10)
    name_entry = tk.Entry(root, font=("Arial", 12))
    name_entry.grid(row=0, column=1, pady=10)

    tk.Label(root, text="Room Type:", font=("Arial", 12)).grid(row=1, column=0, pady=10)
    room_type_var = tk.StringVar(value="Single")
    tk.OptionMenu(root, room_type_var, *["Single", "Double"]).grid(row=1, column=1, pady=10)

    tk.Label(root, text="AC Required:", font=("Arial", 12)).grid(row=2, column=0, pady=10)
    ac_var = tk.StringVar(value="No")
    tk.OptionMenu(root, ac_var, *["Yes", "No"]).grid(row=2, column=1, pady=10)

    tk.Label(root, text="Check-in Date (YYYY-MM-DD):", font=("Arial", 12)).grid(row=3, column=0, pady=10)
    check_in_date_entry = tk.Entry(root, font=("Arial", 12))
    check_in_date_entry.grid(row=3, column=1, pady=10)

    tk.Label(root, text="Number of Days:", font=("Arial", 12)).grid(row=4, column=0, pady=10)
    days_entry = tk.Entry(root, font=("Arial", 12))
    days_entry.grid(row=4, column=1, pady=10)

    tk.Button(root, text="Book Room", command=process_booking, font=("Arial", 12)).grid(row=5, columnspan=2, pady=20)


def manage_catering():
    def update_item_options(*args):
        meal_time = meal_time_var.get()
        item_dropdown["values"] = list(FOOD_MENU[meal_time]["Items"].keys())
        item_var.set(item_dropdown["values"][0])

    def add_order():
        try:
            token = int(token_entry.get())
            item = item_var.get()
            quantity = int(quantity_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please enter numeric values for token and quantity.")
            return

        if token not in guests:
            messagebox.showerror("Error", "Invalid guest token!")
            return

        price = FOOD_MENU[meal_time_var.get()]['Items'].get(item, 0) * quantity
        catering_orders.append((token, item, quantity, price))
        messagebox.showinfo("Success", f"Order added for Token {token}: {quantity} x {item} - ${price:.2f}")

    def view_orders():
        orders_window = tk.Toplevel()
        orders_window.title("Catering Orders")

        tk.Label(orders_window, text="Catering Orders:", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=4)

        tk.Label(orders_window, text="Token", font=("Arial", 12, "bold")).grid(row=1, column=0)
        tk.Label(orders_window, text="Item", font=("Arial", 12, "bold")).grid(row=1, column=1)
        tk.Label(orders_window, text="Quantity", font=("Arial", 12, "bold")).grid(row=1, column=2)
        tk.Label(orders_window, text="Price", font=("Arial", 12, "bold")).grid(row=1, column=3)

        for idx, (token, item, quantity, price) in enumerate(catering_orders, start=2):
            tk.Label(orders_window, text=str(token), font=("Arial", 12)).grid(row=idx, column=0)
            tk.Label(orders_window, text=item, font=("Arial", 12)).grid(row=idx, column=1)
            tk.Label(orders_window, text=str(quantity), font=("Arial", 12)).grid(row=idx, column=2)
            tk.Label(orders_window, text=f"${price:.2f}", font=("Arial", 12)).grid(row=idx, column=3)

    catering_window = tk.Toplevel()
    catering_window.title("Manage Catering")

    tk.Label(catering_window, text="Guest Token:", font=("Arial", 12)).grid(row=0, column=0)
    token_entry = tk.Entry(catering_window, font=("Arial", 12))
    token_entry.grid(row=0, column=1)

    tk.Label(catering_window, text="Meal Time:", font=("Arial", 12)).grid(row=1, column=0)
    meal_time_var = tk.StringVar(value="Breakfast")
    meal_time_dropdown = ttk.Combobox(catering_window, textvariable=meal_time_var, values=list(FOOD_MENU.keys()), font=("Arial", 12))
    meal_time_dropdown.grid(row=1, column=1)
    meal_time_dropdown.bind("<<ComboboxSelected>>", update_item_options)

    tk.Label(catering_window, text="Item:", font=("Arial", 12)).grid(row=2, column=0)
    item_var = tk.StringVar()
    item_dropdown = ttk.Combobox(catering_window, textvariable=item_var, font=("Arial", 12))
    item_dropdown.grid(row=2, column=1)
    update_item_options()

    tk.Label(catering_window, text="Quantity:", font=("Arial", 12)).grid(row=3, column=0)
    quantity_entry = tk.Entry(catering_window, font=("Arial", 12))
    quantity_entry.grid(row=3, column=1)

    tk.Button(catering_window, text="Add Order", command=add_order, font=("Arial", 12)).grid(row=4, columnspan=2)
    tk.Button(catering_window, text="View Orders", command=view_orders, font=("Arial", 12)).grid(row=5, columnspan=2)

def checkout():
    def process_checkout():
        try:
            token = int(token_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please enter a numeric token.")
            return

        if token not in guests:
            messagebox.showerror("Error", "Invalid guest token!")
            return

        guest = guests.pop(token)
        room = rooms[guest["room"]]
        room["status"] = "Available"
        
        # Prepare the date and time info
        current_datetime = datetime.datetime.now()
        date_str = current_datetime.strftime("%d-%m-%Y")
        time_str = current_datetime.strftime("%H:%M:%S")
        day_of_week = current_datetime.strftime("%A")
        month_name = current_datetime.strftime("%B")
        
        # Room charge details
        room_charge = guest["rate"]
        
        # Catering cost details
        catering_cost = sum(order[3] for order in catering_orders if order[0] == token)
        
        # Total cost
        total_cost = room_charge + catering_cost
        
        # Creating the bill content
        bill_content = f"""
        Bill for Guest {guest['name']} (Token: {token})
        --------------------------------------------
        Date: {date_str}  |  Time: {time_str}
        Day: {day_of_week}  |  Month: {month_name}
        
        Room Charges:
        --------------
        Room Type: {guest['room_type']} (Room {guest['room']})
        Room Rate: ${room_charge:.2f}
        
        Catering Orders:
        -----------------
        """
        
        # Adding catering orders to the bill
        for order in catering_orders:
            if order[0] == token:
                bill_content += f"{order[1]} x {order[2]} - ${order[3]:.2f}\n"
        
        # Adding the total cost
        bill_content += f"""
        --------------------------------------------
        Total Catering Cost: ${catering_cost:.2f}
        Total Room Charge: ${room_charge:.2f}
        --------------------------------------------
        Total Cost: ${total_cost:.2f}
        """
        
        # Display the bill in a messagebox
        messagebox.showinfo("Checkout Complete", bill_content)

    checkout_window = tk.Toplevel()
    checkout_window.title("Checkout")

    tk.Label(checkout_window, text="Guest Token:", font=("Arial", 12)).grid(row=0, column=0)
    token_entry = tk.Entry(checkout_window, font=("Arial", 12))
    token_entry.grid(row=0, column=1)

    tk.Button(checkout_window, text="Checkout", command=process_checkout, font=("Arial", 12)).grid(row=1, columnspan=2)

# Start the application
def show_login_screen():
    tk.Button(root, text="Register", command=register_user, font=("Arial", 12)).grid(row=0, column=0, padx=20, pady=20)
    tk.Button(root, text="Login", command=login_user, font=("Arial", 12)).grid(row=1, column=0, padx=20, pady=20)

show_login_screen()
root.mainloop()
