import threading
import os

simulation_mode = os.environ.get("SIMULATION_MODE") != None

left_signal_state = 0
right_signal_state = 0

sim_left_signal = 0
sim_right_signal = 0

def read_left_signal(line):
    import gpiod

    global left_signal_state
    line.request(consumer="Left_Signal_Reader", type=gpiod.LINE_REQ_EV_BOTH_EDGES)

    while True:
        event = line.event_wait()
        if event:
            event = line.event_read()
            if event.type == gpiod.LineEvent.RISING_EDGE:
                left_signal_state = 1
                print('left on')
            else:
                left_signal_state = 0
                print('left off')

def read_right_signal(line):
    import gpiod

    global right_signal_state
    line.request(consumer="Right_Signal_Reader", type=gpiod.LINE_REQ_EV_BOTH_EDGES)

    while True:
        event = line.event_wait()
        if event:
            event = line.event_read()
            if event.type == gpiod.LineEvent.RISING_EDGE:
                right_signal_state = 1
                print('right on')
            else:
                right_signal_state = 0
                print('right off')

def listen_signals(left_signal_line, right_signal_line):
    left_thread = threading.Thread(target=read_left_signal, args=(left_signal_line,))
    left_thread.daemon = True
    left_thread.start()
    right_thread = threading.Thread(target=read_right_signal, args=(right_signal_line,))
    right_thread.daemon = True
    right_thread.start()

def get_left_signal():
    if simulation_mode:
        return sim_left_signal
    else:
        return left_signal_state

def get_right_signal():
    if simulation_mode:
        return sim_right_signal
    else:
        return right_signal_state

def set_sim_left_signal(value):
    global sim_left_signal
    sim_left_signal = int(value)

def set_sim_right_signal(value):
    global sim_right_signal
    sim_right_signal = int(value)