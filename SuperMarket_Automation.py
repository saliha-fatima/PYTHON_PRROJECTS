import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font
import csv
from datetime import datetime

# Global Variables
inventory = {}
sales = []
serial_number = 1
total_profit = 0
low_stock_threshold = 5
users = {"admin": "admin123"}  # Default admin user

def reset_globals():
    """Initialize global variables."""
    global inventory, sales, serial_number, total_profit
    inventory = {}
    sales = []
    serial_number = 1
    total_profit = 0

def show_register_window():
    """Show the registration window."""
    login_window.withdraw()  # Hide login window
    register_window.deiconify()  # Show registration window

def register_user():
    """Register a new user."""
    username = reg_username_entry.get()
    password = reg_password_entry.get()

    if username and password:
        if username in users:
            messagebox.showerror("Registration Error", "Username already exists")
        else:
            users[username] = password
            messagebox.showinfo("Registration Successful", "User registered successfully. Now, please login.")
            reg_username_entry.delete(0, tk.END)  # Clear the registration fields
            reg_password_entry.delete(0, tk.END)
            register_window.withdraw()
            login_window.deiconify()  # Show login window after registration
    else:
        messagebox.showerror("Registration Error", "Please fill out both fields")

def authenticate_user():
    """Authenticate user."""
    username = username_entry.get()
    password = password_entry.get()

    if users.get(username) == password:
        messagebox.showinfo("Login Successful", "Welcome!")
        login_window.destroy()  # Close login window
        root.deiconify()  # Show main window
    else:
        messagebox.showerror("Login Error", "Invalid credentials")

def add_to_inventory():
    """Add items to the inventory."""
    try:
        item_name = item_name_entry.get().strip()
        code = item_code_entry.get().strip()
        quantity = int(item_quantity_entry.get())
        unit_price = float(item_price_entry.get())
        cost_price = float(item_cost_price_entry.get())

        if not item_name or not code:
            raise ValueError("Fields cannot be empty")

        if code in inventory:
            inventory[code]['quantity'] += quantity
        else:
            inventory[code] = {
                'name': item_name,
                'quantity': quantity,
                'unit_price': unit_price,
                'cost_price': cost_price
            }

        update_inventory_list()
        messagebox.showinfo("Success", "Item added to inventory")
    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input: {e}")

def update_inventory_list():
    """Update the inventory list displayed in the GUI."""
    inventory_list.delete(*inventory_list.get_children())
    for code, details in inventory.items():
        inventory_list.insert("", "end", values=(details['name'], code, details['quantity'], details['unit_price'], details['cost_price']))

        # Low stock alert
        if details['quantity'] <= low_stock_threshold:
            inventory_list.item(code, tags='low_stock')

def process_sale():
    """Process a sales transaction."""
    global serial_number, total_profit

    try:
        code = sale_code_entry.get().strip()
        quantity = int(sale_quantity_entry.get())

        if code in inventory and inventory[code]['quantity'] >= quantity:
            item = inventory[code]
            item_price = item['unit_price'] * quantity
            profit = (item['unit_price'] - item['cost_price']) * quantity

            inventory[code]['quantity'] -= quantity
            sales.append({
                'serial': serial_number,
                'name': item['name'],
                'code': code,
                'quantity': quantity,
                'unit_price': item['unit_price'],
                'item_price': item_price,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Adding date to sale record
            })

            serial_number += 1
            total_profit += profit

            update_inventory_list()
            print_bill(serial_number - 1, item['name'], code, quantity, item['unit_price'], item_price)
        else:
            messagebox.showerror("Error", "Insufficient stock or invalid code")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical inputs")

def print_bill(serial, name, code, quantity, unit_price, item_price):
    """Display the sales bill."""
    bill_text.delete("1.0", tk.END)
    bill_text.insert(tk.END, f"Serial Number: {serial}\n")
    bill_text.insert(tk.END, f"Item Name: {name}\n")
    bill_text.insert(tk.END, f"Code Number: {code}\n")
    bill_text.insert(tk.END, f"Quantity: {quantity}\n")
    bill_text.insert(tk.END, f"Unit Price: {unit_price:.2f}\n")
    bill_text.insert(tk.END, f"Item Price: {item_price:.2f}\n")
    bill_text.insert(tk.END, f"Total Amount Payable: {item_price:.2f}\n")

def view_sales_statistics():
    """Display sales statistics."""
    sales_list.delete(*sales_list.get_children())
    for sale in sales:
        sales_list.insert("", "end", values=(sale['serial'], sale['name'], sale['code'], sale['quantity'], sale['unit_price'], sale['item_price'], sale['date']))

    profit_label.config(text=f"Total Profit: {total_profit:.2f}")

def export_inventory_to_csv():
    """Export inventory data to a CSV file."""
    try:
        with open('inventory.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Code", "Quantity", "Unit Price", "Cost Price"])
            for code, details in inventory.items():
                writer.writerow([details['name'], code, details['quantity'], details['unit_price'], details['cost_price']])
        messagebox.showinfo("Success", "Inventory exported to inventory.csv")
    except Exception as e:
        messagebox.showerror("Error", f"Error exporting inventory: {e}")

def export_sales_to_csv():
    """Export sales data to a CSV file."""
    try:
        with open('sales.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Serial", "Name", "Code", "Quantity", "Unit Price", "Item Price", "Date"])
            for sale in sales:
                writer.writerow([sale['serial'], sale['name'], sale['code'], sale['quantity'], sale['unit_price'], sale['item_price'], sale['date']])
        messagebox.showinfo("Success", "Sales exported to sales.csv")
    except Exception as e:
        messagebox.showerror("Error", f"Error exporting sales: {e}")

# GUI Setup
root = tk.Tk()
root.title("Supermarket Automation System")
root.geometry("900x650")

# Set global font
app_font = font.nametofont("TkDefaultFont").copy()
app_font.actual()['size'] = 12

# Login Window (For Admin Authentication)
login_window = tk.Toplevel(root)
login_window.title("Login")
login_window.geometry("300x200")
login_window.protocol("WM_DELETE_WINDOW", root.quit)  # Prevent closing login window directly

ttk.Label(login_window, text="Username:", font=app_font).pack(pady=5)
username_entry = ttk.Entry(login_window, font=app_font)
username_entry.pack(pady=5)

ttk.Label(login_window, text="Password:", font=app_font).pack(pady=5)
password_entry = ttk.Entry(login_window, font=app_font, show="*")
password_entry.pack(pady=5)

ttk.Button(login_window, text="Login", command=authenticate_user, style="TButton").pack(pady=5)
ttk.Button(login_window, text="Don't have an account? Register", command=show_register_window, style="TButton").pack(pady=5)

# Registration Window
register_window = tk.Toplevel(root)
register_window.title("Register")
register_window.geometry("300x200")
register_window.withdraw()  # Initially hidden

ttk.Label(register_window, text="Username:", font=app_font).pack(pady=5)
reg_username_entry = ttk.Entry(register_window, font=app_font)
reg_username_entry.pack(pady=5)

ttk.Label(register_window, text="Password:", font=app_font).pack(pady=5)
reg_password_entry = ttk.Entry(register_window, font=app_font, show="*")
reg_password_entry.pack(pady=5)

ttk.Button(register_window, text="Register", command=register_user, style="TButton").pack(pady=5)
ttk.Button(register_window, text="Already have an account? Login", command=show_register_window, style="TButton").pack(pady=5)

root.withdraw()  # Hide the main window initially

# Inventory Management Frame
inventory_frame = ttk.LabelFrame(root, text="Inventory Management", padding=(10, 5))
inventory_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(inventory_frame, text="Item Name", font=app_font).grid(row=0, column=0, padx=5, pady=5)
item_name_entry = ttk.Entry(inventory_frame, font=app_font)
item_name_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(inventory_frame, text="Code", font=app_font).grid(row=0, column=2, padx=5, pady=5)
item_code_entry = ttk.Entry(inventory_frame, font=app_font)
item_code_entry.grid(row=0, column=3, padx=5, pady=5)

ttk.Label(inventory_frame, text="Quantity", font=app_font).grid(row=1, column=0, padx=5, pady=5)
item_quantity_entry = ttk.Entry(inventory_frame, font=app_font)
item_quantity_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(inventory_frame, text="Unit Price", font=app_font).grid(row=1, column=2, padx=5, pady=5)
item_price_entry = ttk.Entry(inventory_frame, font=app_font)
item_price_entry.grid(row=1, column=3, padx=5, pady=5)

ttk.Label(inventory_frame, text="Cost Price", font=app_font).grid(row=2, column=0, padx=5, pady=5)
item_cost_price_entry = ttk.Entry(inventory_frame, font=app_font)
item_cost_price_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Button(inventory_frame, text="Add to Inventory", command=add_to_inventory, style="TButton").grid(row=2, column=3, padx=5, pady=5)

inventory_list = ttk.Treeview(inventory_frame, columns=("Name", "Code", "Quantity", "Unit Price", "Cost Price"), show="headings", style="Treeview")
for col in ["Name", "Code", "Quantity", "Unit Price", "Cost Price"]:
    inventory_list.heading(col, text=col)
inventory_list.grid(row=3, column=0, columnspan=4, pady=5)

# Sales Transaction Frame
sales_frame = ttk.LabelFrame(root, text="Sales Transaction", padding=(10, 5))
sales_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(sales_frame, text="Code", font=app_font).grid(row=0, column=0, padx=5, pady=5)
sale_code_entry = ttk.Entry(sales_frame, font=app_font)
sale_code_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(sales_frame, text="Quantity", font=app_font).grid(row=0, column=2, padx=5, pady=5)
sale_quantity_entry = ttk.Entry(sales_frame, font=app_font)
sale_quantity_entry.grid(row=0, column=3, padx=5, pady=5)

ttk.Button(sales_frame, text="Process Sale", command=process_sale, style="TButton").grid(row=0, column=4, padx=5, pady=5)

bill_text = tk.Text(sales_frame, height=10, width=80, font=app_font)
bill_text.grid(row=1, column=0, columnspan=5, pady=5)

# Sales Statistics Frame
statistics_frame = ttk.LabelFrame(root, text="Sales Statistics", padding=(10, 5))
statistics_frame.pack(fill="x", padx=10, pady=5)

sales_list = ttk.Treeview(statistics_frame, columns=("Serial", "Name", "Code", "Quantity", "Unit Price", "Item Price", "Date"), show="headings", style="Treeview")
for col in ["Serial", "Name", "Code", "Quantity", "Unit Price", "Item Price", "Date"]:
    sales_list.heading(col, text=col)
sales_list.pack(fill="x", pady=5)

ttk.Button(statistics_frame, text="View Sales Statistics", command=view_sales_statistics, style="TButton").pack(pady=5)
profit_label = ttk.Label(statistics_frame, text="Total Profit: 0.00", font=app_font)
profit_label.pack()

# Export Buttons
export_frame = ttk.LabelFrame(root, text="Export Data", padding=(10, 5))
export_frame.pack(fill="x", padx=10, pady=5)

ttk.Button(export_frame, text="Export Inventory to CSV", command=export_inventory_to_csv, style="TButton").pack(side="left", padx=10, pady=5)
ttk.Button(export_frame, text="Export Sales to CSV", command=export_sales_to_csv, style="TButton").pack(side="left", padx=10, pady=5)

reset_globals()  # Initialize variables
root.mainloop()
