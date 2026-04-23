import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import pickle
import csv

def init_variables():
    global shapes, current_tool, clipboard, canvas, filename, zoom_factor, pan_offset
    shapes = []  # Stores all graphical objects
    current_tool = None  # Stores the current tool (e.g., 'circle', 'rectangle')
    clipboard = [[] for _ in range(10)]  # 10 clipboards for copying objects
    filename = None  # Stores the filename for saving/loading
    zoom_factor = 1.0  # Default zoom level
    pan_offset = [0, 0]  # Pan offset

def create_shape(shape_type, **kwargs):
    global shapes
    shapes.append({'type': shape_type, 'properties': kwargs, 'group': None})
    draw_all()

def draw_all():
    canvas.delete("all")
    for shape in shapes:
        props = shape['properties']
        if shape['type'] == 'circle':
            canvas.create_oval(props['x'] - props['r'], props['y'] - props['r'],
                               props['x'] + props['r'], props['y'] + props['r'],
                               outline=props.get('outline', 'black'), fill=props.get('fill', ''))
        elif shape['type'] == 'rectangle':
            canvas.create_rectangle(props['x1'], props['y1'], props['x2'], props['y2'],
                                    outline=props.get('outline', 'black'), fill=props.get('fill', ''))
        elif shape['type'] == 'line':
            canvas.create_line(props['x1'], props['y1'], props['x2'], props['y2'],
                               fill=props.get('color', 'black'), width=props.get('width', 1))
        elif shape['type'] == 'polygon':
            canvas.create_polygon(props['points'], outline=props.get('outline', 'black'), fill=props.get('fill', ''))
        elif shape['type'] == 'text':
            canvas.create_text(props['x'], props['y'], text=props['text'], fill=props.get('color', 'black'))

def save_graphics():
    global filename
    if not filename:
        filename = filedialog.asksaveasfilename(defaultextension=".gph", filetypes=[("Graphics Files", "*.gph")])
    if filename:
        with open(filename, 'wb') as f:
            pickle.dump(shapes, f)

def load_graphics():
    global shapes, filename
    filename = filedialog.askopenfilename(filetypes=[("Graphics Files", "*.gph")])
    if filename:
        with open(filename, 'rb') as f:
            shapes = pickle.load(f)
        draw_all()

def import_bitmap():
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.bmp;*.png;*.jpg")])
    if filepath:
        img = tk.PhotoImage(file=filepath)
        canvas.create_image(0, 0, anchor=tk.NW, image=img)
        canvas.image = img  # Prevent garbage collection

def import_csv():
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if filepath:
        try:
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    shape_type = row['type']
                    if shape_type == 'circle':
                        create_shape('circle', x=float(row['x']), y=float(row['y']), r=float(row['r']), fill=row.get('fill', ''))
                    elif shape_type == 'rectangle':
                        create_shape('rectangle', x1=float(row['x1']), y1=float(row['y1']), x2=float(row['x2']), y2=float(row['y2']), fill=row.get('fill', ''))
                    elif shape_type == 'line':
                        create_shape('line', x1=float(row['x1']), y1=float(row['y1']), x2=float(row['x2']), y2=float(row['y2']), color=row.get('color', 'black'))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import CSV: {e}")

def zoom(factor):
    global zoom_factor
    zoom_factor *= factor
    canvas.scale("all", 0, 0, factor, factor)

def pan(dx, dy):
    global pan_offset
    pan_offset[0] += dx
    pan_offset[1] += dy
    canvas.move("all", dx, dy)

def fit_to_screen():
    global zoom_factor, pan_offset
    zoom_factor = 1.0
    pan_offset = [0, 0]
    draw_all()

def main():
    global canvas

    init_variables()
    root = tk.Tk()
    root.title("Graphics Editor")

    # Create canvas
    canvas = tk.Canvas(root, width=800, height=600, bg="white")
    canvas.pack(fill=tk.BOTH, expand=True)

    # Add buttons for functionalities
    toolbar = tk.Frame(root, bg="lightgray")
    toolbar.pack(side=tk.TOP, fill=tk.X, pady=5)

    button_font = ("Helvetica", 10)

    tk.Button(toolbar, text="Circle", font=button_font, command=lambda: create_shape('circle', x=100, y=100, r=50, fill='red')).pack(side=tk.LEFT, padx=5)
    tk.Button(toolbar, text="Rectangle", font=button_font, command=lambda: create_shape('rectangle', x1=150, y1=150, x2=300, y2=300, fill='blue')).pack(side=tk.LEFT, padx=5)
    tk.Button(toolbar, text="Save", font=button_font, command=save_graphics).pack(side=tk.LEFT, padx=5)
    tk.Button(toolbar, text="Load", font=button_font, command=load_graphics).pack(side=tk.LEFT, padx=5)
    tk.Button(toolbar, text="Import Bitmap", font=button_font, command=import_bitmap).pack(side=tk.LEFT, padx=5)
    tk.Button(toolbar, text="Import CSV", font=button_font, command=import_csv).pack(side=tk.LEFT, padx=5)
    tk.Button(toolbar, text="Zoom In", font=button_font, command=lambda: zoom(1.2)).pack(side=tk.LEFT, padx=5)
    tk.Button(toolbar, text="Zoom Out", font=button_font, command=lambda: zoom(0.8)).pack(side=tk.LEFT, padx=5)
    tk.Button(toolbar, text="Pan Left", font=button_font, command=lambda: pan(-20, 0)).pack(side=tk.LEFT, padx=5)
    tk.Button(toolbar, text="Pan Right", font=button_font, command=lambda: pan(20, 0)).pack(side=tk.LEFT, padx=5)
    tk.Button(toolbar, text="Fit Screen", font=button_font, command=fit_to_screen).pack(side=tk.LEFT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()
