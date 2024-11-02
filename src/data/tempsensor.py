import math
import os

simulation_mode = os.environ.get("SIMULATION_MODE") != None

temp_resistor = 470
temp_celsius = False
sim_temp = {
    1: 0,
    2: 0
}

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

def to_fahrenheit(temp):
    return (temp * 9 / 5) + 32

def listen_temp(adc_channel):
    if not simulation_mode:
        from .ads1115 import listen_adc
        listen_adc(adc_channel)

def get_temp(adc_channel, stock_sensor = False):
    if simulation_mode:
        return sim_temp[adc_channel]
    else:
        from .ads1115 import get_adc
        voltage = get_adc(adc_channel)
        resistance = (temp_resistor * voltage) / (3.3 - voltage)
        temp = resistance_to_temp(resistance, stock_sensor)
        return temp if temp_celsius else to_fahrenheit(temp)

def set_sim_temp(adc_channel, value):
    global sim_temp
    sim_temp[adc_channel] = float(value)