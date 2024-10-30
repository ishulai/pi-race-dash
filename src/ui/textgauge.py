import tkinter as tk

font_family = "URW Gothic"

def render_textgauge_large(root, label, x, y, default="0"):
    label_size = 15
    value_size = 55
    value = tk.Label(root, text=default, font=(font_family, value_size), fg="white", bg="black")
    value.place(x=x, y=y)
    label = tk.Label(root, text=label, font=(font_family, label_size), fg="orange", bg="black")
    label.place(x=x, y=y + value_size + label_size)
    return label, value

def render_textgauge_small(root, label, unit, x, y):
    label_size = 15
    value_size = 35
    value = tk.Label(root, text="0", font=(font_family, value_size), fg="white", bg="black")
    value.place(x=x, y=y)
    unit_label = tk.Label(root, text=unit, font=(font_family, label_size), fg="orange", bg="black")
    unit_label.place(x=x + 30, y=y + value_size - label_size)
    label = tk.Label(root, text=label, font=(font_family, label_size), fg="orange", bg="black")
    label.place(x=x, y=y + value_size + label_size)
    return label, value, unit_label

def update_textgauge_value_large(root, value_label, value):
    """Update value for large text gauge without a unit label."""
    value_label.config(text=f"{value}")

def update_textgauge_value_small(root, value_label, value, unit_label):
    """Update value for small text gauge with a unit label."""
    value_label.config(text=f"{value}")

    root.update_idletasks()  
    value_width = value_label.winfo_reqwidth()
    unit_label.place(x=value_label.winfo_x() + value_width + 5, y=unit_label.winfo_y())