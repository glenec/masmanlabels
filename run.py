import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json
from masman_label import clear_list, get_readable_data, get_zpl_data, get_product_price_avail, zpl_print
from tkinter.scrolledtext import ScrolledText
import sv_ttk


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
    colours = ["lightblue", "lightgreen", "lightpink", "lightyellow"]

    for num, item in enumerate(get_readable_data()):
        part_label = tk.Label(list_frame, text=f"{item}", anchor="w", justify="left", bg=colours[num % len(colours)], 
                      font=font_options, fg="black", wraplength=canvas.winfo_width(), width = canvas.winfo_width())
        part_label.grid(row=num, column=0, sticky="ew")


    list_frame.grid_rowconfigure(get_readable_data().__len__(), weight=1)
    list_frame.update_idletasks()  # Needed to get the actual frame size
    canvas.configure(scrollregion=canvas.bbox("all"))  # Update the scrollable region

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
        display_parts()
        part_entry.delete(0, tk.END)
    
def on_canvas_scroll(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

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
    app.title("MASMAN Label Printer")
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
    list_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
    scrollbar = ttk.Scrollbar(app, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    app.bind("<MouseWheel>", on_canvas_scroll)

    app.mainloop()