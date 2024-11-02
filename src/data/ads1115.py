import threading
import time

sleep_interval = 0.2

from ADS1x15 import ADS1115
adc = ADS1115(1)

adc.setMode(adc.MODE_SINGLE)
adc.setGain(0)

channels = list()
readings = dict()

thread = None

def _read():
    while True:
        for channel in channels:
            raw_value = adc.readADC(channel)
            voltage = adc.toVoltage(raw_value)
            readings[channel] = voltage
            time.sleep(sleep_interval)

def listen_adc(channel):
    global thread
    if thread == None:
        thread = threading.Thread(target=_read)
        thread.daemon = True
        thread.start()
    channels.append(channel)
    readings[channel] = 0

def get_adc(channel):
    return readings[channel]