import os
import threading
import time
import math

simulation_mode = os.environ.get("SIMULATION_MODE") != None
update_interval = 0.1
voltage_0_psi = 0.5
voltage_100_psi = 4.5
oil_pressure = 0

def read_oil_pressure():
    if not simulation_mode:
        from ADS1x15 import ADS1115
        adc = ADS1115(1)

    while True:
        if simulation_mode:
            time.sleep(update_interval)
            continue
        
        global oil_pressure
        
        raw_value = adc.readADC(3)
        voltage = adc.toVoltage(raw_value)
        oil_pressure = voltage_to_pressure(voltage)
        
        time.sleep(update_interval)

def voltage_to_pressure(voltage):
    return (voltage - voltage_0_psi) / (voltage_100_psi - voltage_0_psi) * 100

def listen_oil_pressure():
    if not simulation_mode:
        thread = threading.Thread(target=read_oil_pressure)
        thread.daemon = True
        thread.start()

def get_oil_pressure():
    return oil_pressure

def set_sim_oil_pressure(value):
    global oil_pressure
    oil_pressure = float(value)