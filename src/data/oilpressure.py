import os

simulation_mode = os.environ.get("SIMULATION_MODE") != None

adc_channel = 3
voltage_0_psi = 0.5
voltage_100_psi = 4.5
sim_oil_pressure = 0

def voltage_to_pressure(voltage):
    pressure = (voltage - voltage_0_psi) / (voltage_100_psi - voltage_0_psi) * 100
    return max(0, pressure)

def listen_oil_pressure():
    if not simulation_mode:
        from .ads1115 import listen_adc
        listen_adc(adc_channel)

def get_oil_pressure():
    if simulation_mode:
        return sim_oil_pressure
    else:
        from .ads1115 import get_adc
        voltage = get_adc(adc_channel)
        return voltage_to_pressure(voltage)

def set_sim_oil_pressure(value):
    global sim_oil_pressure
    sim_oil_pressure = float(value)