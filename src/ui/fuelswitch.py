import tkinter as tk
import io
from PIL import Image, ImageTk
import cairosvg
import os

def load_svg_to_image(filepath, size=(80, 80)):
    png_data = cairosvg.svg2png(url=filepath, output_width=size[0], output_height=size[1])
    image = Image.open(io.BytesIO(png_data)).resize((40,40),resample=Image.NEAREST)
    return ImageTk.PhotoImage(image)

def render_low_fuel_symbol(root, x, y):
    canvas = tk.Canvas(root, width=80, height=80, bg="black", highlightthickness=0)
    canvas.place(x=x, y=y)
    fuel_image = load_svg_to_image("src/ui/assets/fuel.svg")
    fuel_image_item = canvas.create_image(40, 40, image=fuel_image)

    return canvas, fuel_image_item, fuel_image

def update_low_fuel_symbol(canvas, fuel_image_item, low_fuel_on):
    if low_fuel_on:
        canvas.itemconfig(fuel_image_item, state="normal")
    else:
        canvas.itemconfig(fuel_image_item, state="hidden")
