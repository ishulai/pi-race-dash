import tkinter as tk
import math

# Function to draw a gauge (circular dial)
def draw_gauge(canvas, center_x, center_y, radius, start_angle, end_angle, current_value, max_value, label):
    # Draw the circular arc representing the gauge
    canvas.create_arc(
        center_x - radius, center_y - radius,
        center_x + radius, center_y + radius,
        start=start_angle, extent=end_angle - start_angle,
        style=tk.ARC, outline="black", width=2
    )
    
    # Draw the gauge's needle based on current value
    angle = start_angle + (current_value / max_value) * (end_angle - start_angle)
    angle_rad = math.radians(angle)
    needle_x = center_x + radius * 0.8 * math.cos(angle_rad)
    needle_y = center_y - radius * 0.8 * math.sin(angle_rad)
    canvas.create_line(center_x, center_y, needle_x, needle_y, fill="red", width=2)

    # Draw gauge label
    canvas.create_text(center_x, center_y + radius + 20, text=label, font=("Arial", 12))

    # Draw current value
    canvas.create_text(center_x, center_y, text=str(current_value), font=("Arial", 14), fill="blue")

# Create the main window
root = tk.Tk()
root.title("Simple Racer Gauge Cluster")
root.geometry("500x300")

# Create a canvas to draw gauges
canvas = tk.Canvas(root, width=500, height=300)
canvas.pack()

# Draw speedometer gauge
draw_gauge(canvas, center_x=100, center_y=150, radius=80, start_angle=30, end_angle=330, current_value=80, max_value=180, label="Speed (km/h)")

# Draw RPM gauge
draw_gauge(canvas, center_x=250, center_y=150, radius=80, start_angle=30, end_angle=330, current_value=4000, max_value=8000, label="RPM")

# Draw fuel gauge
draw_gauge(canvas, center_x=400, center_y=150, radius=80, start_angle=30, end_angle=330, current_value=50, max_value=100, label="Fuel (%)")

# Start the GUI event loop
root.mainloop()
