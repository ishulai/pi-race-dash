import os
import threading
import time

simulation_mode = os.environ.get("SIMULATION_MODE") != None
update_interval = 1.0  # Update every 1 second
adc_channel = 0  # Channel where the fuel level sensor is connected
fuel_resistor = 10  # Adjust this based on your divider design
sim_fuel_level = 0

def read_fuel():
    if not simulation_mode:
        from ADS1x15 import ADS1115
        adc = ADS1115(1)  # Initialize ADS1115 on I2C bus 1
        adc.setGain(2)    # Set gain for expected input range, adjust as needed

    global sim_fuel_level
    while True:
        if simulation_mode:
            time.sleep(update_interval)
            continue
        
        # Read voltage and calculate resistance
        raw_value = adc.readADC(adc_channel)
        voltage = adc.toVoltage(raw_value)
        resistance = (fuel_resistor * voltage) / (3.3 - voltage)
        print("voltage")
        print(voltage)
        print("resistance")
        print(resistance)
        # Convert resistance to fuel level percentage
        fuel_level_percent = resistance_to_fuel_level(resistance)
        sim_fuel_level = fuel_level_percent
        
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
    return sim_fuel_level

def set_sim_fuel_level(value):
    global sim_fuel_level
    sim_fuel_level = int(value)
