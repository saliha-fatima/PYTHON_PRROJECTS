import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import csv

# Initialize the database (in real-world, use a database system like SQLite)
customers = {}
delivery_persons = {}
subscriptions = {}
payments = {}
deliveries = {}

# Initialize the cost of publications
publication_cost = {
    'newspaper': 5,
    'magazine': 10
}

# Function to add a new customer
def add_customer():
    customer_id = simpledialog.askstring("Input", "Enter Customer ID:")
    customer_name = simpledialog.askstring("Input", "Enter Customer Name:")
    customers[customer_id] = {'name': customer_name, 'subscriptions': [], 'outstanding': 0, 'payment_due': 0}
    messagebox.showinfo("Success", f"Customer {customer_name} added successfully.")

# Function to add a new delivery person
def add_delivery_person():
    delivery_person_id = simpledialog.askstring("Input", "Enter Delivery Person ID:")
    delivery_person_name = simpledialog.askstring("Input", "Enter Delivery Person Name:")
    delivery_persons[delivery_person_id] = {'name': delivery_person_name}
    messagebox.showinfo("Success", f"Delivery person {delivery_person_name} added successfully.")

# Function to add or update subscriptions for a customer
def update_subscription():
    customer_id = simpledialog.askstring("Input", "Enter Customer ID:")
    if customer_id not in customers:
        messagebox.showerror("Error", "Customer not found!")
        return
    
    subscriptions_list = simpledialog.askstring("Input", "Enter Subscribed Publications (comma separated):")
    subscriptions_list = subscriptions_list.split(',')
    customers[customer_id]['subscriptions'] = subscriptions_list
    messagebox.showinfo("Success", "Subscription list updated successfully.")

# Function to process a delivery person's daily task
def process_delivery():
    delivery_person_id = simpledialog.askstring("Input", "Enter Delivery Person ID:")
    if delivery_person_id not in delivery_persons:
        messagebox.showerror("Error", "Delivery person not found!")
        return
    
    today = datetime.date.today()
    delivery = []
    for customer_id, customer in customers.items():
        if customer_id in subscriptions:
            delivery.append((customer_id, customer['subscriptions']))
    
    deliveries[delivery_person_id] = delivery
    messagebox.showinfo("Success", "Delivery processed successfully.")

# Function to print daily publication deliveries for each delivery person
def print_daily_deliveries():
    delivery_person_id = simpledialog.askstring("Input", "Enter Delivery Person ID:")
    if delivery_person_id not in deliveries:
        messagebox.showerror("Error", "No deliveries found for this person.")
        return
    
    delivery = deliveries[delivery_person_id]
    for customer_id, subscriptions in delivery:
        messagebox.showinfo("Deliveries", f"Customer {customer_id} will receive: {', '.join(subscriptions)}.")

# Function to generate bill for a customer
def generate_bill():
    customer_id = simpledialog.askstring("Input", "Enter Customer ID:")
    if customer_id not in customers:
        messagebox.showerror("Error", "Customer not found!")
        return
    
    customer = customers[customer_id]
    total_cost = 0
    for publication in customer['subscriptions']:
        total_cost += publication_cost.get(publication.strip().lower(), 0)
    
    customers[customer_id]['payment_due'] = total_cost
    messagebox.showinfo("Bill", f"Bill for {customer['name']} is: {total_cost}")

# Function to handle customer payments
def handle_payment():
    customer_id = simpledialog.askstring("Input", "Enter Customer ID:")
    if customer_id not in customers:
        messagebox.showerror("Error", "Customer not found!")
        return
    
    payment_method = simpledialog.askstring("Input", "Enter payment method (Cheque/Cash):")
    if payment_method.lower() == 'cheque':
        cheque_number = simpledialog.askstring("Input", "Enter Cheque Number:")
        payments[customer_id] = {'method': 'Cheque', 'cheque_number': cheque_number}
    elif payment_method.lower() == 'cash':
        payments[customer_id] = {'method': 'Cash'}
    else:
        messagebox.showerror("Error", "Invalid payment method!")
        return
    
    payment_amount = simpledialog.askfloat("Input", f"Enter amount for {customers[customer_id]['name']}:")
    if payment_amount < customers[customer_id]['payment_due']:
        customers[customer_id]['outstanding'] += customers[customer_id]['payment_due'] - payment_amount
        messagebox.showinfo("Payment", f"Payment received. Outstanding balance: {customers[customer_id]['outstanding']}")
    else:
        customers[customer_id]['outstanding'] = 0
        customers[customer_id]['payment_due'] = 0
        messagebox.showinfo("Payment", "Payment completed, no outstanding balance.")

# Function to generate delivery boy's commission
def calculate_delivery_boy_commission():
    delivery_person_id = simpledialog.askstring("Input", "Enter Delivery Person ID:")
    if delivery_person_id not in deliveries:
        messagebox.showerror("Error", "No deliveries found for this person.")
        return
    
    total_value = 0
    for customer_id, subscriptions in deliveries[delivery_person_id]:
        for publication in subscriptions:
            total_value += publication_cost.get(publication.strip().lower(), 0)
    
    commission = total_value * 0.025  # 2.5% commission
    messagebox.showinfo("Commission", f"Total commission for Delivery Person {delivery_person_id} is: {commission}")

# Function to print reminder for customers with outstanding dues
def print_reminders():
    for customer_id, customer in customers.items():
        if customer['outstanding'] > 0:
            messagebox.showinfo("Reminder", f"Customer {customer_id} has an outstanding balance of {customer['outstanding']}.")

# Function to save data to CSV
def save_data_to_csv():
    with open('customers.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Customer ID', 'Customer Name', 'Subscriptions', 'Outstanding', 'Payment Due'])
        for customer_id, customer in customers.items():
            writer.writerow([customer_id, customer['name'], ','.join(customer['subscriptions']), customer['outstanding'], customer['payment_due']])
    
    with open('payments.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Customer ID', 'Payment Method', 'Cheque Number', 'Payment Amount'])
        for customer_id, payment in payments.items():
            writer.writerow([customer_id, payment['method'], payment.get('cheque_number', ''), customer['payment_due']])

    messagebox.showinfo("Success", "Data saved to CSV files.")

# Function to load data from CSV
def load_data_from_csv():
    global customers, payments
    customers = {}
    payments = {}

    try:
        with open('customers.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                customer_id, customer_name, subscriptions, outstanding, payment_due = row
                customers[customer_id] = {
                    'name': customer_name,
                    'subscriptions': subscriptions.split(','),
                    'outstanding': float(outstanding),
                    'payment_due': float(payment_due)
                }

        with open('payments.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                customer_id, payment_method, cheque_number, payment_amount = row
                payments[customer_id] = {'method': payment_method, 'cheque_number': cheque_number, 'payment_amount': float(payment_amount)}
        
        messagebox.showinfo("Success", "Data loaded from CSV files.")
    except FileNotFoundError:
        messagebox.showerror("Error", "CSV files not found.")

# GUI Setup
root = tk.Tk()
root.title("Newspaper Agency Automation")
root.geometry('400x600')  # Set window size

# Set modern fonts
font = ('Helvetica', 12)

# Create buttons for different functionalities
button_add_customer = tk.Button(root, text="Add Customer", command=add_customer, font=font)
button_add_customer.pack(pady=5)

button_add_delivery_person = tk.Button(root, text="Add Delivery Person", command=add_delivery_person, font=font)
button_add_delivery_person.pack(pady=5)

button_update_subscription = tk.Button(root, text="Update Subscription", command=update_subscription, font=font)
button_update_subscription.pack(pady=5)

button_process_delivery = tk.Button(root, text="Process Delivery", command=process_delivery, font=font)
button_process_delivery.pack(pady=5)

button_print_daily_deliveries = tk.Button(root, text="Print Daily Deliveries", command=print_daily_deliveries, font=font)
button_print_daily_deliveries.pack(pady=5)

button_generate_bill = tk.Button(root, text="Generate Bill", command=generate_bill, font=font)
button_generate_bill.pack(pady=5)

button_handle_payment = tk.Button(root, text="Handle Payment", command=handle_payment, font=font)
button_handle_payment.pack(pady=5)

button_calculate_commission = tk.Button(root, text="Calculate Delivery Boy Commission", command=calculate_delivery_boy_commission, font=font)
button_calculate_commission.pack(pady=5)

button_print_reminders = tk.Button(root, text="Print Reminders", command=print_reminders, font=font)
button_print_reminders.pack(pady=5)

button_save_data = tk.Button(root, text="Save Data to CSV", command=save_data_to_csv, font=font)
button_save_data.pack(pady=5)

button_load_data = tk.Button(root, text="Load Data from CSV", command=load_data_from_csv, font=font)
button_load_data.pack(pady=5)

# Run the Tkinter mainloop
root.mainloop()
