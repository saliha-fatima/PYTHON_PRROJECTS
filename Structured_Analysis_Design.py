import tkinter as tk
from tkinter import messagebox, filedialog
import csv

class CASEToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern CASE Tool for Structured Analysis and Design")
        self.root.geometry("1200x800")

        # Font Size increase
        self.font = ("Helvetica", 14)

        # Data structure to hold diagram components
        self.data_flow_diagram = {"entities": [], "data_stores": [], "bubbles": [], "data_flows": []}
        self.modules = []

        # Canvas for drawing
        self.canvas = tk.Canvas(self.root, bg="white", width=900, height=700)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        # Control Panel
        self.control_panel = tk.Frame(self.root)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.create_widgets()

    def create_widgets(self):
        # Buttons for drawing entities, data stores, bubbles, etc.
        self.create_entity_widgets()
        self.create_data_store_widgets()
        self.create_bubble_widgets()
        self.create_data_flow_widgets()
        self.create_module_widgets()

        # File operations
        self.create_file_widgets()

    def create_entity_widgets(self):
        tk.Label(self.control_panel, text="Entity", font=self.font).pack()
        self.entity_name = tk.Entry(self.control_panel, width=20, font=self.font)
        self.entity_name.pack()
        self.entity_position = tk.Entry(self.control_panel, width=20, font=self.font)
        self.entity_position.pack()
        tk.Button(self.control_panel, text="Draw Entity", command=self.draw_entity, font=self.font).pack()

    def create_data_store_widgets(self):
        tk.Label(self.control_panel, text="Data Store", font=self.font).pack()
        self.data_store_name = tk.Entry(self.control_panel, width=20, font=self.font)
        self.data_store_name.pack()
        self.data_store_position = tk.Entry(self.control_panel, width=20, font=self.font)
        self.data_store_position.pack()
        tk.Button(self.control_panel, text="Draw Data Store", command=self.draw_data_store, font=self.font).pack()

    def create_bubble_widgets(self):
        tk.Label(self.control_panel, text="Bubble", font=self.font).pack()
        self.bubble_name = tk.Entry(self.control_panel, width=20, font=self.font)
        self.bubble_name.pack()
        self.bubble_position = tk.Entry(self.control_panel, width=20, font=self.font)
        self.bubble_position.pack()
        tk.Button(self.control_panel, text="Draw Bubble", command=self.draw_bubble, font=self.font).pack()

    def create_data_flow_widgets(self):
        tk.Label(self.control_panel, text="Data Flow Arrow", font=self.font).pack()
        self.arrow_name = tk.Entry(self.control_panel, width=20, font=self.font)
        self.arrow_name.pack()
        self.arrow_start = tk.Entry(self.control_panel, width=20, font=self.font)
        self.arrow_start.pack()
        self.arrow_end = tk.Entry(self.control_panel, width=20, font=self.font)
        self.arrow_end.pack()
        tk.Button(self.control_panel, text="Draw Data Flow", command=self.draw_data_flow_arrow, font=self.font).pack()

    def create_module_widgets(self):
        tk.Label(self.control_panel, text="Module", font=self.font).pack()
        self.module_name = tk.Entry(self.control_panel, width=20, font=self.font)
        self.module_name.pack()
        self.module_position = tk.Entry(self.control_panel, width=20, font=self.font)
        self.module_position.pack()
        tk.Button(self.control_panel, text="Draw Module", command=self.draw_module, font=self.font).pack()

    def create_file_widgets(self):
        tk.Button(self.control_panel, text="Save Diagram", command=self.save_diagram_csv, font=self.font).pack()
        tk.Button(self.control_panel, text="Load Diagram", command=self.load_diagram_csv, font=self.font).pack()
        tk.Button(self.control_panel, text="New Diagram", command=self.create_new_diagram, font=self.font).pack()

    def create_new_diagram(self):
        self.canvas.delete("all")
        self.data_flow_diagram = {"entities": [], "data_stores": [], "bubbles": [], "data_flows": []}
        self.modules = []
        messagebox.showinfo("New Diagram", "New diagram created.")

    def draw_entity(self):
        try:
            position = self.entity_position.get().strip()
            if position.count(",") != 1:
                raise ValueError("Please enter a valid position in the format 'x,y' (e.g., '100,200').")
            x, y = position.split(",")
            x, y = int(x), int(y)

            name = self.entity_name.get()
            entity = self.canvas.create_oval(x - 30, y - 20, x + 30, y + 20, fill="lightblue", outline="black", width=2)
            text = self.canvas.create_text(x, y, text=name)
            self.data_flow_diagram["entities"].append((entity, text, name, x, y))
        except ValueError as ve:
            messagebox.showerror("Invalid Input", f"Error: {str(ve)}")

    def draw_data_store(self):
        try:
            position = self.data_store_position.get().strip()
            if position.count(",") != 1:
                raise ValueError("Please enter a valid position in the format 'x,y' (e.g., '100,200').")
            x, y = position.split(",")
            x, y = int(x), int(y)

            name = self.data_store_name.get()
            store = self.canvas.create_rectangle(x - 40, y - 20, x + 40, y + 20, fill="lightyellow", outline="black", width=2)
            text = self.canvas.create_text(x, y, text=name)
            self.data_flow_diagram["data_stores"].append((store, text, name, x, y))
        except ValueError as ve:
            messagebox.showerror("Invalid Input", f"Error: {str(ve)}")

    def draw_bubble(self):
        try:
            position = self.bubble_position.get().strip()
            if position.count(",") != 1:
                raise ValueError("Please enter a valid position in the format 'x,y' (e.g., '100,200').")
            x, y = position.split(",")
            x, y = int(x), int(y)

            name = self.bubble_name.get()
            bubble = self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill="lightgreen", outline="black", width=2)
            text = self.canvas.create_text(x, y, text=name)
            self.data_flow_diagram["bubbles"].append((bubble, text, name, x, y))
        except ValueError as ve:
            messagebox.showerror("Invalid Input", f"Error: {str(ve)}")

    def draw_data_flow_arrow(self):
        try:
            start = self.arrow_start.get().strip()
            end = self.arrow_end.get().strip()
            if start.count(",") != 1 or end.count(",") != 1:
                raise ValueError("Please enter valid start and end positions in the format 'x,y' (e.g., '100,200').")
            start = list(map(int, start.split(",")))
            end = list(map(int, end.split(",")))

            name = self.arrow_name.get()
            arrow = self.canvas.create_line(start[0], start[1], end[0], end[1], arrow=tk.LAST, fill="black", width=2)
            label_x = (start[0] + end[0]) // 2
            label_y = (start[1] + end[1]) // 2
            label = self.canvas.create_text(label_x, label_y, text=name)
            self.data_flow_diagram["data_flows"].append((arrow, label, name, start, end))
        except ValueError as ve:
            messagebox.showerror("Invalid Input", f"Error: {str(ve)}")

    def draw_module(self):
        try:
            position = self.module_position.get().strip()
            if position.count(",") != 1:
                raise ValueError("Please enter a valid position in the format 'x,y' (e.g., '100,200').")
            x, y = position.split(",")
            x, y = int(x), int(y)

            name = self.module_name.get()
            module = self.canvas.create_rectangle(x - 40, y - 20, x + 40, y + 20, fill="lightgray", outline="black", width=2)
            text = self.canvas.create_text(x, y, text=name)
            self.modules.append((module, text, name, x, y))
        except ValueError as ve:
            messagebox.showerror("Invalid Input", f"Error: {str(ve)}")

    def save_diagram_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if filename:
            with open(filename, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "X", "Y", "Type"])
                for entity in self.data_flow_diagram["entities"]:
                    writer.writerow([entity[2], entity[3], entity[4], "Entity"])
                for store in self.data_flow_diagram["data_stores"]:
                    writer.writerow([store[2], store[3], store[4], "Data Store"])
                for bubble in self.data_flow_diagram["bubbles"]:
                    writer.writerow([bubble[2], bubble[3], bubble[4], "Bubble"])
                for flow in self.data_flow_diagram["data_flows"]:
                    writer.writerow([flow[2], flow[3][0], flow[3][1], "Data Flow"])
                for module in self.modules:
                    writer.writerow([module[2], module[3], module[4], "Module"])
            messagebox.showinfo("Save Diagram", f"Diagram saved to {filename}")

    def load_diagram_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if filename:
            with open(filename, "r") as f:
                reader = csv.reader(f)
                next(reader)  # Skip header row
                self.restore_diagram_from_csv(reader)
            messagebox.showinfo("Load Diagram", f"Diagram loaded from {filename}")

    def restore_diagram_from_csv(self, reader):
        self.create_new_diagram()
        for row in reader:
            name, x, y, type_ = row
            x, y = int(x), int(y)
            if type_ == "Entity":
                self.draw_entity_at_position(x, y, name)
            elif type_ == "Data Store":
                self.draw_data_store_at_position(x, y, name)
            elif type_ == "Bubble":
                self.draw_bubble_at_position(x, y, name)
            elif type_ == "Module":
                self.draw_module_at_position(x, y, name)
            elif type_ == "Data Flow":
                # Implement data flow restoration logic here
                pass

    def draw_entity_at_position(self, x, y, name):
        entity = self.canvas.create_oval(x - 30, y - 20, x + 30, y + 20, fill="lightblue", outline="black", width=2)
        text = self.canvas.create_text(x, y, text=name)
        self.data_flow_diagram["entities"].append((entity, text, name, x, y))

    def draw_data_store_at_position(self, x, y, name):
        store = self.canvas.create_rectangle(x - 40, y - 20, x + 40, y + 20, fill="lightyellow", outline="black", width=2)
        text = self.canvas.create_text(x, y, text=name)
        self.data_flow_diagram["data_stores"].append((store, text, name, x, y))

    def draw_bubble_at_position(self, x, y, name):
        bubble = self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill="lightgreen", outline="black", width=2)
        text = self.canvas.create_text(x, y, text=name)
        self.data_flow_diagram["bubbles"].append((bubble, text, name, x, y))

    def draw_module_at_position(self, x, y, name):
        module = self.canvas.create_rectangle(x - 40, y - 20, x + 40, y + 20, fill="lightgray", outline="black", width=2)
        text = self.canvas.create_text(x, y, text=name)
        self.modules.append((module, text, name, x, y))

# Run the application
root = tk.Tk()
app = CASEToolApp(root)
root.mainloop()
