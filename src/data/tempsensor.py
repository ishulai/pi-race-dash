import threading
import os
import time

simulation_mode = os.environ.get("SIMULATION_MODE") != None

use_fahrenheit = True

display_interval = 1.0

sim_temp = 25

if not simulation_mode:
    from Adafruit_ADS1x15 import ADS1115
    adc = ADS1115()
    GAIN = 1

v_in = 3.3
r_fixed = 470

def read_temp_voltage():
    if simulation_mode:
        return 0
    raw_adc_value = adc.read_adc(1, gain=GAIN)
    voltage = raw_adc_value * (4.096 / 32767)
    return voltage

def calculate_temp_resistance(v_out, v_in=3.3, r_fixed=470):
    if v_out == 0:
        return float('inf')
    return r_fixed * ((v_in / v_out) - 1)

def calculate_temperature(resistance):
    min_resistance = 20 
    max_resistance = 3000
    min_temp = 100
    max_temp = 0
    
    temp_celsius = max_temp + (min_temp - max_temp) * (resistance - min_resistance) / (max_resistance - min_resistance)
    return temp_celsius

def convert_to_fahrenheit(celsius_temp):
    return (celsius_temp * 9/5) + 32

def read_temp():
    global latest_temp
    while True:
        voltage = read_temp_voltage()
        resistance = calculate_temp_resistance(voltage)
        temp_celsius = calculate_temperature(resistance)
        latest_temp = temp_celsius
        time.sleep(display_interval)

def listen_temp():
    if not simulation_mode:
        thread = threading.Thread(target=read_temp)
        thread.daemon = True
        thread.start()

def get_temp():
    if simulation_mode:
        temp_celsius = sim_temp
    else:
        temp_celsius = latest_temp
    return convert_to_fahrenheit(temp_celsius) if use_fahrenheit else temp_celsius

def set_sim_temp(temp):
    global sim_temp
    sim_temp = int(temp)

def set_temp_unit(fahrenheit=False):
    global use_fahrenheit
    use_fahrenheit = fahrenheit
