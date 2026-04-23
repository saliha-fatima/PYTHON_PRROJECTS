import tkinter as tk
from tkinter import messagebox, simpledialog
import csv

# Global variables to manage fleet of vehicles
vehicles = {
    "Ambassador": {"Non-AC": 10, "AC": 2},
    "Tata Sumo": {"Non-AC": 5, "AC": 5},
    "Maruti Omni": {"Non-AC": 10, "AC": 0},
    "Maruti Esteem": {"Non-AC": 0, "AC": 10},
    "Mahindra Armada": {"Non-AC": 10, "AC": 0}
}

vehicle_prices = {
    "Ambassador": {"Non-AC": {"per_hour": 150, "per_km": 10}, "AC": {"per_hour": 225, "per_km": 15}},
    "Tata Sumo": {"Non-AC": {"per_hour": 200, "per_km": 12}, "AC": {"per_hour": 300, "per_km": 18}},
    "Maruti Omni": {"Non-AC": {"per_hour": 100, "per_km": 8}, "AC": {"per_hour": 0, "per_km": 0}},
    "Maruti Esteem": {"Non-AC": {"per_hour": 0, "per_km": 0}, "AC": {"per_hour": 350, "per_km": 20}},
    "Mahindra Armada": {"Non-AC": {"per_hour": 180, "per_km": 12}, "AC": {"per_hour": 0, "per_km": 0}},
}

car_status = {
    "Ambassador": {"Non-AC": {"status": "available", "rented": 0, "mileage": 0, "repair_cost": 0},
                   "AC": {"status": "available", "rented": 0, "mileage": 0, "repair_cost": 0}},
    "Tata Sumo": {"Non-AC": {"status": "available", "rented": 0, "mileage": 0, "repair_cost": 0},
                  "AC": {"status": "available", "rented": 0, "mileage": 0, "repair_cost": 0}},
    "Maruti Omni": {"Non-AC": {"status": "available", "rented": 0, "mileage": 0, "repair_cost": 0},
                    "AC": {"status": "available", "rented": 0, "mileage": 0, "repair_cost": 0}},
    "Maruti Esteem": {"Non-AC": {"status": "available", "rented": 0, "mileage": 0, "repair_cost": 0},
                     "AC": {"status": "available", "rented": 0, "mileage": 0, "repair_cost": 0}},
    "Mahindra Armada": {"Non-AC": {"status": "available", "rented": 0, "mileage": 0, "repair_cost": 0},
                        "AC": {"status": "available", "rented": 0, "mileage": 0, "repair_cost": 0}},
}

# Function to calculate rental charge
def calculate_rental_charge(vehicle_type, ac_type, hours, km, night_halt=False):
    base_hour_charge = vehicle_prices[vehicle_type][ac_type]["per_hour"]
    base_km_charge = vehicle_prices[vehicle_type][ac_type]["per_km"]
    
    if base_hour_charge == 0 and base_km_charge == 0:
        messagebox.showerror("Error", "Vehicle not available in this category.")
        return 0

    min_charge = base_hour_charge * 4  # Minimum charge for 4 hours
    rental_by_hour = base_hour_charge * hours
    rental_by_km = base_km_charge * km

    rental = max(rental_by_hour, rental_by_km, min_charge)

    if night_halt:
        rental += 150  # Charge for night halt

    return rental

# Function to rent a vehicle
def rent_vehicle():
    vehicle_type = simpledialog.askstring("Vehicle Type", "Enter vehicle type (e.g., Ambassador, Tata Sumo, Maruti Omni, Maruti Esteem, Mahindra Armada):")
    ac_type = simpledialog.askstring("AC Type", "Enter AC type (AC or Non-AC):")
    
    if vehicle_type not in vehicles or ac_type not in vehicles[vehicle_type]:
        messagebox.showerror("Error", "Invalid vehicle or AC type")
        return
    
    available_vehicles = vehicles[vehicle_type][ac_type]
    
    if available_vehicles <= 0:
        messagebox.showerror("Error", f"No {ac_type} {vehicle_type} available.")
        return
    
    hours = int(simpledialog.askstring("Rental Hours", "Enter number of rental hours (min 4 hours):"))
    km = int(simpledialog.askstring("Kilometers", "Enter number of kilometers driven:"))
    night_halt = simpledialog.askstring("Night Halt", "Is there a night halt (yes/no)?").lower() == "yes"
    
    if hours < 4:
        messagebox.showerror("Error", "Minimum rental time is 4 hours.")
        return
    
    rental_cost = calculate_rental_charge(vehicle_type, ac_type, hours, km, night_halt)
    
    advance = int(simpledialog.askstring("Advance Payment", "Enter advance payment amount:"))
    
    if advance < rental_cost:
        messagebox.showinfo("Rental Info", f"Remaining amount to pay: Rs. {rental_cost - advance}")
    elif advance > rental_cost:
        messagebox.showinfo("Rental Info", f"Refund: Rs. {advance - rental_cost}")
    
    vehicles[vehicle_type][ac_type] -= 1
    car_status[vehicle_type][ac_type]["status"] = "rented"
    car_status[vehicle_type][ac_type]["rented"] += 1
    car_status[vehicle_type][ac_type]["mileage"] += km

# Function to return a vehicle
def return_vehicle():
    vehicle_type = simpledialog.askstring("Vehicle Type", "Enter vehicle type (e.g., Ambassador, Tata Sumo, Maruti Omni, Maruti Esteem, Mahindra Armada):")
    ac_type = simpledialog.askstring("AC Type", "Enter AC type (AC or Non-AC):")
    
    if vehicle_type not in vehicles or ac_type not in vehicles[vehicle_type]:
        messagebox.showerror("Error", "Invalid vehicle or AC type")
        return
    
    hours = int(simpledialog.askstring("Rental Hours", "Enter number of rental hours (min 4 hours):"))
    km = int(simpledialog.askstring("Kilometers", "Enter number of kilometers driven:"))
    
    rental_cost = calculate_rental_charge(vehicle_type, ac_type, hours, km)
    
    # Refund or additional charge
    advance = int(simpledialog.askstring("Advance Payment", "Enter advance payment amount:"))
    
    if advance < rental_cost:
        messagebox.showinfo("Rental Info", f"Additional amount to pay: Rs. {rental_cost - advance}")
    elif advance > rental_cost:
        messagebox.showinfo("Rental Info", f"Refund: Rs. {advance - rental_cost}")
    
    vehicles[vehicle_type][ac_type] += 1
    car_status[vehicle_type][ac_type]["status"] = "available"

# Function to display vehicle statistics
def display_statistics():
    stats = ""
    for vehicle_type in vehicles:
        for ac_type in ["Non-AC", "AC"]:
            total_rent = car_status[vehicle_type][ac_type]["rented"] * vehicle_prices[vehicle_type][ac_type]["per_hour"]
            stats += f"{vehicle_type} ({ac_type}):\n"
            stats += f"Total Rentals: {car_status[vehicle_type][ac_type]['rented']}\n"
            stats += f"Total Revenue: Rs. {total_rent}\n\n"
    
    messagebox.showinfo("Vehicle Statistics", stats)

# Function to save data to CSV
def save_to_csv():
    with open("vehicle_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Vehicle Type", "AC Type", "Available Vehicles", "Rented Vehicles"])
        for vehicle_type in vehicles:
            for ac_type in ["Non-AC", "AC"]:
                writer.writerow([vehicle_type, ac_type, vehicles[vehicle_type][ac_type], car_status[vehicle_type][ac_type]["rented"]])
    messagebox.showinfo("Info", "Data saved to vehicle_data.csv")

# Function to load data from CSV
def load_from_csv():
    try:
        with open("vehicle_data.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                vehicle_type, ac_type, available_vehicles, rented_vehicles = row
                vehicles[vehicle_type][ac_type] = int(available_vehicles)
                car_status[vehicle_type][ac_type]["rented"] = int(rented_vehicles)
        messagebox.showinfo("Info", "Data loaded from vehicle_data.csv")
    except FileNotFoundError:
        messagebox.showerror("Error", "No saved data file found.")

# GUI setup
def setup_gui():
    root = tk.Tk()
    root.title("Travel Agency Vehicle Management")

    # Increase font size
    font = ("Arial", 14)

    tk.Button(root, text="Rent a Vehicle", command=rent_vehicle, font=font).pack(pady=10)
    tk.Button(root, text="Return a Vehicle", command=return_vehicle, font=font).pack(pady=10)
    tk.Button(root, text="Display Vehicle Statistics", command=display_statistics, font=font).pack(pady=10)
    tk.Button(root, text="Save to CSV", command=save_to_csv, font=font).pack(pady=10)
    tk.Button(root, text="Load from CSV", command=load_from_csv, font=font).pack(pady=10)

    root.mainloop()

setup_gui()
