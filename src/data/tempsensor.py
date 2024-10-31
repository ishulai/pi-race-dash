import os
import threading
import time
import math

simulation_mode = os.environ.get("SIMULATION_MODE") != None
update_interval = 0.1
adc_channel = 1
temp_resistor = 470
temp_celsius = False
temperature_c = 0

def read_temp():
    if not simulation_mode:
        from ADS1x15 import ADS1115
        adc = ADS1115(1)
        adc.setGain(2)

    while True:
        if simulation_mode:
            time.sleep(update_interval)
            continue
        
        raw_value = adc.readADC(adc_channel)
        voltage = adc.toVoltage(raw_value)
        resistance = (temp_resistor * voltage) / (3.3 - voltage)
        
        global temperature_c
        temperature_c = resistance_to_temp(resistance)
        
        time.sleep(update_interval)

def resistance_to_temp(resistance):
    # https://www.r3vlimited.com/board/forum/e30-technical-forums/general-technical/200903-coolant-temp-sensor-resistance-curve
    # coefficient = 0.00134876
    # constant = 3842.49
    # temperature_kelvin = constant / math.log(resistance / coefficient)
    # temperature_celsius = temperature_kelvin - 273.15
    # return temperature_celsius
    A = 1.743591812e-3
    B = 2.413388475e-4
    C = 1.391160959e-7
    temperature_kelvin = 1 / (A + B * math.log(resistance) + C * math.pow(math.log(resistance), 3))
    temperature_celsius = temperature_kelvin - 273.15
    return temperature_celsius

def listen_temp():
    if not simulation_mode:
        thread = threading.Thread(target=read_temp)
        thread.daemon = True
        thread.start()

def get_temp():
    return temperature_c if temp_celsius else (temperature_c * 9/5) + 32

def set_sim_temp(value):
    global temperature_c
    temperature_c = value
