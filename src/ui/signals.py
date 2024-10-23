import tkinter as tk

off_color = "black"
on_color = "green"

def render_left_signal(root, x, y):
    canvas = tk.Canvas(root, width=80, height=60, bg="black", highlightthickness=0)
    canvas.place(x=x, y=y)
    arrow = canvas.create_polygon([20, 30, 50, 10, 50, 20, 70, 20, 70, 40, 50, 40, 50, 50], fill=off_color, outline=off_color)
    return canvas, arrow

def render_right_signal(root, x, y):
    canvas = tk.Canvas(root, width=80, height=60, bg="black", highlightthickness=0)
    canvas.place(x=x, y=y)
    arrow = canvas.create_polygon([60, 30, 30, 10, 30, 20, 10, 20, 10, 40, 30, 40, 30, 50], fill=off_color, outline=off_color)
    return canvas, arrow

def update_signal(canvas, arrow, on):
    if on:
        canvas.itemconfig(arrow, fill=on_color, outline=on_color)
    else:
        canvas.itemconfig(arrow, fill=off_color, outline=off_color)