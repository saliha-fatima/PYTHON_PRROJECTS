import tkinter as tk
from tkinter import ttk
import random
import time
import csv

def simulate(factory_params, output_label):
    num_machines = factory_params['num_machines']
    num_adjusters = factory_params['num_adjusters']
    mttf = factory_params['mttf']
    simulation_time = factory_params['simulation_time']

    machines = [0] * num_machines  # Tracks machine state (0 = working, 1 = failed)
    adjusters = [0] * num_adjusters  # Tracks adjuster state (0 = idle, 1 = busy)

    total_machine_uptime = 0
    total_adjuster_busy_time = 0
    machine_failures = 0

    machine_queue = []  # Queue for failed machines or idle adjusters

    for t in range(simulation_time):
        # Check for machine failures
        for i in range(num_machines):
            if machines[i] == 0:  # Machine is working
                if random.random() < 1 / mttf:  # Probability of failure
                    machines[i] = 1
                    machine_queue.append(i)  # Add to failure queue

        # Assign adjusters to failed machines
        while machine_queue and 0 in adjusters:
            failed_machine = machine_queue.pop(0)
            free_adjuster = adjusters.index(0)
            adjusters[free_adjuster] = mttf // 10  # Adjuster busy for some time
            machines[failed_machine] = 2  # Machine under repair

        # Update machine and adjuster states
        for i in range(num_machines):
            if machines[i] == 2:  # Under repair
                machines[i] = 0  # Machine back to working

        for i in range(num_adjusters):
            if adjusters[i] > 0:  # Busy adjuster
                adjusters[i] -= 1
                if adjusters[i] == 0 and machines.count(2) > 0:
                    machine_failures += 1

        # Update utilization
        total_machine_uptime += machines.count(0)
        total_adjuster_busy_time += num_adjusters - adjusters.count(0)

    # Calculate utilization
    machine_utilization = (total_machine_uptime / (simulation_time * num_machines)) * 100
    adjuster_utilization = (total_adjuster_busy_time / (simulation_time * num_adjusters)) * 100

    # Display results
    result = f"Machine Utilization: {machine_utilization:.2f}%\n"
    result += f"Adjuster Utilization: {adjuster_utilization:.2f}%\n"
    result += f"Total Machine Failures: {machine_failures}"
    output_label.config(text=result)
    
    # Return the results for CSV export
    return {
        "Machine Utilization": machine_utilization,
        "Adjuster Utilization": adjuster_utilization,
        "Total Machine Failures": machine_failures
    }

def start_simulation():
    try:
        factory_params = {
            'num_machines': int(entry_num_machines.get()),
            'num_adjusters': int(entry_num_adjusters.get()),
            'mttf': int(entry_mttf.get()),
            'simulation_time': int(entry_simulation_time.get())
        }
        results = simulate(factory_params, output_label)
        export_button.config(state=tk.NORMAL)  # Enable the export button after simulation

        # Store the results for CSV export
        global simulation_results
        simulation_results = results
    except ValueError:
        output_label.config(text="Please enter valid numerical inputs.")

def export_to_csv():
    try:
        with open("simulation_results.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Metric", "Value"])
            for key, value in simulation_results.items():
                writer.writerow([key, value])
        output_label.config(text="Results exported to simulation_results.csv")
    except Exception as e:
        output_label.config(text=f"Error exporting to CSV: {e}")

# GUI Setup
root = tk.Tk()
root.title("Factory Simulation Software")

# Define a large font size for better readability
font_style = ('Arial', 14)

# Input fields
tk.Label(root, text="Number of Machines:", font=font_style).grid(row=0, column=0, padx=10, pady=5, sticky='w')
entry_num_machines = ttk.Entry(root, font=font_style)
entry_num_machines.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Number of Adjusters:", font=font_style).grid(row=1, column=0, padx=10, pady=5, sticky='w')
entry_num_adjusters = ttk.Entry(root, font=font_style)
entry_num_adjusters.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Mean Time to Failure (MTTF):", font=font_style).grid(row=2, column=0, padx=10, pady=5, sticky='w')
entry_mttf = ttk.Entry(root, font=font_style)
entry_mttf.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Simulation Time (seconds):", font=font_style).grid(row=3, column=0, padx=10, pady=5, sticky='w')
entry_simulation_time = ttk.Entry(root, font=font_style)
entry_simulation_time.grid(row=3, column=1, padx=10, pady=5)

# Start button
start_button = ttk.Button(root, text="Start Simulation", command=start_simulation, style="TButton")
start_button.grid(row=4, column=0, columnspan=2, pady=10)

# Output label
output_label = tk.Label(root, text="", font=font_style, justify=tk.LEFT)
output_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

# Export button (disabled initially)
export_button = ttk.Button(root, text="Export to CSV", command=export_to_csv, state=tk.DISABLED)
export_button.grid(row=6, column=0, columnspan=2, pady=10)

# Run the main loop
root.mainloop()
