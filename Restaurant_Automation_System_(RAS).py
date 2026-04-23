import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import csv

# Global variables
menu = {
    "Burger": 5.0,
    "Pizza": 8.0,
    "Pasta": 6.5,
    "Salad": 4.0,
}
ingredient_stock = {
    "Bun": 50,
    "Cheese": 20,
    "Lettuce": 30,
    "Dough": 15,
    "Tomato Sauce": 10,
    "Pasta": 12,
    "Vegetables": 25,
}
ingredient_threshold = {}
sales = []
expenses = []
cash_balance = 1000.0
staff_salaries = {"Chef": 2000, "Waiter": 1500, "Manager": 2500}  # Example salaries
tables = {f"Table {i}": [] for i in range(1, 11)}  # Track orders for 10 tables

def calculate_threshold():
    for ingredient, stock in ingredient_stock.items():
        ingredient_threshold[ingredient] = max(2 * (stock // 3), 2)

def update_prices():
    def save_prices():
        for item in menu:
            try:
                new_price = float(price_vars[item].get())
                menu[item] = new_price
            except ValueError:
                messagebox.showerror("Error", f"Invalid price for {item}")
        messagebox.showinfo("Success", "Prices updated successfully!")
        price_window.destroy()

    price_window = tk.Toplevel()
    price_window.title("Update Prices")

    price_vars = {}
    for idx, item in enumerate(menu):
        tk.Label(price_window, text=item).grid(row=idx, column=0)
        price_vars[item] = tk.StringVar(value=menu[item])
        tk.Entry(price_window, textvariable=price_vars[item]).grid(row=idx, column=1)

    tk.Button(price_window, text="Save", command=save_prices).grid(row=len(menu), columnspan=2)

def generate_bill():
    def add_item():
        item = item_var.get()
        quantity = int(quantity_var.get())

        if item not in menu:
            messagebox.showerror("Error", "Invalid item")
            return

        bill_items.append((item, quantity, menu[item] * quantity))
        bill_text.insert(tk.END, f"{item} x {quantity} = ${menu[item] * quantity:.2f}\n")

    def finalize_bill():
        total = sum(item[2] for item in bill_items)
        table = table_var.get()
        if table not in tables:
            messagebox.showerror("Error", "Invalid table")
            return
        
        tables[table] = bill_items
        sales.append((datetime.date.today(), bill_items, total))
        bill_text.insert(tk.END, f"\nTotal: ${total:.2f}")

    bill_items = []
    bill_window = tk.Toplevel()
    bill_window.title("Generate Bill")

    tk.Label(bill_window, text="Table").grid(row=0, column=0)
    table_var = tk.StringVar()
    table_entry = ttk.Combobox(bill_window, textvariable=table_var, values=list(tables.keys()))
    table_entry.grid(row=0, column=1)

    tk.Label(bill_window, text="Item").grid(row=1, column=0)
    item_var = tk.StringVar()
    item_entry = ttk.Combobox(bill_window, textvariable=item_var, values=list(menu.keys()))
    item_entry.grid(row=1, column=1)

    tk.Label(bill_window, text="Quantity").grid(row=2, column=0)
    quantity_var = tk.StringVar(value="1")
    tk.Entry(bill_window, textvariable=quantity_var).grid(row=2, column=1)

    tk.Button(bill_window, text="Add", command=add_item).grid(row=3, columnspan=2)

    bill_text = tk.Text(bill_window, height=15, width=50)
    bill_text.grid(row=4, column=0, columnspan=2)

    tk.Button(bill_window, text="Finalize", command=finalize_bill).grid(row=5, columnspan=2)

def issue_ingredients():
    def issue():
        ingredient = ingredient_var.get()
        quantity = int(quantity_var.get())

        if ingredient not in ingredient_stock:
            messagebox.showerror("Error", "Invalid ingredient")
            return

        if ingredient_stock[ingredient] < quantity:
            messagebox.showerror("Error", "Insufficient stock")
            return

        ingredient_stock[ingredient] -= quantity
        messagebox.showinfo("Success", f"Issued {quantity} of {ingredient}")
        issue_window.destroy()

    issue_window = tk.Toplevel()
    issue_window.title("Issue Ingredients")

    tk.Label(issue_window, text="Ingredient").grid(row=0, column=0)
    ingredient_var = tk.StringVar()
    ingredient_entry = ttk.Combobox(issue_window, textvariable=ingredient_var, values=list(ingredient_stock.keys()))
    ingredient_entry.grid(row=0, column=1)

    tk.Label(issue_window, text="Quantity").grid(row=1, column=0)
    quantity_var = tk.StringVar(value="1")
    tk.Entry(issue_window, textvariable=quantity_var).grid(row=1, column=1)

    tk.Button(issue_window, text="Issue", command=issue).grid(row=2, columnspan=2)

def generate_purchase_orders():
    calculate_threshold()
    orders = []

    for ingredient, stock in ingredient_stock.items():
        if stock < ingredient_threshold[ingredient]:
            orders.append((ingredient, ingredient_threshold[ingredient] - stock))

    if not orders:
        messagebox.showinfo("No Orders", "All ingredients are sufficiently stocked.")
        return

    orders_window = tk.Toplevel()
    orders_window.title("Purchase Orders")

    tk.Label(orders_window, text="Purchase Orders").grid(row=0, column=0)
    orders_text = tk.Text(orders_window, height=10, width=50)
    orders_text.grid(row=1, column=0)

    for ingredient, quantity in orders:
        orders_text.insert(tk.END, f"{ingredient}: {quantity}\n")

def record_invoice():
    def save_invoice():
        ingredient = ingredient_var.get()
        quantity = int(quantity_var.get())
        cost = float(cost_var.get())

        ingredient_stock[ingredient] += quantity
        expenses.append((datetime.date.today(), cost))

        global cash_balance
        if cash_balance >= cost:
            cash_balance -= cost
            messagebox.showinfo("Success", "Invoice recorded and cheque issued.")
        else:
            messagebox.showwarning("Warning", "Invoice recorded, but insufficient cash for cheque.")

        invoice_window.destroy()

    invoice_window = tk.Toplevel()
    invoice_window.title("Record Invoice")

    tk.Label(invoice_window, text="Ingredient").grid(row=0, column=0)
    ingredient_var = tk.StringVar()
    ingredient_entry = ttk.Combobox(invoice_window, textvariable=ingredient_var, values=list(ingredient_stock.keys()))
    ingredient_entry.grid(row=0, column=1)

    tk.Label(invoice_window, text="Quantity").grid(row=1, column=0)
    quantity_var = tk.StringVar(value="1")
    tk.Entry(invoice_window, textvariable=quantity_var).grid(row=1, column=1)

    tk.Label(invoice_window, text="Cost").grid(row=2, column=0)
    cost_var = tk.StringVar(value="0.0")
    tk.Entry(invoice_window, textvariable=cost_var).grid(row=2, column=1)

    tk.Button(invoice_window, text="Save", command=save_invoice).grid(row=3, columnspan=2)

def generate_reports():
    def show_reports():
        report_text.delete("1.0", tk.END)
        report_text.insert(tk.END, "Monthly Sales:\n")
        for sale in sales:
            report_text.insert(tk.END, f"{sale}\n")
        report_text.insert(tk.END, "\nMonthly Expenses:\n")
        for expense in expenses:
            report_text.insert(tk.END, f"{expense}\n")
        report_text.insert(tk.END, f"\nCurrent Cash Balance: ${cash_balance:.2f}")
        report_text.insert(tk.END, "\n\nStaff Salaries:") 
        for staff, salary in staff_salaries.items():
            report_text.insert(tk.END, f"{staff}: ${salary}\n")
        report_text.insert(tk.END, "\n\nOrders by Table:")
        for table, orders in tables.items():
            report_text.insert(tk.END, f"{table}: {orders}\n")

    report_window = tk.Toplevel()
    report_window.title("Reports")

    report_text = tk.Text(report_window, height=20, width=70)
    report_text.grid(row=0, column=0)

    tk.Button(report_window, text="Refresh", command=show_reports).grid(row=1, column=0)
    show_reports()

def print_menu():
    menu_window = tk.Toplevel()
    menu_window.title("Menu")

    menu_text = tk.Text(menu_window, height=15, width=50)
    menu_text.grid(row=0, column=0)

    for item, price in menu.items():
        menu_text.insert(tk.END, f"{item}: ${price:.2f}\n")

def import_csv():
    def load_csv():
        try:
            with open('menu.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    item, price = row
                    menu[item] = float(price)
            messagebox.showinfo("Success", "Menu loaded successfully from CSV!")
            csv_window.destroy()
        except FileNotFoundError:
            messagebox.showerror("Error", "CSV file not found.")

    csv_window = tk.Toplevel()
    csv_window.title("Import Menu from CSV")

    tk.Button(csv_window, text="Load CSV", command=load_csv).grid(row=0, column=0)

# Main GUI setup
root = tk.Tk()
root.title("Restaurant Automation System")

# Set the default font for all widgets
root.option_add("*Font", "Arial 12")

buttons = [
    ("Update Prices", update_prices),
    ("Generate Bill", generate_bill),
    ("Issue Ingredients", issue_ingredients),
    ("Generate Purchase Orders", generate_purchase_orders),
    ("Record Invoice", record_invoice),
    ("Generate Reports", generate_reports),
    ("Print Menu", print_menu),
    ("Import Menu CSV", import_csv),
]

for idx, (text, command) in enumerate(buttons):
    tk.Button(root, text=text, command=command, width=30).grid(row=idx, column=0, pady=5)

root.mainloop()
