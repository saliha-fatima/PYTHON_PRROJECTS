import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog, ttk
import csv

# Initialize data structures
catalogue = []
usage_stats = {}

# Helper functions
def add_component(name, category, description, keywords):
    component = {
        "name": name,
        "category": category,
        "description": description,
        "keywords": keywords.split(","),
    }
    catalogue.append(component)
    usage_stats[name] = {"used": 0, "queried": 0, "not_used": 0}
    messagebox.showinfo("Success", f"Component '{name}' added to catalogue.")

def delete_component(name):
    global catalogue
    global usage_stats
    catalogue = [comp for comp in catalogue if comp["name"] != name]
    if name in usage_stats:
        del usage_stats[name]
    messagebox.showinfo("Success", f"Component '{name}' deleted from catalogue.")

def query_components(keywords):
    keywords = keywords.split(",")
    results = [comp for comp in catalogue if any(kw in comp["keywords"] for kw in keywords)]
    for result in results:
        usage_stats[result["name"]]["queried"] += 1
    if results:
        return results
    else:
        messagebox.showinfo("No Results", "No components found matching the query.")
        return []

def use_component(name):
    if name in usage_stats:
        usage_stats[name]["used"] += 1
        usage_stats[name]["not_used"] = max(0, usage_stats[name]["not_used"] - 1)
        messagebox.showinfo("Success", f"Component '{name}' marked as used.")
    else:
        messagebox.showwarning("Error", f"Component '{name}' not found.")

def purge_unused():
    global catalogue
    global usage_stats
    unused = [comp for comp in catalogue if usage_stats[comp["name"]]["used"] == 0]
    for comp in unused:
        usage_stats.pop(comp["name"], None)
    catalogue = [comp for comp in catalogue if comp not in unused]
    messagebox.showinfo("Purge Complete", f"Purged {len(unused)} unused components.")

def import_csv():
    filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if filename:
        global catalogue
        global usage_stats
        catalogue.clear()
        usage_stats.clear()
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                add_component(row['name'], row['category'], row['description'], row['keywords'])
        messagebox.showinfo("Import Complete", "Components have been imported successfully.")

def export_csv():
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if filename:
        with open(filename, "w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["name", "category", "description", "keywords"])
            writer.writeheader()
            for comp in catalogue:
                writer.writerow({
                    "name": comp["name"],
                    "category": comp["category"],
                    "description": comp["description"],
                    "keywords": ",".join(comp["keywords"]),
                })
        messagebox.showinfo("Export Complete", "Components have been exported successfully.")

# GUI functions
def add_component_gui():
    def submit():
        add_component(name_entry.get(), category_entry.get(), desc_entry.get(), keywords_entry.get())
        add_window.destroy()

    add_window = tk.Toplevel()
    add_window.title("Add Component")

    font = ('Arial', 12)

    tk.Label(add_window, text="Name:", font=font).grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(add_window, font=font)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Category:", font=font).grid(row=1, column=0, padx=10, pady=5)
    category_entry = tk.Entry(add_window, font=font)
    category_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Description:", font=font).grid(row=2, column=0, padx=10, pady=5)
    desc_entry = tk.Entry(add_window, font=font)
    desc_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Keywords (comma-separated):", font=font).grid(row=3, column=0, padx=10, pady=5)
    keywords_entry = tk.Entry(add_window, font=font)
    keywords_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Button(add_window, text="Submit", command=submit, font=font).grid(row=4, column=0, columnspan=2, pady=10)

def delete_component_gui():
    def submit():
        delete_component(name_entry.get())
        delete_window.destroy()

    delete_window = tk.Toplevel()
    delete_window.title("Delete Component")

    font = ('Arial', 12)

    tk.Label(delete_window, text="Name:", font=font).grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(delete_window, font=font)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Button(delete_window, text="Submit", command=submit, font=font).grid(row=1, column=0, columnspan=2, pady=10)

def query_components_gui():
    def submit():
        results = query_components(keywords_entry.get())
        query_window.destroy()
        if results:
            result_window = tk.Toplevel()
            result_window.title("Query Results")
            for idx, result in enumerate(results):
                tk.Label(result_window, text=f"{idx + 1}. {result['name']} - {result['description']}", font=('Arial', 12)).pack(padx=10, pady=5)

    query_window = tk.Toplevel()
    query_window.title("Query Components")

    font = ('Arial', 12)

    tk.Label(query_window, text="Keywords (comma-separated):", font=font).grid(row=0, column=0, padx=10, pady=5)
    keywords_entry = tk.Entry(query_window, font=font)
    keywords_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Button(query_window, text="Submit", command=submit, font=font).grid(row=1, column=0, columnspan=2, pady=10)

def use_component_gui():
    def submit():
        use_component(name_entry.get())
        use_window.destroy()

    use_window = tk.Toplevel()
    use_window.title("Use Component")

    font = ('Arial', 12)

    tk.Label(use_window, text="Name:", font=font).grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(use_window, font=font)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Button(use_window, text="Submit", command=submit, font=font).grid(row=1, column=0, columnspan=2, pady=10)

# Main GUI window
root = tk.Tk()
root.title("Software Component Catalogue")
font = ('Arial', 12)

# Buttons for different functions
tk.Button(root, text="Add Component", command=add_component_gui, font=font).pack(fill=tk.X, pady=5)
tk.Button(root, text="Delete Component", command=delete_component_gui, font=font).pack(fill=tk.X, pady=5)
tk.Button(root, text="Query Components", command=query_components_gui, font=font).pack(fill=tk.X, pady=5)
tk.Button(root, text="Use Component", command=use_component_gui, font=font).pack(fill=tk.X, pady=5)
tk.Button(root, text="Purge Unused Components", command=purge_unused, font=font).pack(fill=tk.X, pady=5)
tk.Button(root, text="Import CSV", command=import_csv, font=font).pack(fill=tk.X, pady=5)
tk.Button(root, text="Export CSV", command=export_csv, font=font).pack(fill=tk.X, pady=5)

root.mainloop()
