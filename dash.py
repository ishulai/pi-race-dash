import tkinter as tk
import math

# Function to draw the S2000-style RPM gauge
def draw_s2k_rpm_gauge(canvas, center_x, center_y, radius, current_rpm, max_rpm, redline_rpm):
    start_angle = 30  # Starting angle for the gauge arc
    end_angle = 330   # Ending angle for the gauge arc

    # Draw the circular arc representing the gauge
    canvas.create_arc(
        center_x - radius, center_y - radius,
        center_x + radius, center_y + radius,
        start=start_angle, extent=end_angle - start_angle,
        style=tk.ARC, outline="black", width=2
    )

    # Draw segments indicating the redline area
    redline_start_angle = start_angle + (redline_rpm / max_rpm) * (end_angle - start_angle)
    canvas.create_arc(
        center_x - radius, center_y - radius,
        center_x + radius, center_y + radius,
        start=redline_start_angle, extent=end_angle - redline_start_angle,
        style=tk.ARC, outline="red", width=4
    )

    # Draw the gauge's needle based on current RPM
    needle_angle = start_angle + (current_rpm / max_rpm) * (end_angle - start_angle)
    needle_angle_rad = math.radians(needle_angle)
    needle_x = center_x + radius * 0.8 * math.cos(needle_angle_rad)
    needle_y = center_y - radius * 0.8 * math.sin(needle_angle_rad)
    canvas.create_line(center_x, center_y, needle_x, needle_y, fill="red", width=3)

    # Draw the RPM text at different intervals (like 1000, 3000, 5000, etc.)
    for i in range(0, max_rpm + 1, 1000):
        angle = start_angle + (i / max_rpm) * (end_angle - start_angle)
        angle_rad = math.radians(angle)
        text_x = center_x + (radius + 20) * math.cos(angle_rad)
        text_y = center_y - (radius + 20) * math.sin(angle_rad)
        canvas.create_text(text_x, text_y, text=str(i), font=("Arial", 10))

    # Draw gauge label
    canvas.create_text(center_x, center_y + radius + 40, text="RPM", font=("Arial", 14))

    # Draw current RPM value
    canvas.create_text(center_x, center_y, text=str(current_rpm), font=("Arial", 18), fill="blue")

# Create the main window
root = tk.Tk()
root.title("S2000 RPM Gauge")
root.geometry("400x400")

# Create a canvas to draw the gauge
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Draw the S2000-style RPM gauge
current_rpm = 5000  # Example current RPM
max_rpm = 9000      # Maximum RPM for the gauge
redline_rpm = 7000  # Redline starts at 7000 RPM

draw_s2k_rpm_gauge(canvas, center_x=200, center_y=200, radius=150, current_rpm=current_rpm, max_rpm=max_rpm, redline_rpm=redline_rpm)

# Start the GUI event loop
root.mainloop()
