import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from datetime import datetime
import csv

# Data Structures
medicines = {}  # Stores medicine code, name, vendor, quantity, expiry, prices
vendors = {}  # Stores vendor details
sales_data = []  # Stores sales data
inventory_data = []  # Stores inventory details

# Function to generate Medicine Code
def generate_medicine_code():
    return len(medicines) + 1

# Function to add new medicine
def add_new_medicine(trade_name, generic_name, vendor_list, selling_price, purchasing_price):
    medicine_code = generate_medicine_code()
    medicines[medicine_code] = {
        'trade_name': trade_name,
        'generic_name': generic_name,
        'vendors': vendor_list,
        'selling_price': selling_price,
        'purchasing_price': purchasing_price,
        'quantity': 0,
        'expiry_date': None
    }
    return medicine_code

# Function to add Vendor
def add_vendor(vendor_name, vendor_address, vendor_code):
    vendors[vendor_code] = {'name': vendor_name, 'address': vendor_address}
    return vendor_code

# Function to update stock with new supplies
def update_stock(medicine_code, quantity, batch_number, expiry_date, vendor_code):
    if medicine_code in medicines:
        medicines[medicine_code]['quantity'] += quantity
        medicines[medicine_code]['expiry_date'] = expiry_date
        inventory_data.append({
            'medicine_code': medicine_code,
            'quantity': quantity,
            'batch_number': batch_number,
            'expiry_date': expiry_date,
            'vendor_code': vendor_code
        })
    else:
        messagebox.showerror("Error", "Medicine not found!")

# Function to calculate threshold quantity for reordering
def calculate_threshold(medicine_code):
    weekly_sales_avg = sum(sale['quantity'] for sale in sales_data) // len(sales_data) if sales_data else 0
    threshold = weekly_sales_avg * 7
    return threshold

# Function to track expired medicines
def track_expired_medicines():
    expired_medicines = []
    for medicine_code, details in medicines.items():
        if details['expiry_date'] and details['expiry_date'] < datetime.now():
            expired_medicines.append({
                'medicine_code': medicine_code,
                'trade_name': details['trade_name'],
                'expiry_date': details['expiry_date'],
                'vendors': details['vendors']
            })
    return expired_medicines

# Function to generate vendor-wise expired items
def expired_vendor_report():
    expired_items = track_expired_medicines()
    vendor_expired_report = {}
    
    for item in expired_items:
        for vendor_code in item['vendors']:
            vendor = vendors.get(vendor_code)
            if vendor:
                if vendor['name'] not in vendor_expired_report:
                    vendor_expired_report[vendor['name']] = []
                vendor_expired_report[vendor['name']].append(item)
    
    return vendor_expired_report

# Function to process sales
def process_sale(medicine_code, quantity_sold):
    if medicine_code in medicines:
        if medicines[medicine_code]['quantity'] >= quantity_sold:
            medicines[medicine_code]['quantity'] -= quantity_sold
            sales_data.append({
                'medicine_code': medicine_code,
                'quantity': quantity_sold,
                'date': datetime.now()
            })
            receipt = f"Receipt\nMedicine: {medicines[medicine_code]['trade_name']}\nQuantity Sold: {quantity_sold}\nTotal: {medicines[medicine_code]['selling_price'] * quantity_sold}"
            return receipt
        else:
            return "Not enough stock available!"
    else:
        return "Medicine not found!"

# Function to generate a vendor-wise payment report
def vendor_payment_report():
    payments = {}
    for sale in sales_data:
        medicine_code = sale['medicine_code']
        quantity_sold = sale['quantity']
        medicine_details = medicines[medicine_code]
        for vendor_code in medicine_details['vendors']:
            vendor = vendors.get(vendor_code)
            if vendor:
                payment = medicine_details['purchasing_price'] * quantity_sold
                if vendor['name'] not in payments:
                    payments[vendor['name']] = 0
                payments[vendor['name']] += payment
    return payments

# Function to display a simple message in the GUI
def display_message(message):
    messagebox.showinfo("Message", message)

# Function to load data from CSV files
def load_csv_data():
    # Load medicines
    try:
        file_path = filedialog.askopenfilename(title="Select Medicines CSV File", filetypes=[("CSV Files", "*.csv")])
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                trade_name, generic_name, vendors_list, selling_price, purchasing_price = row
                vendors_list = vendors_list.split(',')
                add_new_medicine(trade_name, generic_name, vendors_list, float(selling_price), float(purchasing_price))
        display_message("Medicines loaded successfully from CSV!")
    except Exception as e:
        display_message(f"Error loading CSV: {str(e)}")

# GUI setup
def run_gui():
    def add_medicine_gui():
        trade_name = trade_name_entry.get()
        generic_name = generic_name_entry.get()
        vendor_list = vendor_entry.get().split(',')
        selling_price = float(selling_price_entry.get())
        purchasing_price = float(purchasing_price_entry.get())
        code = add_new_medicine(trade_name, generic_name, vendor_list, selling_price, purchasing_price)
        display_message(f"New medicine added with code: {code}")

    def update_stock_gui():
        medicine_code = int(medicine_code_entry.get())
        quantity = int(quantity_entry.get())
        batch_number = batch_number_entry.get()
        expiry_date = expiry_date_entry.get()
        vendor_code = vendor_code_entry.get()
        update_stock(medicine_code, quantity, batch_number, expiry_date, vendor_code)
        display_message("Stock updated successfully!")

    def process_sale_gui():
        medicine_code = int(medicine_code_sale_entry.get())
        quantity_sold = int(quantity_sale_entry.get())
        receipt = process_sale(medicine_code, quantity_sold)
        display_message(receipt)

    root = tk.Tk()
    root.title("Medicine Shop Automation")

    font_style = ("Arial", 12)

    # Add Medicine
    tk.Label(root, text="Trade Name:", font=font_style).grid(row=0, column=0)
    trade_name_entry = tk.Entry(root, font=font_style)
    trade_name_entry.grid(row=0, column=1)

    tk.Label(root, text="Generic Name:", font=font_style).grid(row=1, column=0)
    generic_name_entry = tk.Entry(root, font=font_style)
    generic_name_entry.grid(row=1, column=1)

    tk.Label(root, text="Vendors (comma separated):", font=font_style).grid(row=2, column=0)
    vendor_entry = tk.Entry(root, font=font_style)
    vendor_entry.grid(row=2, column=1)

    tk.Label(root, text="Selling Price:", font=font_style).grid(row=3, column=0)
    selling_price_entry = tk.Entry(root, font=font_style)
    selling_price_entry.grid(row=3, column=1)

    tk.Label(root, text="Purchasing Price:", font=font_style).grid(row=4, column=0)
    purchasing_price_entry = tk.Entry(root, font=font_style)
    purchasing_price_entry.grid(row=4, column=1)

    add_medicine_button = tk.Button(root, text="Add Medicine", font=font_style, command=add_medicine_gui)
    add_medicine_button.grid(row=5, column=1)

    # Update Stock
    tk.Label(root, text="Medicine Code:", font=font_style).grid(row=6, column=0)
    medicine_code_entry = tk.Entry(root, font=font_style)
    medicine_code_entry.grid(row=6, column=1)

    tk.Label(root, text="Quantity:", font=font_style).grid(row=7, column=0)
    quantity_entry = tk.Entry(root, font=font_style)
    quantity_entry.grid(row=7, column=1)

    tk.Label(root, text="Batch Number:", font=font_style).grid(row=8, column=0)
    batch_number_entry = tk.Entry(root, font=font_style)
    batch_number_entry.grid(row=8, column=1)

    tk.Label(root, text="Expiry Date:", font=font_style).grid(row=9, column=0)
    expiry_date_entry = tk.Entry(root, font=font_style)
    expiry_date_entry.grid(row=9, column=1)

    tk.Label(root, text="Vendor Code:", font=font_style).grid(row=10, column=0)
    vendor_code_entry = tk.Entry(root, font=font_style)
    vendor_code_entry.grid(row=10, column=1)

    update_stock_button = tk.Button(root, text="Update Stock", font=font_style, command=update_stock_gui)
    update_stock_button.grid(row=11, column=1)

    # Process Sale
    tk.Label(root, text="Medicine Code (Sale):", font=font_style).grid(row=12, column=0)
    medicine_code_sale_entry = tk.Entry(root, font=font_style)
    medicine_code_sale_entry.grid(row=12, column=1)

    tk.Label(root, text="Quantity Sold:", font=font_style).grid(row=13, column=0)
    quantity_sale_entry = tk.Entry(root, font=font_style)
    quantity_sale_entry.grid(row=13, column=1)

    process_sale_button = tk.Button(root, text="Process Sale", font=font_style, command=process_sale_gui)
    process_sale_button.grid(row=14, column=1)

    # Load CSV Data
    load_csv_button = tk.Button(root, text="Load Medicines from CSV", font=font_style, command=load_csv_data)
    load_csv_button.grid(row=15, column=1)

    root.mainloop()

run_gui()
