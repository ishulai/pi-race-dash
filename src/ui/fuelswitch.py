import os
import tkinter as tk
from .helpers import load_svg_to_image

simulation_mode = os.environ.get("SIMULATION_MODE") != None

def render_low_fuel_symbol(root, x, y):
    canvas = tk.Canvas(root, width=60, height=80, bg="black", highlightthickness=0)
    canvas.place(x=x, y=y)
    image_path = "src/ui/assets/fuel.svg"
    # if simulation_mode:
    #     image_path = "src/ui/assets/fuel.svg"
    # else:
    #     image_path = "pi-race-dash/src/ui/assets/fuel.svg"
    fuel_image = load_svg_to_image(image_path, (40, 40))
    fuel_image_item = canvas.create_image(40, 40, image=fuel_image)

    return canvas, fuel_image_item, fuel_image

def update_low_fuel_symbol(canvas, fuel_image_item, low_fuel_on):
    if low_fuel_on:
        canvas.itemconfig(fuel_image_item, state="normal")
    else:
        canvas.itemconfig(fuel_image_item, state="hidden")
