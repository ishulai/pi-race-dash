import threading
import os
import time
from collections import deque

simulation_mode = os.environ.get("SIMULATION_MODE") != None

display_interval = 0.1
revs_per_mi = 846
pulses_per_rev = 9
pulses_per_mi = revs_per_mi * pulses_per_rev
calculation_interval = 1.0
num_intervals = int(calculation_interval / display_interval)

pulse_buffer = deque([0] * num_intervals, maxlen=num_intervals)
speed_count = 0

sim_speed = 0

min_debounce_interval = 0.002  # 2ms

def calculate_dynamic_debounce(speed):
    if speed > 0:
        pulses_per_second = (speed / 3600) * pulses_per_mi
        time_between_pulses = 1 / pulses_per_second
        return max(time_between_pulses * 0.5, min_debounce_interval)
    else:
        return 0.1
    
def calculate_speed():
    pulse_sum = sum(pulse_buffer)
    return (pulse_sum / calculation_interval) * (3600 / pulses_per_mi)

def read_speed(chip):
    import gpiod

    global speed_count

    speed_line = chip.get_line(27)

    last_speed_time = 0
    while True:
        speed_event = speed_line.event_wait()
        if speed_event:
            speed_event = speed_line.event_read()
            current_time = time.time()
            current_speed = calculate_speed(pulse_buffer, pulses_per_mi)
            debounce_interval = calculate_dynamic_debounce(current_speed)
            if speed_event.type == gpiod.LineEvent.RISING_EDGE and (current_time - last_speed_time) > debounce_interval:
                speed_count += 1
                last_speed_time = current_time

def listen_speed(chip):
    thread = threading.Thread(target=read_speed, args=(chip))
    thread.daemon = True
    thread.start()

def get_speed():
    if simulation_mode:
        return sim_speed
    else:
        return calculate_speed()

def set_sim_speed(speed):
    global sim_speed
    sim_speed = int(speed)