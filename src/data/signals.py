import threading
import os

simulation_mode = os.environ.get("SIMULATION_MODE") != None

left_signal_state = 0
right_signal_state = 0
hazard_state = 0

sim_left_signal = 0
sim_right_signal = 0

def read_signals():
    import gpiod

    global left_signal_state, right_signal_state

    chip = gpiod.Chip('gpiochip0')
    left_signal_line = chip.get_line(5)
    right_signal_line = chip.get_line(6)

    while True:
        left_event = left_signal_line.event_wait()
        if left_event:
            left_event = left_signal_line.event_read()
            if left_event.type == gpiod.LineEvent.RISING_EDGE:
                left_signal_state = 1
            else:
                left_signal_state = 0

        right_event = right_signal_line.event_wait()
        if right_event:
            right_event = right_signal_line.event_read()
            if right_event.type == gpiod.LineEvent.RISING_EDGE:
                right_signal_state = 1
            else:
                right_signal_state = 0

def listen_signals():
    thread = threading.Thread(target=read_signals)
    thread.daemon = True
    thread.start()

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