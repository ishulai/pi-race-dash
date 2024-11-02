import os
import threading
import time
import math

update_interval = 1
temp_resistor = 470
temp_celsius = False
temperature_c = {
    1: 0,
    2: 0
}
fuel_resistor = 100
fuel_level_percent = 0
voltage_0_psi = 0.5
voltage_100_psi = 4.5
oil_pressure = 0

from ADS1x15 import ADS1115
adc = ADS1115(1)

adc.setMode(adc.MODE_SINGLE)
adc.setGain(0)

def read():
    global temperature_c
    global fuel_level_percent
    global oil_pressure
    while True:
        raw_value = adc.readADC(0)
        voltage = adc.toVoltage(raw_value)
        resistance = (fuel_resistor * voltage) / (3.3 - voltage)
        fuel_level_percent = resistance_to_fuel_level(resistance)

        print("\033[H\033[J", end="")
        print(f"Fuel Level: {fuel_level_percent}%")
        print(f"Water Temp: {temperature_c[1]}°C")
        print(f"Oil Temp: {temperature_c[2]}°C")
        print(f"Oil Pressure: {oil_pressure} psi")
        print("-" * 50)
        
        time.sleep(update_interval)
        
        raw_value = adc.readADC(1)
        voltage = adc.toVoltage(raw_value)
        resistance = (fuel_resistor * voltage) / (3.3 - voltage)
        temperature_c[1] = resistance_to_temp(resistance, True)

        print("\033[H\033[J", end="")
        print(f"Fuel Level: {fuel_level_percent}%")
        print(f"Water Temp: {temperature_c[1]}°C")
        print(f"Oil Temp: {temperature_c[2]}°C")
        print(f"Oil Pressure: {oil_pressure} psi")
        print("-" * 50)
        
        time.sleep(update_interval)
        
        raw_value = adc.readADC(2)
        voltage = adc.toVoltage(raw_value)
        resistance = (fuel_resistor * voltage) / (3.3 - voltage)
        temperature_c[2] = resistance_to_temp(resistance, False)

        print("\033[H\033[J", end="")
        print(f"Fuel Level: {fuel_level_percent}%")
        print(f"Water Temp: {temperature_c[1]}°C")
        print(f"Oil Temp: {temperature_c[2]}°C")
        print(f"Oil Pressure: {oil_pressure} psi")
        print("-" * 50)
        
        time.sleep(update_interval)
        
        raw_value = adc.readADC(3)
        voltage = adc.toVoltage(raw_value)
        oil_pressure = voltage_to_pressure(voltage)

        print("\033[H\033[J", end="")
        print(f"Fuel Level: {fuel_level_percent}%")
        print(f"Water Temp: {temperature_c[1]}°C")
        print(f"Oil Temp: {temperature_c[2]}°C")
        print(f"Oil Pressure: {oil_pressure} psi")
        print("-" * 50)
        
        time.sleep(update_interval)

def resistance_to_fuel_level(resistance):
    # Map resistance to percentage, assuming 0 ohms = full, 59 ohms = empty
    if resistance >= 59:
        return 0
    elif resistance <= 0:
        return 100
    else:
        return (59 - resistance) / 59 * 100

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

def voltage_to_pressure(voltage):
    return (voltage - voltage_0_psi) / (voltage_100_psi - voltage_0_psi) * 100

read()