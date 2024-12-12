import threading
import os
import time
from collections import deque

simulation_mode = os.environ.get("SIMULATION_MODE") != None

pulses_per_revolution = 3
window_size = 10  # Number of recent pulses to calculate RPM
timestamp_buffer = deque(maxlen=window_size)  # Store timestamps of the most recent pulses

sim_rpm = 0

def read_rpm(line):
    import gpiod

    global timestamp_buffer
    line.request(consumer="RPM_Reader", type=gpiod.LINE_REQ_EV_RISING_EDGE)

    while True:
        rpm_event = line.event_wait()
        if rpm_event:
            rpm_event = line.event_read()
            if rpm_event.type == gpiod.LineEvent.RISING_EDGE:
                # Record the current time for each pulse
                timestamp_buffer.append(time.time())

def listen_rpm(line):
    thread = threading.Thread(target=read_rpm, args=(line,))
    thread.daemon = True
    thread.start()

def get_rpm():
    if simulation_mode:
        return sim_rpm
    else:
        current_time = time.time()
        
        # Remove old timestamps from the buffer (more than one second old)
        while timestamp_buffer and current_time - timestamp_buffer[0] > 1:
            timestamp_buffer.popleft()

        # Calculate RPM if there are enough pulses in the buffer
        if len(timestamp_buffer) >= 2:
            time_diff = timestamp_buffer[-1] - timestamp_buffer[0]  # Time span of all pulses
            pulse_count = len(timestamp_buffer) - 1  # Number of intervals
            avg_interval = time_diff / pulse_count if pulse_count > 0 else 0
            rpm = int((60 / (avg_interval * pulses_per_revolution)) if avg_interval > 0 else 0)
        else:
            rpm = 0  # Not enough data to calculate RPM

        return rpm

def set_sim_rpm(rpm):
    global sim_rpm
    sim_rpm = int(rpm)
