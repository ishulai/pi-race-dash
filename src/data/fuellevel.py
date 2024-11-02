import os
import threading
import time

simulation_mode = os.environ.get("SIMULATION_MODE") != None
update_interval = 5
adc_channel = 0
fuel_resistor = 100
fuel_level_percent = 0

def read_fuel():
    if not simulation_mode:
        from ADS1x15 import ADS1115
        adc = ADS1115(1)

    global fuel_level_percent
    while True:
        if simulation_mode:
            time.sleep(update_interval)
            continue
        
        raw_value = adc.readADC(adc_channel)
        voltage = adc.toVoltage(raw_value)
        resistance = (fuel_resistor * voltage) / (3.3 - voltage)
        fuel_level_percent = resistance_to_fuel_level(resistance)
        
        time.sleep(update_interval)

def resistance_to_fuel_level(resistance):
    # Map resistance to percentage, assuming 0 ohms = full, 59 ohms = empty
    if resistance >= 59:
        return 0
    elif resistance <= 0:
        return 100
    else:
        return (59 - resistance) / 59 * 100

def listen_fuel():
    if not simulation_mode:
        thread = threading.Thread(target=read_fuel)
        thread.daemon = True
        thread.start()

def get_fuel_level():
    return fuel_level_percent

def set_sim_fuel_level(value):
    global fuel_level_percent
    fuel_level_percent = float(value)
