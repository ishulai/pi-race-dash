import threading
import os
from collections import deque

simulation_mode = os.environ.get("SIMULATION_MODE") != None

display_interval = 0.1
pulses_per_revolution = 3
calculation_interval = 1.0
num_intervals = int(calculation_interval / display_interval)

rpm_pulse_buffer = deque([0] * num_intervals, maxlen=num_intervals)
rpm_count = 0

sim_rpm = 0

def read_rpm(line):
    import gpiod

    global rpm_count

    while True:
        rpm_event = line.event_wait()
        if rpm_event:
            rpm_event = line.event_read()
            if rpm_event.type == gpiod.LineEvent.RISING_EDGE:
                rpm_count += 1

def listen_rpm(line):
    thread = threading.Thread(target=read_rpm, args=(line))
    thread.daemon = True
    thread.start()

def get_rpm():
    if simulation_mode:
        return sim_rpm
    else:
        pulse_sum = sum(rpm_pulse_buffer)
        return (pulse_sum / calculation_interval) * (60 / pulses_per_revolution)

def set_sim_rpm(rpm):
    global sim_rpm
    sim_rpm = int(rpm)