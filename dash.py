import tkinter as tk
import math
import time
import threading

simulation_mode = False

if not simulation_mode:
    import gpiod
    # GPIO setup for RPM and Speed measurement
    chip = gpiod.Chip('gpiochip0')  # Adjust if needed
    rpm_line = chip.get_line(17)  # GPIO pin 17 for RPM
    speed_line = chip.get_line(18)  # GPIO pin 18 for Speed

    rpm_line.request(consumer="RPM_Reader", type=gpiod.LINE_REQ_EV_RISING_EDGE)
    speed_line.request(consumer="Speed_Reader", type=gpiod.LINE_REQ_EV_RISING_EDGE)

# Variables for RPM and Speed calculation
calculation_interval = 0.1  # 0.1 second interval for 10Hz updates (100ms)
pulses_per_revolution = 2   # Adjust based on the engine setup
pulses_per_mi = 1025        # Adjust based on the speed sensor setup

rpm_count = 0
speed_count = 0

sim_rpm_value = 0
sim_speed_value = 0

# Function to calculate RPM from pulses
def calculate_rpm(pulse_count, interval, pulses_per_revolution):
    return (pulse_count / interval) * (60 / pulses_per_revolution)

# Function to calculate Speed from pulses
def calculate_speed(pulse_count, interval, pulses_per_mi):
    return (pulse_count / interval) * (3600 / pulses_per_mi)  # Speed in km/h

# Function to read RPM and Speed pulses from GPIO
def read_gpio():
    global rpm_count, speed_count
    while True:
        rpm_event = rpm_line.event_wait()
        if rpm_event:
            rpm_event = rpm_line.event_read()
            if rpm_event.type == gpiod.LineEvent.RISING_EDGE:
                rpm_count += 1

        # # Poll for Speed event
        # speed_event = speed_line.event_wait()
        # if speed_event:
        #     speed_event = speed_line.event_read()
        #     if speed_event.type == gpiod.LineEvent.RISING_EDGE:
        #         speed_count += 1

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
    # Update the UI with new data
    if simulation_mode:
        update_gauge(int(sim_rpm_value), int(sim_speed_value))
    else:
        rpm = calculate_rpm(rpm_count, calculation_interval, pulses_per_revolution)
        speed = calculate_speed(speed_count, calculation_interval, pulses_per_mi)
        rpm_count = 0
        speed_count = 0
        update_gauge(int(rpm), int(speed))
    
    # Schedule the next update after 100ms (10Hz)
    root.after(100, update_ui)

# Create the main window for the gauge
root = tk.Tk()
root.title("Racecar Dashboard")
root.geometry("800x480")
root.config(bg="black")

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
  label = tk.Label(root, text=label, font=("Futura", label_size), fg="orange", bg="black")
  label.place(x=x, y=y + value_size + label_size)
  value = tk.Label(root, text="0", font=("Futura", value_size), fg="white", bg="black")
  value.place(x=x, y=y)
  return (label, value)

def render_small_value(label, unit, x, y):
  label_size = 15
  value_size = 35
  label = tk.Label(root, text=label, font=("Futura", label_size), fg="orange", bg="black")
  label.place(x=x, y=y + value_size + label_size)
  value = tk.Label(root, text="0", font=("Futura", value_size), fg="white", bg="black")
  value.place(x=x, y=y)
  unit = tk.Label(root, text=unit, font=("Futura", label_size), fg="orange", bg="black")
  unit.place(x=x+30, y=y + value_size - label_size)
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
    gpio_thread = threading.Thread(target=read_gpio)
    gpio_thread.daemon = True  # Ensure the thread will exit when the main program exits
    gpio_thread.start()
else:
    open_simulation_window()

# Start the UI update loop at 10Hz
root.after(100, update_ui)

# Start the GUI event loop
root.mainloop()
