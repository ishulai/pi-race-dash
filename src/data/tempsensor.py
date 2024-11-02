import os
import threading
import time
import math

simulation_mode = os.environ.get("SIMULATION_MODE") != None
update_interval = 5
temp_resistor = 470
temp_celsius = False
temperature_c = {
    1: 0,
    2: 0
}

def read_temp(adc_channel, stock_sensor):
    if not simulation_mode:
        from ADS1x15 import ADS1115
        adc = ADS1115(1)

    while True:
        if simulation_mode:
            time.sleep(update_interval)
            continue
        
        raw_value = adc.readADC(adc_channel)
        voltage = adc.toVoltage(raw_value)
        resistance = (temp_resistor * voltage) / (3.3 - voltage)
        
        global temperature_c
        temperature_c[adc_channel] = resistance_to_temp(resistance, stock_sensor)
        
        time.sleep(update_interval)

def resistance_to_temp(resistance, stock_sensor):
    if stock_sensor:
      A = 1.743591812e-3
      B = 2.413388475e-4
      C = 1.391160959e-7
    else:
      A = 1.512189580e-3
      B = 2.374512684e-4
      C = -0.04684082023e-7
    temperature_kelvin = 1 / (A + B * math.log(resistance) + C * math.pow(math.log(resistance), 3))
    temperature_celsius = temperature_kelvin - 273.15
    return temperature_celsius

def listen_temp(adc_channel, stock_sensor = False):
    if not simulation_mode:
        thread = threading.Thread(target=read_temp, args=(adc_channel, stock_sensor))
        thread.daemon = True
        thread.start()

def get_temp(adc_channel):
    t = temperature_c[adc_channel]
    return t if temp_celsius else (t * 9/5) + 32

def set_sim_temp(adc_channel, value):
    global temperature_c
    temperature_c[adc_channel] = float(value)