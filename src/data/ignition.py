import threading
import os

simulation_mode = os.environ.get("SIMULATION_MODE") != None

ignition_state = 0
sim_ignition = 0

def read_ignition(ignition_line):
    import gpiod

    global ignition_state

    ignition_line.request(consumer="Ignition_Reader", type=gpiod.LINE_REQ_EV_BOTH_EDGES, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)

    ignition_state = ignition_line.get_value()

    while True:
        ignition_event = ignition_line.event_wait()
        if ignition_event:
            ignition_state = ignition_line.get_value()

def listen_ignition(ignition_line):
    thread = threading.Thread(target=read_ignition, args=(ignition_line,))
    thread.daemon = True
    thread.start()

def get_ignition_state():
    if simulation_mode:
        return sim_ignition
    else:
        return ignition_state

def set_sim_ignition_state(value):
    global sim_ignition
    sim_ignition = int(value)
