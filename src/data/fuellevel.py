import os

simulation_mode = os.environ.get("SIMULATION_MODE") != None

adc_channel = 0
fuel_resistor = 100
sim_fuel_level = 0

def resistance_to_fuel_level(resistance):
    resistance_to_fuel = [
        (74, 0),           # Empty
        (35, 5/16 * 100),  # 5/16 tank
        (24, 1/2 * 100),   # 1/2 tank
        (16, 5/8 * 100),   # 5/8 tank
        (11, 3/4 * 100),   # 3/4 tank
        (5, 100),          # Full
    ]
    
    if resistance >= resistance_to_fuel[0][0]:
        return resistance_to_fuel[0][1]
    elif resistance <= resistance_to_fuel[-1][0]:
        return resistance_to_fuel[-1][1]
    
    # Interpolate between the two nearest points
    for i in range(len(resistance_to_fuel) - 1):
        r1, f1 = resistance_to_fuel[i]
        r2, f2 = resistance_to_fuel[i + 1]
        if r1 >= resistance >= r2:
            return f1 + (f2 - f1) * (r1 - resistance) / (r1 - r2)

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
