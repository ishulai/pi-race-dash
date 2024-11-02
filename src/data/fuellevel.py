import os

simulation_mode = os.environ.get("SIMULATION_MODE") != None

adc_channel = 0
fuel_resistor = 100
sim_fuel_level = 0

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
        from .ads1115 import listen_adc
        listen_adc(adc_channel)

def get_fuel_level():
    if simulation_mode:
        return sim_fuel_level
    else:
        from .ads1115 import get_adc
        voltage = get_adc(adc_channel)
        resistance = (fuel_resistor * voltage) / (3.3 - voltage)
        fuel_level_percent = resistance_to_fuel_level(resistance)
        return fuel_level_percent

def set_sim_fuel_level(value):
    global sim_fuel_level
    sim_fuel_level = float(value)
