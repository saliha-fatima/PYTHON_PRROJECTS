import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import csv

# Global variables to store data
inventory = {}
sales_data = {}
parts_sold = {}

# Function to update inventory based on daily sales
def update_inventory(part_number, quantity_sold):
    if part_number in inventory:
        inventory[part_number] -= quantity_sold
        if inventory[part_number] < 0:
            inventory[part_number] = 0
    else:
        inventory[part_number] = 0

# Function to add new sales data
def add_sale(part_number, quantity_sold):
    if part_number not in sales_data:
        sales_data[part_number] = []
    sales_data[part_number].append(quantity_sold)
    update_inventory(part_number, quantity_sold)

# Function to calculate the weekly average sales
def calculate_weekly_sales(part_number):
    if part_number in sales_data:
        sales = sales_data[part_number]
        avg_sales = sum(sales[-7:]) / len(sales[-7:]) if len(sales) >= 7 else sum(sales) / len(sales)
        return avg_sales
    return 0

# Function to calculate the threshold value for ordering
def calculate_threshold(part_number):
    avg_sales = calculate_weekly_sales(part_number)
    return avg_sales * 7  # Assuming 1 week of stock required

# Function to generate orders
def generate_orders():
    order_list = []
    for part_number, stock in inventory.items():
        threshold = calculate_threshold(part_number)
        if stock < threshold:
            amount_required = threshold - stock
            order_list.append((part_number, amount_required, "Vendor Address"))  # Placeholder for vendor address
    return order_list

# Function to calculate daily revenue
def calculate_daily_revenue():
    revenue = 0
    for part_number, sales in sales_data.items():
        revenue += sum(sales)
    return revenue

# Function to show the sales graph for the month
def show_sales_graph():
    days = list(range(1, len(sales_data.get(list(sales_data.keys())[0], [])) + 1))
    sales_by_day = [sum([sales_data[part][day-1] for part in sales_data]) for day in days]

    plt.plot(days, sales_by_day, label="Sales")
    plt.xlabel("Days of the Month")
    plt.ylabel("Total Sales")
    plt.title("Sales for Each Day of the Month")
    plt.legend()
    plt.show()

# Save data to CSV
def save_data():
    try:
        # Save inventory data
        with open('inventory.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Part Number", "Stock"])
            for part_number, stock in inventory.items():
                writer.writerow([part_number, stock])

        # Save sales data
        with open('sales_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Part Number", "Sales"])
            for part_number, sales in sales_data.items():
                writer.writerow([part_number, ','.join(map(str, sales))])

        messagebox.showinfo("Success", "Data saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving data: {e}")

# Load data from CSV
def load_data():
    try:
        # Load inventory data
        with open('inventory.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                inventory[row[0]] = int(row[1])

        # Load sales data
        with open('sales_data.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                sales_data[row[0]] = list(map(int, row[1].split(',')))

        messagebox.showinfo("Success", "Data loaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error loading data: {e}")

# GUI to interact with the program
def create_gui():
    def add_part_sale():
        part_number = entry_part_number.get()
        try:
            quantity_sold = int(entry_quantity_sold.get())
            add_sale(part_number, quantity_sold)
            messagebox.showinfo("Success", f"Sale added for part {part_number}.")
            entry_part_number.delete(0, tk.END)
            entry_quantity_sold.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity.")

    def show_orders():
        orders = generate_orders()
        orders_text.delete(1.0, tk.END)
        for order in orders:
            orders_text.insert(tk.END, f"Part: {order[0]}, Amount: {order[1]}, Vendor: {order[2]}\n")

    def show_revenue():
        revenue = calculate_daily_revenue()
        messagebox.showinfo("Daily Revenue", f"Total revenue for the day: {revenue}")

    def plot_graph():
        show_sales_graph()

    root = tk.Tk()
    root.title("Motor Parts Shop Software")
    root.geometry("600x500")

    # Styling using ttk
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 12), padding=6)
    style.configure('TLabel', font=('Arial', 12))
    style.configure('TEntry', font=('Arial', 12))
    style.configure('TText', font=('Arial', 12))

    tk.Label(root, text="Part Number:").grid(row=0, column=0)
    tk.Label(root, text="Quantity Sold:").grid(row=1, column=0)

    entry_part_number = ttk.Entry(root)
    entry_quantity_sold = ttk.Entry(root)

    entry_part_number.grid(row=0, column=1)
    entry_quantity_sold.grid(row=1, column=1)

    ttk.Button(root, text="Add Sale", command=add_part_sale).grid(row=2, column=0, columnspan=2)
    ttk.Button(root, text="Show Orders", command=show_orders).grid(row=3, column=0, columnspan=2)
    ttk.Button(root, text="Show Revenue", command=show_revenue).grid(row=4, column=0, columnspan=2)
    ttk.Button(root, text="Show Sales Graph", command=plot_graph).grid(row=5, column=0, columnspan=2)
    ttk.Button(root, text="Save Data", command=save_data).grid(row=7, column=0, columnspan=2)
    ttk.Button(root, text="Load Data", command=load_data).grid(row=8, column=0, columnspan=2)

    orders_text = tk.Text(root, height=10, width=50)
    orders_text.grid(row=6, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
