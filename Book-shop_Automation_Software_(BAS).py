import tkinter as tk
from tkinter import messagebox, ttk
import csv
import datetime

# Sample Data
inventory = {
    "9781234567897": {"title": "Sample Book 1", "author": "Author 1", "price": 200, "copies": 10, "rack": "A1", "publisher": "Pub1", "stockist": "Stockist1, Address1"},
    "9789876543210": {"title": "Sample Book 2", "author": "Author 2", "price": 300, "copies": 5, "rack": "B2", "publisher": "Pub2", "stockist": "Stockist2, Address2"}
}
requests = {}
sales = []

def search_book():
    search_term = search_var.get()
    results_list.delete(0, tk.END)
    for isbn, details in inventory.items():
        if search_term.lower() in details['title'].lower() or search_term.lower() in details['author'].lower():
            results_list.insert(tk.END, f"{details['title']} by {details['author']} - {details['copies']} copies in Rack {details['rack']}")
    if not results_list.size():
        messagebox.showinfo("Not Found", "Book not found. Please add details for future procurement.")
        add_request(search_term)

def add_request(book_details):
    if book_details not in requests:
        requests[book_details] = 1
    else:
        requests[book_details] += 1
    messagebox.showinfo("Request Added", f"Request for '{book_details}' has been recorded.")

def purchase_book():
    isbn = isbn_var.get()
    if isbn in inventory and inventory[isbn]['copies'] > 0:
        inventory[isbn]['copies'] -= 1
        sales.append({
            "isbn": isbn,
            "title": inventory[isbn]['title'],
            "publisher": inventory[isbn]['publisher'],
            "copies": 1,
            "revenue": inventory[isbn]['price']
        })
        messagebox.showinfo("Purchase Successful", f"Purchase successful for '{inventory[isbn]['title']}'.")
    else:
        messagebox.showerror("Out of Stock", "The book is out of stock or does not exist.")

def update_inventory():
    isbn = isbn_var.get()
    new_copies = int(copies_var.get())
    if isbn in inventory:
        inventory[isbn]['copies'] += new_copies
        messagebox.showinfo("Inventory Updated", f"{new_copies} copies of '{inventory[isbn]['title']}' added to inventory.")
    else:
        title, author, price, rack, publisher, stockist = title_var.get(), author_var.get(), float(price_var.get()), rack_var.get(), publisher_var.get(), stockist_var.get()
        inventory[isbn] = {
            "title": title, "author": author, "price": price, "copies": new_copies, "rack": rack, "publisher": publisher, "stockist": stockist
        }
        messagebox.showinfo("Inventory Added", f"New book '{title}' added to inventory.")

def view_requests():
    request_list.delete(0, tk.END)
    for book, count in requests.items():
        request_list.insert(tk.END, f"{book}: {count} requests")

def generate_sales_stats():
    stats_list.delete(0, tk.END)
    stats = {}
    for sale in sales:
        if sale['isbn'] not in stats:
            stats[sale['isbn']] = {"title": sale['title'], "publisher": sale['publisher'], "copies": 0, "revenue": 0}
        stats[sale['isbn']]['copies'] += sale['copies']
        stats[sale['isbn']]['revenue'] += sale['revenue']
    for isbn, data in stats.items():
        stats_list.insert(tk.END, f"{data['title']} ({data['publisher']}): {data['copies']} sold, Revenue: {data['revenue']}")

def low_stock_report():
    report_list.delete(0, tk.END)
    threshold = 5
    for isbn, details in inventory.items():
        if details['copies'] < threshold:
            report_list.insert(tk.END, f"{details['title']} - {threshold - details['copies']} to be procured ({details['stockist']})")

# Export data to CSV
def export_inventory():
    with open('inventory.csv', 'w', newline='') as csvfile:
        fieldnames = ['ISBN', 'Title', 'Author', 'Price', 'Copies', 'Rack', 'Publisher', 'Stockist']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for isbn, details in inventory.items():
            writer.writerow({
                'ISBN': isbn, 'Title': details['title'], 'Author': details['author'], 'Price': details['price'], 
                'Copies': details['copies'], 'Rack': details['rack'], 'Publisher': details['publisher'], 'Stockist': details['stockist']
            })
    messagebox.showinfo("Export Successful", "Inventory data exported to inventory.csv.")

def export_sales():
    with open('sales.csv', 'w', newline='') as csvfile:
        fieldnames = ['ISBN', 'Title', 'Publisher', 'Copies', 'Revenue']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for sale in sales:
            writer.writerow({
                'ISBN': sale['isbn'], 'Title': sale['title'], 'Publisher': sale['publisher'], 
                'Copies': sale['copies'], 'Revenue': sale['revenue']
            })
    messagebox.showinfo("Export Successful", "Sales data exported to sales.csv.")

# GUI Setup
root = tk.Tk()
root.title("Book-shop Automation Software")
root.geometry("800x600")  # Resize window

# Font Style
font_style = ('Arial', 12)

# Search Section
search_var = tk.StringVar()
tk.Label(root, text="Search Book (Title/Author):", font=font_style).grid(row=0, column=0, sticky=tk.W)
tk.Entry(root, textvariable=search_var, font=font_style).grid(row=0, column=1, sticky=tk.W)
tk.Button(root, text="Search", command=search_book, font=font_style).grid(row=0, column=2, sticky=tk.W)
results_list = tk.Listbox(root, height=5, width=60, font=font_style)
results_list.grid(row=1, column=0, columnspan=3, sticky=tk.W)

# Purchase Section
isbn_var = tk.StringVar()
tk.Label(root, text="ISBN:", font=font_style).grid(row=2, column=0, sticky=tk.W)
tk.Entry(root, textvariable=isbn_var, font=font_style).grid(row=2, column=1, sticky=tk.W)
tk.Button(root, text="Purchase", command=purchase_book, font=font_style).grid(row=2, column=2, sticky=tk.W)

# Inventory Update Section
title_var = tk.StringVar()
author_var = tk.StringVar()
price_var = tk.StringVar()
copies_var = tk.StringVar()
rack_var = tk.StringVar()
publisher_var = tk.StringVar()
stockist_var = tk.StringVar()
tk.Label(root, text="Title:", font=font_style).grid(row=3, column=0, sticky=tk.W)
tk.Entry(root, textvariable=title_var, font=font_style).grid(row=3, column=1, sticky=tk.W)
tk.Label(root, text="Author:", font=font_style).grid(row=4, column=0, sticky=tk.W)
tk.Entry(root, textvariable=author_var, font=font_style).grid(row=4, column=1, sticky=tk.W)
tk.Label(root, text="Price:", font=font_style).grid(row=5, column=0, sticky=tk.W)
tk.Entry(root, textvariable=price_var, font=font_style).grid(row=5, column=1, sticky=tk.W)
tk.Label(root, text="Copies:", font=font_style).grid(row=6, column=0, sticky=tk.W)
tk.Entry(root, textvariable=copies_var, font=font_style).grid(row=6, column=1, sticky=tk.W)
tk.Label(root, text="Rack:", font=font_style).grid(row=7, column=0, sticky=tk.W)
tk.Entry(root, textvariable=rack_var, font=font_style).grid(row=7, column=1, sticky=tk.W)
tk.Label(root, text="Publisher:", font=font_style).grid(row=8, column=0, sticky=tk.W)
tk.Entry(root, textvariable=publisher_var, font=font_style).grid(row=8, column=1, sticky=tk.W)
tk.Label(root, text="Stockist:", font=font_style).grid(row=9, column=0, sticky=tk.W)
tk.Entry(root, textvariable=stockist_var, font=font_style).grid(row=9, column=1, sticky=tk.W)
tk.Button(root, text="Update Inventory", command=update_inventory, font=font_style).grid(row=10, column=1, sticky=tk.W)

# Requests Section
tk.Button(root, text="View Requests", command=view_requests, font=font_style).grid(row=11, column=0, sticky=tk.W)
request_list = tk.Listbox(root, height=5, width=60, font=font_style)
request_list.grid(row=12, column=0, columnspan=3, sticky=tk.W)

# Sales Statistics Section
tk.Button(root, text="Generate Sales Stats", command=generate_sales_stats, font=font_style).grid(row=13, column=0, sticky=tk.W)
stats_list = tk.Listbox(root, height=5, width=60, font=font_style)
stats_list.grid(row=14, column=0, columnspan=3, sticky=tk.W)

# Low Stock Report
tk.Button(root, text="Low Stock Report", command=low_stock_report, font=font_style).grid(row=15, column=0, sticky=tk.W)
report_list = tk.Listbox(root, height=5, width=60, font=font_style)
report_list.grid(row=16, column=0, columnspan=3, sticky=tk.W)

# Export Section
tk.Button(root, text="Export Inventory", command=export_inventory, font=font_style).grid(row=17, column=0, sticky=tk.W)
tk.Button(root, text="Export Sales", command=export_sales, font=font_style).grid(row=17, column=1, sticky=tk.W)

root.mainloop()
