import threading
import os

simulation_mode = os.environ.get("SIMULATION_MODE") != None

abs_state = 0
sim_abs = 0

def read_abs(abs_line):
    import gpiod

    global abs_state

    abs_line.request(consumer="ABS_Reader", type=gpiod.LINE_REQ_EV_BOTH_EDGES, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)

    abs_state = abs_line.get_value()

    while True:
        fuel_event = abs_line.event_wait()
        if fuel_event:
            abs_state = abs_line.get_value()

def listen_abs(abs_line):
    thread = threading.Thread(target=read_abs, args=(abs_line,))
    thread.daemon = True
    thread.start()

def get_abs_state():
    if simulation_mode:
        return sim_abs
    else:
        return abs_state

def set_sim_abs(value):
    global sim_abs
    sim_abs = int(value)
