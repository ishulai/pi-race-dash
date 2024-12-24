import threading
import os

simulation_mode = os.environ.get("SIMULATION_MODE") != None

clutch_switch_state = 0
sim_clutch_switch = 0

def read_clutch_switch(clutch_switch_line):
    import gpiod

    global clutch_switch_state

    clutch_switch_line.request(consumer="Clutch_Switch_Reader", type=gpiod.LINE_REQ_EV_BOTH_EDGES, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)

    clutch_switch_state = clutch_switch_line.get_value()

    while True:
        fuel_event = clutch_switch_line.event_wait()
        if fuel_event:
            clutch_switch_state = clutch_switch_line.get_value()

def listen_clutch_switch(clutch_switch_line):
    thread = threading.Thread(target=read_clutch_switch, args=(clutch_switch_line,))
    thread.daemon = True
    thread.start()

def get_clutch_switch_state():
    if simulation_mode:
        return sim_clutch_switch
    else:
        return clutch_switch_state

def set_sim_clutch_switch(value):
    global sim_clutch_switch
    sim_clutch_switch = int(value)
