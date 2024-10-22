import tkinter as tk
import threading
from collections import deque
import os
import time

simulation_mode = os.environ.get("SIMULATION_MODE") != None

if not simulation_mode:
    import gpiod
    # GPIO setup for RPM and Speed measurement
    chip = gpiod.Chip('gpiochip0')  # Adjust if needed
    rpm_line = chip.get_line(17)  # GPIO pin 17 for RPM
    speed_line = chip.get_line(27)  # GPIO pin 27 for Speed

    rpm_line.request(consumer="RPM_Reader", type=gpiod.LINE_REQ_EV_RISING_EDGE)
    speed_line.request(consumer="Speed_Reader", type=gpiod.LINE_REQ_EV_RISING_EDGE)

font_family = "URW Gothic"

# Variables for RPM and Speed calculation
display_interval = 0.1  # 0.1 second interval for 10Hz updates (100ms)
pulses_per_revolution = 3
revs_per_mi = 846
pulses_per_rev = 9
pulses_per_mi = revs_per_mi * pulses_per_rev

# Rolling window parameters
calculation_interval = 1.0  # 1 second rolling window for RPM and speed calculation
num_intervals = int(calculation_interval / display_interval)  # Number of 0.1s intervals in 1 second

# Rolling window buffers (to store pulse counts for the last 1 second)
rpm_pulse_buffer = deque([0] * num_intervals, maxlen=num_intervals)
speed_pulse_buffer = deque([0] * num_intervals, maxlen=num_intervals)

rpm_count = 0
speed_count = 0

sim_rpm_value = 0
sim_speed_value = 0

min_debounce_interval = 0.002  # 2ms

def calculate_dynamic_debounce(speed):
    if speed > 0:
        pulses_per_second = (speed / 3600) * pulses_per_mi
        time_between_pulses = 1 / pulses_per_second
        return max(time_between_pulses * 0.5, min_debounce_interval)
    else:
        return 0.1

# Function to calculate RPM from pulses
def calculate_rpm(pulse_buffer, pulses_per_revolution):
    pulse_sum = sum(pulse_buffer)
    return (pulse_sum / calculation_interval) * (60 / pulses_per_revolution)

# Function to calculate Speed from pulses
def calculate_speed(pulse_buffer, pulses_per_mi):
    pulse_sum = sum(pulse_buffer)
    return (pulse_sum / calculation_interval) * (3600 / pulses_per_mi)

def read_rpm():
    global rpm_count
    while True:
        rpm_event = rpm_line.event_wait()
        if rpm_event:
            rpm_event = rpm_line.event_read()
            if rpm_event.type == gpiod.LineEvent.RISING_EDGE:
                rpm_count += 1

def read_speed():
    global speed_count
    last_speed_time = 0
    while True:
        speed_event = speed_line.event_wait()
        if speed_event:
            speed_event = speed_line.event_read()
            current_time = time.time()
            current_speed = calculate_speed(speed_pulse_buffer, pulses_per_mi)
            debounce_interval = calculate_dynamic_debounce(current_speed)
            if speed_event.type == gpiod.LineEvent.RISING_EDGE and (current_time - last_speed_time) > debounce_interval:
                speed_count += 1
                last_speed_time = current_time

# Function to update the dashboard UI
def update_gauge(rpm_value, speed_value):
    # Update RPM label without recreating the widget
    rpm_label_value.config(text=f"{rpm_value}")
    # Update Speed label without recreating the widget
    speed_label_value.config(text=f"{speed_value}")
    
    # Update the RPM bar (visual effect)
    max_bar_width = 720  # Maximum width of the bar, adjusted for 800px window width
    fill_width = int(rpm_value / max_rpm * max_bar_width)
    rpm_bar.coords(rpm_bar_fill, 0, 0, fill_width, 50)

# Function to periodically update the UI at 10Hz
def update_ui():
    if simulation_mode:
        update_gauge(int(sim_rpm_value), int(sim_speed_value))
    else:
        global rpm_count, speed_count
        # Add the current pulse counts to the rolling buffer
        rpm_pulse_buffer.append(rpm_count)
        speed_pulse_buffer.append(speed_count)
        
        # Calculate the RPM and Speed from the rolling buffer
        rpm = calculate_rpm(rpm_pulse_buffer, pulses_per_revolution)
        speed = calculate_speed(speed_pulse_buffer, pulses_per_mi)
        
        # Reset the current pulse counts for the next interval
        rpm_count = 0
        speed_count = 0
        
        # Update the UI with the latest RPM and Speed values
        update_gauge(int(rpm), int(speed))
    
    # Schedule the next update after 100ms (10Hz)
    root.after(round(1000 * display_interval), update_ui)

# Create the main window for the gauge
root = tk.Tk()
root.title("Racecar Dashboard")
root.geometry("800x480")
root.config(bg="black")

# Set the window to full-screen mode
root.attributes('-fullscreen', True)

# Optional: Add an escape key binding to exit full-screen mode
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

# Max values for the gauges
max_rpm = 9000
redline = 7000
max_speed = 200

# Create RPM bar (visual effect)
rpm_bar = tk.Canvas(root, width=720, height=60, bg="white", highlightthickness=0)
rpm_bar.place(x=40, y=50)
rpm_bar.create_rectangle(0, 50, (redline - 500) / max_rpm * 720, 60, fill="green", outline="green")
rpm_bar.create_rectangle((redline - 500) / max_rpm * 720, 50, redline / max_rpm * 720, 60, fill="orange", outline="orange")
rpm_bar.create_rectangle(redline / max_rpm * 720, 50, 720, 60, fill="red", outline="red")
rpm_bar_fill = rpm_bar.create_rectangle(0, 0, 20, 50, fill="blue", outline="blue")

def render_large_value(label, x, y):
  label_size = 15
  value_size = 55
  value = tk.Label(root, text="0", font=(font_family, value_size), fg="white", bg="black")
  value.place(x=x, y=y)
  label = tk.Label(root, text=label, font=(font_family, label_size), fg="orange", bg="black")
  label.place(x=x, y=y + value_size + label_size)
  return (label, value)

def render_small_value(label, unit, x, y):
  label_size = 15
  value_size = 35
  value = tk.Label(root, text="0", font=(font_family, value_size), fg="white", bg="black")
  value.place(x=x, y=y)
  unit = tk.Label(root, text=unit, font=(font_family, label_size), fg="orange", bg="black")
  unit.place(x=x+30, y=y + value_size - label_size)
  label = tk.Label(root, text=label, font=(font_family, label_size), fg="orange", bg="black")
  label.place(x=x, y=y + value_size + label_size)
  return (label, value)

rpm_label, rpm_label_value = render_large_value("RPM", 40, 120)
speed_label, speed_label_value = render_large_value("MPH", 340, 120)
gear_label, gear_label_value = render_large_value("GEAR", 640, 120)

water_temp_label, water_temp_label_value = render_small_value("WATER TEMP", "°F", 40, 260)
oil_temp_label, oil_temp_label_value = render_small_value("OIL TEMP", "°F", 240, 260)
oil_pressure_label, oil_pressure_label_value = render_small_value("OIL PRESSURE", "PSI", 440, 260)
fuel_label, fuel_label_value = render_small_value("FUEL", "KG", 640, 260)

# Function to handle the simulation window with sliders
def open_simulation_window():
    def adjust_rpm(val):
        global sim_rpm_value
        sim_rpm_value = int(val)
    
    def adjust_speed(val):
        global sim_speed_value
        sim_speed_value = int(val)
    
    # Create a second window for the simulation controls
    sim_window = tk.Toplevel(root)
    sim_window.title("Simulation Controls")
    sim_window.geometry("400x200")
    
    # Create an RPM slider
    rpm_slider = tk.Scale(sim_window, from_=0, to=max_rpm, orient=tk.HORIZONTAL, label="RPM", command=adjust_rpm)
    rpm_slider.pack(fill=tk.X, padx=20, pady=10)
    
    # Create a Speed slider
    speed_slider = tk.Scale(sim_window, from_=0, to=max_speed, orient=tk.HORIZONTAL, label="Speed", command=adjust_speed)
    speed_slider.pack(fill=tk.X, padx=20, pady=10)

if not simulation_mode:
  # Start a thread to read RPM and speed and update the dashboard
    rpm_thread = threading.Thread(target=read_rpm)
    rpm_thread.daemon = True  # Ensure the thread will exit when the main program exits
    rpm_thread.start()
    speed_thread = threading.Thread(target=read_speed)
    speed_thread.daemon = True  # Ensure the thread will exit when the main program exits
    speed_thread.start()
else:
    open_simulation_window()

root.after(100, update_ui)

# Start the GUI event loop
root.mainloop()
