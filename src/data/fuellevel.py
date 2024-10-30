import threading
import os
import time

simulation_mode = os.environ.get("SIMULATION_MODE") != None

interval = 1.0 

sim_fuel_level = 100

if not simulation_mode:
    from Adafruit_ADS1x15 import ADS1115
    adc = ADS1115()
    GAIN = 1

v_in = 3.3
r_fixed = 10

def read_fuel_voltage():
    if simulation_mode:
        return 0 
    raw_adc_value = adc.read_adc(0, gain=GAIN)
    voltage = raw_adc_value * (4.096 / 32767)
    return voltage

def calculate_fuel_resistance(v_out, v_in=3.3, r_fixed=10):
    if v_out == 0:
        return 0
    return r_fixed * ((v_in / v_out) - 1)

def calculate_fuel_level(resistance):
    full_resistance = 0 
    empty_resistance = 59
    
    fuel_level = max(0, min(100, (1 - (resistance / empty_resistance)) * 100))
    return fuel_level

def read_fuel():
    global latest_fuel_level
    while True:
        voltage = read_fuel_voltage()
        resistance = calculate_fuel_resistance(voltage)
        fuel_level = calculate_fuel_level(resistance)
        latest_fuel_level = fuel_level
        time.sleep(interval)

def listen_fuel():
    if not simulation_mode:
        thread = threading.Thread(target=read_fuel)
        thread.daemon = True
        thread.start()

def get_fuel_level():
    return sim_fuel_level if simulation_mode else latest_fuel_level

def set_sim_fuel_level(level):
    global sim_fuel_level
    sim_fuel_level = int(level)
