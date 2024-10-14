import tkinter as tk
import math
import gpiod
import time
import threading

# GPIO setup for RPM measurement
chip = gpiod.Chip('gpiochip0')  # Adjust if needed
rpm_line = chip.get_line(17)  # GPIO pin 17 for RPM
rpm_line.request(consumer="RPM_Reader", type=gpiod.LINE_REQ_EV_RISING_EDGE)

# Variables for RPM calculation
calculation_interval = 0.1  # 1 second interval for RPM calculation
pulses_per_revolution = 2   # Adjust based on the engine setup
rpm_count = 0

# S2000 RPM gauge constants
max_rpm = 9000
redline_rpm = 7000

# Function to calculate RPM from pulses
def calculate_rpm(pulse_count, interval, pulses_per_revolution):
    return (pulse_count / interval) * (60 / pulses_per_revolution)

# Function to read RPM pulses from GPIO
def read_rpm():
    global rpm_count
    while True:
        rpm_count = 0
        start_time = time.time()

        while time.time() - start_time < calculation_interval:
            rpm_event = rpm_line.event_wait()
            if rpm_event:
                rpm_event = rpm_line.event_read()
                if rpm_event.type == gpiod.LineEvent.RISING_EDGE:
                    rpm_count += 1

        # Calculate the RPM and update the gauge
        rpm = calculate_rpm(rpm_count, calculation_interval, pulses_per_revolution)
        update_gauge(int(rpm))

# Function to update the RPM gauge on the canvas
def update_gauge(rpm_value):
    canvas.delete("all")
    draw_s2k_rpm_gauge(canvas, center_x=200, center_y=200, radius=150, current_rpm=rpm_value, max_rpm=max_rpm, redline_rpm=redline_rpm)

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

# Create the main window for the gauge
root = tk.Tk()
root.title("S2000 RPM Gauge")
root.geometry("400x400")

# Create a canvas to draw the gauge
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Start a thread to read RPM and update the gauge
rpm_thread = threading.Thread(target=read_rpm)
rpm_thread.daemon = True  # Ensure the thread will exit when the main program exits
rpm_thread.start()

# Start the GUI event loop
root.mainloop()
