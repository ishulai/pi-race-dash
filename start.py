import threading
from collections import deque
import os
import time

import gpiod
# GPIO setup for RPM and Speed measurement
chip = gpiod.Chip('gpiochip0')  # Adjust if needed
rpm_line = chip.get_line(17)  # GPIO pin 17 for RPM
speed_line = chip.get_line(18)  # GPIO pin 18 for Speed

rpm_line.request(consumer="RPM_Reader", type=gpiod.LINE_REQ_EV_RISING_EDGE)
speed_line.request(consumer="Speed_Reader", type=gpiod.LINE_REQ_EV_RISING_EDGE)

# Variables for RPM and Speed calculation
display_interval = 0.1  # 0.1 second interval for 10Hz updates (100ms)
pulses_per_revolution = 2   # Adjust based on the engine setup
pulses_per_mi = 1025        # Adjust based on the speed sensor setup

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

# Function to calculate RPM from pulses
def calculate_rpm(pulse_buffer, pulses_per_revolution):
    pulse_sum = sum(pulse_buffer)
    return (pulse_sum / calculation_interval) * (60 / pulses_per_revolution)

# Function to calculate Speed from pulses
def calculate_speed(pulse_buffer, pulses_per_mi):
    pulse_sum = sum(pulse_buffer)
    return (pulse_sum / calculation_interval) * (3600 / pulses_per_mi)  # Speed in km/h

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
    while True:
        speed_event = speed_line.event_wait()
        if speed_event:
            speed_event = speed_line.event_read()
            if speed_event.type == gpiod.LineEvent.RISING_EDGE:
                speed_count += 1

# Function to update the dashboard UI
def update_gauge(rpm_value, speed_value):
    print ("RPM: " + str(rpm_value) + ", Speed: " + str(speed_value), end="\r")

# Function to periodically update the UI at 10Hz
def update_ui():
    global rpm_count, speed_count
    while True:
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
        time.sleep(display_interval)

# Start a thread to read RPM and speed and update the dashboard
rpm_thread = threading.Thread(target=read_rpm)
rpm_thread.daemon = True  # Ensure the thread will exit when the main program exits
rpm_thread.start()
speed_thread = threading.Thread(target=read_speed)
speed_thread.daemon = True  # Ensure the thread will exit when the main program exits
speed_thread.start()
update_ui()