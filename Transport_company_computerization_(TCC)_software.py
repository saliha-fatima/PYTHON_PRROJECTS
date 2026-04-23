import tkinter as tk
from tkinter import messagebox
import datetime
import csv

# Data Storage
trucks = {}
consignments = []
branches = {}

def initialize_data():
    global trucks, branches
    branches = {
        "Capital": [],
        "Branch1": [],
        "Branch2": [],
    }
    trucks = {
        "Capital": [],
        "Branch1": [],
        "Branch2": [],
    }
    load_data()

def load_data():
    # Load consignments from CSV if exists
    try:
        with open('consignments.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                consignment = {
                    "id": int(row["id"]),
                    "volume": float(row["volume"]),
                    "sender": row["sender"],
                    "receiver": row["receiver"],
                    "destination": row["destination"],
                    "date": datetime.datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S"),
                }
                consignments.append(consignment)
                branches[row["destination"]].append(consignment)
    except FileNotFoundError:
        pass

def save_data():
    # Save consignments to CSV
    with open('consignments.csv', 'w', newline='') as file:
        fieldnames = ["id", "volume", "sender", "receiver", "destination", "date"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for consignment in consignments:
            writer.writerow({
                "id": consignment["id"],
                "volume": consignment["volume"],
                "sender": consignment["sender"],
                "receiver": consignment["receiver"],
                "destination": consignment["destination"],
                "date": consignment["date"].strftime("%Y-%m-%d %H:%M:%S"),
            })

# GUI Functions

def add_consignment():
    volume = float(volume_entry.get())
    sender = sender_entry.get()
    receiver = receiver_entry.get()
    destination = destination_entry.get()
    consignment_id = len(consignments) + 1

    consignment = {
        "id": consignment_id,
        "volume": volume,
        "sender": sender,
        "receiver": receiver,
        "destination": destination,
        "date": datetime.datetime.now(),
    }
    consignments.append(consignment)
    branches[destination].append(consignment)
    save_data()  # Save after adding new consignment
    messagebox.showinfo("Success", f"Consignment {consignment_id} added successfully.")
    compute_charges(destination, volume)

def compute_charges(destination, volume):
    charge = volume * 10  # Example formula for transport charges
    messagebox.showinfo("Charge Info", f"Transport charge for {volume}m³ to {destination}: ${charge}")
    check_truck_allocation(destination)

def check_truck_allocation(destination):
    total_volume = sum([c["volume"] for c in branches[destination]])
    if total_volume >= 500:
        allocate_truck(destination)

def allocate_truck(destination):
    if trucks[destination]:
        truck_id = len(trucks[destination]) + 1
    else:
        truck_id = 1
    trucks[destination].append(f"Truck-{truck_id}")
    branches[destination].clear()
    messagebox.showinfo("Truck Allocation", f"Truck-{truck_id} allocated for {destination}.")

def view_truck_status():
    status = "".join([f"{branch}: {len(trucks[branch])} trucks\n" for branch in branches])
    messagebox.showinfo("Truck Status", status)

def view_truck_usage():
    usage = "Truck usage over time will be calculated and displayed here."  # Placeholder
    messagebox.showinfo("Truck Usage", usage)

def query_consignment_status():
    consignment_id = int(query_entry.get())
    consignment = next((c for c in consignments if c["id"] == consignment_id), None)
    if consignment:
        info = f"Consignment {consignment_id}: {consignment}"
    else:
        info = f"Consignment {consignment_id} not found."
    messagebox.showinfo("Consignment Status", info)

def view_average_wait_time():
    wait_times = [(datetime.datetime.now() - c["date"]).total_seconds() for c in consignments]
    avg_wait = sum(wait_times) / len(wait_times) if wait_times else 0
    messagebox.showinfo("Average Wait Time", f"Average Wait Time: {avg_wait} seconds")

def view_idle_time():
    idle_time = "Idle time stats for each truck will be displayed here."  # Placeholder
    messagebox.showinfo("Idle Time", idle_time)

# GUI Setup

root = tk.Tk()
root.title("Transport Company Computerization (TCC)")

initialize_data()

# Increase font size
font = ("Helvetica", 12)

# Add Consignment
frame1 = tk.Frame(root)
frame1.pack(pady=10)
tk.Label(frame1, text="Add Consignment:", font=font).grid(row=0, column=0, columnspan=2)
tk.Label(frame1, text="Volume:", font=font).grid(row=1, column=0)
volume_entry = tk.Entry(frame1, font=font)
volume_entry.grid(row=1, column=1)
tk.Label(frame1, text="Sender:", font=font).grid(row=2, column=0)
sender_entry = tk.Entry(frame1, font=font)
sender_entry.grid(row=2, column=1)
tk.Label(frame1, text="Receiver:", font=font).grid(row=3, column=0)
receiver_entry = tk.Entry(frame1, font=font)
receiver_entry.grid(row=3, column=1)
tk.Label(frame1, text="Destination:", font=font).grid(row=4, column=0)
destination_entry = tk.Entry(frame1, font=font)
destination_entry.grid(row=4, column=1)
tk.Button(frame1, text="Add", command=add_consignment, font=font).grid(row=5, column=0, columnspan=2)

# View Truck Status
frame2 = tk.Frame(root)
frame2.pack(pady=10)
tk.Label(frame2, text="Truck Management:", font=font).grid(row=0, column=0, columnspan=2)
tk.Button(frame2, text="View Truck Status", command=view_truck_status, font=font).grid(row=1, column=0)
tk.Button(frame2, text="View Truck Usage", command=view_truck_usage, font=font).grid(row=1, column=1)

# Query Consignment
frame3 = tk.Frame(root)
frame3.pack(pady=10)
tk.Label(frame3, text="Query Consignment:", font=font).grid(row=0, column=0, columnspan=2)
tk.Label(frame3, text="Consignment ID:", font=font).grid(row=1, column=0)
query_entry = tk.Entry(frame3, font=font)
query_entry.grid(row=1, column=1)
tk.Button(frame3, text="Query", command=query_consignment_status, font=font).grid(row=2, column=0, columnspan=2)

# Statistics
frame4 = tk.Frame(root)
frame4.pack(pady=10)
tk.Label(frame4, text="Statistics:", font=font).grid(row=0, column=0, columnspan=2)
tk.Button(frame4, text="Average Wait Time", command=view_average_wait_time, font=font).grid(row=1, column=0)
tk.Button(frame4, text="Idle Time", command=view_idle_time, font=font).grid(row=1, column=1)

root.mainloop()
