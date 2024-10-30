import os
import time
import threading
from ADS1x15 import ADS1115

simulation_mode = os.environ.get("SIMULATION_MODE") != None
update_interval = 1.0  # Update every 1 second
adc_channel = 0  # ADC channel for the temperature sensor
temp_resistor = 1000  # Adjust based on your voltage divider design

sim_temp = 0
temp_celsius = True  # Set to False if you want Fahrenheit

def read_temp():
    global sim_temp
    adc = ADS1115()  # Initialize the ADS1115 instance
    while True:
        # Read the ADC value for the temperature sensor
        raw_value = adc.read_voltage(adc_channel)
        
        # Convert the ADC reading to resistance (example formula based on your divider)
        resistance = (temp_resistor * raw_value) / (3.3 - raw_value)
        
        # Convert resistance to temperature based on the sensor's characteristics
        temperature_c = resistance_to_temp(resistance)
        
        # Store the temperature, converting if needed
        sim_temp = temperature_c if temp_celsius else (temperature_c * 9/5) + 32
        time.sleep(update_interval)

def resistance_to_temp(resistance):
    # Example: conversion based on sensor data
    return (resistance - 1000) / 10  # Placeholder formula; adjust to match sensor specs

def listen_temp():
    if not simulation_mode:
        thread = threading.Thread(target=read_temp)
        thread.daemon = True
        thread.start()

def get_temp():
    return sim_temp

def set_sim_temp(value):
    global sim_temp
    sim_temp = int(value)
