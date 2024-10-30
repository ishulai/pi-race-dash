import os
import threading
import time

simulation_mode = os.environ.get("SIMULATION_MODE") != None
update_interval = 1.0  # Update every 1 second
adc_channel = 1  # Channel where the temperature sensor is connected
temp_resistor = 1000  # Adjust this based on your divider design
temp_celsius = True  # Toggle between Celsius and Fahrenheit
sim_temp = 0

def read_temp():
    if not simulation_mode:
        from ADS1x15 import ADS1115
        adc = ADS1115(1)  # Initialize ADS1115 on I2C bus 1
        adc.setGain(2)    # Set gain for expected input range, adjust as needed

    global sim_temp
    while True:
        if simulation_mode:
            time.sleep(update_interval)
            continue
        
        # Read voltage and calculate resistance
        raw_value = adc.readADC(adc_channel)
        voltage = adc.toVoltage(raw_value)
        resistance = (temp_resistor * voltage) / (3.3 - voltage)
        
        # Convert resistance to temperature
        temperature_c = resistance_to_temp(resistance)
        sim_temp = temperature_c if temp_celsius else (temperature_c * 9/5) + 32
        
        time.sleep(update_interval)

def resistance_to_temp(resistance):
    # Replace with appropriate formula for your sensor
    return (resistance - 1000) / 10  # Example formula

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
