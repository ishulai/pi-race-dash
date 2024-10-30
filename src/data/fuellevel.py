import os
import time
import threading
from ADS1x15 import ADS1115

simulation_mode = os.environ.get("SIMULATION_MODE") != None
update_interval = 1.0  # Update every 1 second
adc_channel = 1  # ADC channel for the fuel level sensor
fuel_resistor = 10  # Adjust based on your voltage divider design

sim_fuel_level = 0

def read_fuel():
    global sim_fuel_level
    adc = ADS1115()  # Initialize the ADS1115 instance
    while True:
        # Read the ADC value for the fuel level sensor
        raw_value = adc.read_voltage(adc_channel)
        
        # Convert the ADC reading to resistance (example formula based on your divider)
        resistance = (fuel_resistor * raw_value) / (3.3 - raw_value)
        
        # Map the resistance to fuel level percentage
        fuel_level_percent = resistance_to_fuel_level(resistance)
        
        # Store the fuel level
        sim_fuel_level = fuel_level_percent
        time.sleep(update_interval)

def resistance_to_fuel_level(resistance):
    # Example: linear mapping based on 0-59 ohms for full-empty
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
    return sim_fuel_level

def set_sim_fuel_level(value):
    global sim_fuel_level
    sim_fuel_level = int(value)
