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
    unit = tk.Label(root, text=unit, font=(font_family, label_size), fg="orange", bg="black")
    unit.place(x=x+30, y=y + value_size - label_size)
    label = tk.Label(root, text=label, font=(font_family, label_size), fg="orange", bg="black")
    label.place(x=x, y=y + value_size + label_size)
    return label, value

def update_textgauge_value(value_label, value):
    value_label.config(text=f"{value}")