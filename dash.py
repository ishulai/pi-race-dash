import tkinter as tk
import math
import time
import threading

READ_VALUES = True

if READ_VALUES:
  import gpiod
  # GPIO setup for RPM and Speed measurement
  chip = gpiod.Chip('gpiochip0')  # Adjust if needed
  rpm_line = chip.get_line(17)  # GPIO pin 17 for RPM
  speed_line = chip.get_line(18)  # GPIO pin 18 for Speed

  rpm_line.request(consumer="RPM_Reader", type=gpiod.LINE_REQ_EV_RISING_EDGE)
  speed_line.request(consumer="Speed_Reader", type=gpiod.LINE_REQ_EV_RISING_EDGE)

# Variables for RPM and Speed calculation
calculation_interval = 1.0  # 1 second interval for RPM and Speed calculation
pulses_per_revolution = 2   # Adjust based on the engine setup
pulses_per_km = 637        # Adjust based on the speed sensor setup

rpm_count = 0
speed_count = 0

# Function to calculate RPM from pulses
def calculate_rpm(pulse_count, interval, pulses_per_revolution):
    return (pulse_count / interval) * (60 / pulses_per_revolution)

# Function to calculate Speed from pulses
def calculate_speed(pulse_count, interval, pulses_per_km):
    return (pulse_count / interval) * (3600 / pulses_per_km)  # Speed in km/h

# Function to read RPM and Speed pulses from GPIO
def read_gpio():
    global rpm_count, speed_count
    while True:
        rpm_count = 0
        speed_count = 0
        start_time = time.time()

        while time.time() - start_time < calculation_interval:
            # Poll for RPM event
            rpm_event = rpm_line.event_wait()
            if rpm_event:
                rpm_event = rpm_line.event_read()
                if rpm_event.type == gpiod.LineEvent.RISING_EDGE:
                    rpm_count += 1

            # Poll for Speed event
            speed_event = speed_line.event_wait()
            if speed_event:
                speed_event = speed_line.event_read()
                if speed_event.type == gpiod.LineEvent.RISING_EDGE:
                    speed_count += 1

        # Calculate RPM and speed based on the pulse counts
        rpm = calculate_rpm(rpm_count, calculation_interval, pulses_per_revolution)
        speed = calculate_speed(speed_count, calculation_interval, pulses_per_km)

        # Update the gauge with new values
        update_gauge(int(rpm), int(speed))

# Function to update the dashboard UI
def update_gauge(rpm_value, speed_value):
    # Update RPM label
    rpm_label.config(text=f"{rpm_value}")
    # Update Speed label
    speed_label.config(text=f"{speed_value} km/h")
    
    # Update the RPM bar (visual effect)
    rpm_bar.coords(rpm_bar_fill, 20, 50, 20 + int(rpm_value / max_rpm * 360), 90)

# Create the main window for the gauge
root = tk.Tk()
root.title("Racecar Dashboard")
root.geometry("600x400")
root.config(bg="black")

# Max values for the gauges
max_rpm = 9000
max_speed = 300

# Create RPM bar (visual effect)
rpm_bar = tk.Canvas(root, width=400, height=50, bg="black", highlightthickness=0)
rpm_bar.place(x=100, y=50)
rpm_bar.create_rectangle(20, 50, 380, 90, outline="white", width=2)
rpm_bar_fill = rpm_bar.create_rectangle(20, 50, 20, 90, fill="green", outline="green")

# Create RPM label
rpm_label = tk.Label(root, text="0", font=("Arial", 30), fg="white", bg="black")
rpm_label.place(x=450, y=50)

# Create Speed label
speed_label = tk.Label(root, text="0 km/h", font=("Arial", 30), fg="white", bg="black")
speed_label.place(x=200, y=150)

# Static values for water temp, oil pressure, and turbo
water_temp_label = tk.Label(root, text="140°F", font=("Arial", 14), fg="white", bg="black")
water_temp_label.place(x=50, y=250)

oil_pressure_label = tk.Label(root, text="12.7 BAR", font=("Arial", 14), fg="white", bg="black")
oil_pressure_label.place(x=250, y=250)

turbo_pressure_label = tk.Label(root, text="5.22 BAR", font=("Arial", 14), fg="white", bg="black")
turbo_pressure_label.place(x=450, y=250)

# Warning lights (static icons)
warning_label = tk.Label(root, text="⚠", font=("Arial", 24), fg="red", bg="black")
warning_label.place(x=50, y=300)

battery_label = tk.Label(root, text="🔋", font=("Arial", 24), fg="yellow", bg="black")
battery_label.place(x=150, y=300)

check_engine_label = tk.Label(root, text="🔧", font=("Arial", 24), fg="orange", bg="black")
check_engine_label.place(x=250, y=300)

if READ_VALUES:
  # Start a thread to read RPM and speed and update the dashboard
  gpio_thread = threading.Thread(target=read_gpio)
  gpio_thread.daemon = True  # Ensure the thread will exit when the main program exits
  gpio_thread.start()

# Start the GUI event loop
root.mainloop()
