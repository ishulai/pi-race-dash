import tkinter as tk

font_family = "URW Gothic"

def render_mileage(root, x, y, default="0"):
    label_size = 15
    value_size = 20
    value = tk.Label(root, text=default, font=(font_family, value_size), fg="white", bg="black")
    value.place(x=x, y=y)
    label = tk.Label(root, text="MI", font=(font_family, label_size), fg="orange", bg="black")
    label.place(x=x, y=y+5)
    return label, value

def update_mileage(root, value_label, value, miles_label):
    value_label.config(text=f"{value:,}")
    root.update_idletasks()  
    value_width = value_label.winfo_reqwidth()
    miles_label.place(x=value_label.winfo_x() + value_width, y=miles_label.winfo_y())