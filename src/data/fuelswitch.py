import threading
import os

simulation_mode = os.environ.get("SIMULATION_MODE") != None

fuel_switch_state = 0
sim_fuel_switch = 0

def read_fuel_switch(fuel_switch_line):
    import gpiod

    global fuel_switch_state

    fuel_switch_line.request(consumer="Fuel_Switch_Reader", type=gpiod.LINE_REQ_EV_BOTH_EDGES, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)

    fuel_switch_state = not fuel_switch_line.get_value()

    while True:
        fuel_event = fuel_switch_line.event_wait()
        if fuel_event:
            fuel_switch_state = not fuel_switch_line.get_value()

def listen_fuel_switch(fuel_switch_line):
    thread = threading.Thread(target=read_fuel_switch, args=(fuel_switch_line,))
    thread.daemon = True
    thread.start()

def get_fuel_switch_state():
    if simulation_mode:
        return sim_fuel_switch
    else:
        return fuel_switch_state

def set_sim_fuel_switch(value):
    global sim_fuel_switch
    sim_fuel_switch = int(value)
