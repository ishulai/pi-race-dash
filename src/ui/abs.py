import os
import tkinter as tk
from .helpers import load_svg_to_image

simulation_mode = os.environ.get("SIMULATION_MODE") != None

def render_abs_symbol(root, x, y):
    canvas = tk.Canvas(root, width=80, height=60, bg="black", highlightthickness=0)
    canvas.place(x=x, y=y)
    if simulation_mode:
        image_path = "src/ui/assets/abs.svg"
    else:
        image_path = "pi-race-dash/src/ui/assets/abs.svg"
    abs_image = load_svg_to_image(image_path, size=(80, 60))
    abs_image_item = canvas.create_image(0, 0, image=abs_image, anchor="nw")

    return canvas, abs_image_item, abs_image

def update_abs_symbol(canvas, abs_image_item, abs_on):
    if abs_on:
        canvas.itemconfig(abs_image_item, state="normal")
    else:
        canvas.itemconfig(abs_image_item, state="hidden")
