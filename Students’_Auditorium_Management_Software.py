import tkinter as tk
from tkinter import messagebox
import datetime
import csv

# Database-like structure to hold the data
shows = {}
salespersons = {}
tickets = {}
cancellations = {}
expenditures = {}
balance_sheets = {}

# Helper functions
def get_current_date():
    return datetime.datetime.now().date()

def add_show(show_id, date, balcony_seats, ordinary_seats, balcony_price, ordinary_price):
    shows[show_id] = {
        'date': date,
        'balcony_seats': balcony_seats,
        'ordinary_seats': ordinary_seats,
        'balcony_price': balcony_price,
        'ordinary_price': ordinary_price,
        'booked_balcony': 0,
        'booked_ordinary': 0
    }
    save_shows_to_csv()

def book_ticket(show_id, seat_type, quantity, salesperson_id):
    if show_id not in shows:
        messagebox.showerror("Error", "Show not found!")
        return
    
    show = shows[show_id]
    if seat_type == 'balcony':
        available = show['balcony_seats'] - show['booked_balcony']
    else:
        available = show['ordinary_seats'] - show['booked_ordinary']
    
    if available < quantity:
        messagebox.showerror("Error", f"Not enough {seat_type} seats available!")
        return

    ticket_price = show['balcony_price'] if seat_type == 'balcony' else show['ordinary_price']
    tickets[f"{show_id}_{seat_type}_{salesperson_id}"] = {
        'show_id': show_id,
        'seat_type': seat_type,
        'quantity': quantity,
        'price': ticket_price,
        'salesperson_id': salesperson_id,
        'status': 'booked'
    }

    if seat_type == 'balcony':
        show['booked_balcony'] += quantity
    else:
        show['booked_ordinary'] += quantity

    # Record the salesperson's sale
    if salesperson_id not in salespersons:
        salespersons[salesperson_id] = {'name': '', 'total_sales': 0}
    salespersons[salesperson_id]['total_sales'] += ticket_price * quantity

    save_salespersons_to_csv()
    messagebox.showinfo("Success", f"Booked {quantity} {seat_type} seat(s) successfully!")

def cancel_ticket(ticket_id):
    if ticket_id not in tickets or tickets[ticket_id]['status'] != 'booked':
        messagebox.showerror("Error", "Ticket not found or already cancelled!")
        return
    
    ticket = tickets[ticket_id]
    show = shows[ticket['show_id']]
    cancellation_fee = 0
    
    # Calculate cancellation fee based on the date and seat type
    ticket_date = show['date']
    today = get_current_date()
    days_to_show = (ticket_date - today).days

    if days_to_show > 3:
        cancellation_fee = 5
    elif 1 <= days_to_show <= 3:
        cancellation_fee = 10 if ticket['seat_type'] == 'ordinary' else 15
    elif days_to_show == 0:
        cancellation_fee = ticket['price'] / 2
    
    refund_amount = ticket['price'] * ticket['quantity'] - cancellation_fee * ticket['quantity']
    tickets[ticket_id]['status'] = 'cancelled'
    
    # Update the available seats
    if ticket['seat_type'] == 'balcony':
        show['booked_balcony'] -= ticket['quantity']
    else:
        show['booked_ordinary'] -= ticket['quantity']
    
    save_tickets_to_csv()
    messagebox.showinfo("Success", f"Ticket cancelled. Refund: Rs. {refund_amount}")

def query_seat_availability(show_id):
    if show_id not in shows:
        messagebox.showerror("Error", "Show not found!")
        return

    show = shows[show_id]
    available_balcony = show['balcony_seats'] - show['booked_balcony']
    available_ordinary = show['ordinary_seats'] - show['booked_ordinary']
    messagebox.showinfo("Seat Availability", f"Available Balcony Seats: {available_balcony}\nAvailable Ordinary Seats: {available_ordinary}")

def create_salesperson_account(salesperson_id, name):
    if salesperson_id in salespersons:
        messagebox.showerror("Error", "Salesperson ID already exists!")
        return

    salespersons[salesperson_id] = {'name': name, 'total_sales': 0}
    save_salespersons_to_csv()
    messagebox.showinfo("Success", f"Salesperson {name} account created successfully!")

def generate_balance_sheet(show_id):
    if show_id not in shows:
        messagebox.showerror("Error", "Show not found!")
        return

    show = shows[show_id]
    revenue = (show['booked_balcony'] * show['balcony_price']) + (show['booked_ordinary'] * show['ordinary_price'])
    expenditure = expenditures.get(show_id, 0)
    profit_or_loss = revenue - expenditure

    balance_sheets[show_id] = {
        'revenue': revenue,
        'expenditure': expenditure,
        'profit_or_loss': profit_or_loss
    }

    messagebox.showinfo("Balance Sheet", f"Revenue: Rs. {revenue}\nExpenditure: Rs. {expenditure}\nProfit/Loss: Rs. {profit_or_loss}")

def enter_expenditure(show_id, expenditure_amount):
    if show_id not in shows:
        messagebox.showerror("Error", "Show not found!")
        return

    expenditures[show_id] = expenditure_amount
    save_expenditures_to_csv()
    messagebox.showinfo("Success", f"Expenditure of Rs. {expenditure_amount} entered for show {show_id}")

def salesperson_report(salesperson_id):
    if salesperson_id not in salespersons:
        messagebox.showerror("Error", "Salesperson not found!")
        return

    salesperson = salespersons[salesperson_id]
    messagebox.showinfo("Salesperson Report", f"Salesperson: {salesperson['name']}\nTotal Sales: Rs. {salesperson['total_sales']}")

# CSV Functions
def save_shows_to_csv():
    with open('shows.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['show_id', 'date', 'balcony_seats', 'ordinary_seats', 'balcony_price', 'ordinary_price', 'booked_balcony', 'booked_ordinary'])
        writer.writeheader()
        for show_id, show in shows.items():
            show['show_id'] = show_id
            writer.writerow(show)

def load_shows_from_csv():
    try:
        with open('shows.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                shows[row['show_id']] = row
    except FileNotFoundError:
        pass

def save_salespersons_to_csv():
    with open('salespersons.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['salesperson_id', 'name', 'total_sales'])
        writer.writeheader()
        for salesperson_id, salesperson in salespersons.items():
            writer.writerow({'salesperson_id': salesperson_id, 'name': salesperson['name'], 'total_sales': salesperson['total_sales']})

def load_salespersons_from_csv():
    try:
        with open('salespersons.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                salespersons[row['salesperson_id']] = row
    except FileNotFoundError:
        pass

def save_tickets_to_csv():
    with open('tickets.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['ticket_id', 'show_id', 'seat_type', 'quantity', 'price', 'salesperson_id', 'status'])
        writer.writeheader()
        for ticket_id, ticket in tickets.items():
            ticket['ticket_id'] = ticket_id
            writer.writerow(ticket)

def load_tickets_from_csv():
    try:
        with open('tickets.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tickets[row['ticket_id']] = row
    except FileNotFoundError:
        pass

def save_expenditures_to_csv():
    with open('expenditures.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['show_id', 'expenditure'])
        writer.writeheader()
        for show_id, expenditure in expenditures.items():
            writer.writerow({'show_id': show_id, 'expenditure': expenditure})

def load_expenditures_from_csv():
    try:
        with open('expenditures.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                expenditures[row['show_id']] = float(row['expenditure'])
    except FileNotFoundError:
        pass

# GUI Setup
root = tk.Tk()
root.title("Students' Auditorium Management Software")

# Increase font size globally
font = ('Arial', 12)

# Add Show
def add_show_ui():
    show_id = entry_show_id.get()
    date = entry_show_date.get()
    balcony_seats = int(entry_balcony_seats.get())
    ordinary_seats = int(entry_ordinary_seats.get())
    balcony_price = float(entry_balcony_price.get())
    ordinary_price = float(entry_ordinary_price.get())
    add_show(show_id, date, balcony_seats, ordinary_seats, balcony_price, ordinary_price)
    messagebox.showinfo("Success", f"Show {show_id} added successfully!")

label_show_id = tk.Label(root, text="Show ID", font=font)
label_show_id.grid(row=0, column=0)
entry_show_id = tk.Entry(root, font=font)
entry_show_id.grid(row=0, column=1)

label_show_date = tk.Label(root, text="Show Date (YYYY-MM-DD)", font=font)
label_show_date.grid(row=1, column=0)
entry_show_date = tk.Entry(root, font=font)
entry_show_date.grid(row=1, column=1)

label_balcony_seats = tk.Label(root, text="Balcony Seats", font=font)
label_balcony_seats.grid(row=2, column=0)
entry_balcony_seats = tk.Entry(root, font=font)
entry_balcony_seats.grid(row=2, column=1)

label_ordinary_seats = tk.Label(root, text="Ordinary Seats", font=font)
label_ordinary_seats.grid(row=3, column=0)
entry_ordinary_seats = tk.Entry(root, font=font)
entry_ordinary_seats.grid(row=3, column=1)

label_balcony_price = tk.Label(root, text="Balcony Seat Price", font=font)
label_balcony_price.grid(row=4, column=0)
entry_balcony_price = tk.Entry(root, font=font)
entry_balcony_price.grid(row=4, column=1)

label_ordinary_price = tk.Label(root, text="Ordinary Seat Price", font=font)
label_ordinary_price.grid(row=5, column=0)
entry_ordinary_price = tk.Entry(root, font=font)
entry_ordinary_price.grid(row=5, column=1)

button_add_show = tk.Button(root, text="Add Show", command=add_show_ui, font=font)
button_add_show.grid(row=6, columnspan=2)

# Load data from CSV on start
load_shows_from_csv()
load_salespersons_from_csv()
load_tickets_from_csv()
load_expenditures_from_csv()

root.mainloop()
