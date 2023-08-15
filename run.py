import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json
from masman_label import clear_list, get_readable_data, get_zpl_data, get_product_price_avail, zpl_print
from tkinter.scrolledtext import ScrolledText
import sv_ttk
from win32 import win32print

# Your get_product_price_avail and generate_zpl functions here

key = "97479037"
parts = []
field_list = []
wh = ""
cust = ""
prices = "X"

def display_parts():
    for widget in list_frame.winfo_children():
        widget.destroy()

    font_options = ("Arial", 12)
    colours = ["lightblue", "lightpink", "lightyellow"]
    
    for num, item in enumerate(get_readable_data()):
        parts = item.split('\n', 1)
        part_number = parts[0]
        description = parts[1] if len (parts) > 1 else ""

        MAX_PART_NUMBER_WIDTH = 125
        entry_frame = tk.Frame(list_frame, bg=colours[num % len(colours)])
        entry_frame.grid(row=num, column=0, sticky="ew", columnspan=2)

        # Label for part number
        part_number_label = tk.Label(entry_frame, text=part_number, anchor="w", justify="left", 
                             bg=colours[num % len(colours)], font=font_options, 
                             fg="black", width=15, wraplength=MAX_PART_NUMBER_WIDTH)
        part_number_label.grid(row=0, column=0, sticky="ew")

        content_wrap_length = canvas.winfo_width() - part_number_label.winfo_reqwidth()
        # Label for the remaining content
        content_label = tk.Label(entry_frame, text=description, anchor="w", justify="left",
                         bg=colours[num % len(colours)], font=font_options, 
                         fg="black", wraplength=content_wrap_length, padx=20)
        content_label.grid(row=0, column=1, sticky="ew")
        entry_frame.update()
    list_frame.grid_rowconfigure(get_readable_data().__len__(), weight=1)
    list_frame.update_idletasks()  # Needed to get the actual frame size

def fetch_data_and_display():
    try:
        get_product_price_avail(key, parts, field_list, wh, cust, prices)
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data for part {parts[0]}: {str(e)}")
    display_parts()
    parts.clear()

def on_enter(event):
    part = part_entry.get()
    if part:
        parts.append(part)
        fetch_data_and_display()
        part_entry.delete(0, tk.END)
    
def on_canvas_scroll(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_window_resize(event):
    # Adjust the canvas size when the window is resized
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.itemconfig(canvas_frame, width=event.width)
    list_frame.update_idletasks()

def clear_and_refresh():
    clear_list()
    display_parts()

if __name__ == "__main__":
    app = tk.Tk()
    app.title("GLEN")
    app.geometry("600x800")

    sv_ttk.set_theme("dark")

    app.bind("<Configure>", on_window_resize)
    
    button_frame = ttk.Frame(app, style="TFrame")
    button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

    refresh_button = ttk.Button(button_frame, text="Refresh", command=display_parts)
    refresh_button.pack(side=tk.LEFT, padx=5, pady=5)

    print_button = ttk.Button(button_frame, text="Print Labels", command=zpl_print)
    print_button.pack(side=tk.LEFT, padx=5, pady=5)

    clear_button = ttk.Button(button_frame, text="Clear List", command=clear_and_refresh)
    clear_button.pack(side=tk.RIGHT, padx=5, pady=5)

    label = ttk.Label(app, text="Enter Part Number:")
    label.pack()

    part_entry = tk.Entry(app, font=("Arial", 12), borderwidth=3, relief="solid", text="Enter Peach Code")
    part_entry.pack(padx=10, pady=5)
    part_entry.bind("<Return>", on_enter)

    canvas = tk.Canvas(app)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    list_frame = tk.Frame(canvas)
    canvas_frame = canvas.create_window((0, 0), window=list_frame, anchor='nw')

    # Scroll bar
    app.bind("<Configure>", lambda event: app.configure(scrollregion=app.bbox("all")))
    scrollbar = ttk.Scrollbar(app, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    app.bind("<MouseWheel>", on_canvas_scroll)

    app.mainloop()