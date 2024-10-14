import RPi.GPIO as GPIO
import time

# GPIO pin assignments
RPM_PIN = 17  # Pin where RPM signal is connected
#SPEED_PIN = 18  # Pin where speedometer signal is connected

# Variables to store counts
rpm_count = 0
speed_count = 0

# Time window for calculating frequency
calculation_interval = 1.0  # in seconds

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RPM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(SPEED_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# RPM pulse handler
def rpm_pulse_callback(channel):
    global rpm_count
    rpm_count += 1

# Speedometer pulse handler
def speed_pulse_callback(channel):
    global speed_count
    speed_count += 1

# Attach event handlers for rising edge pulses
GPIO.add_event_detect(RPM_PIN, GPIO.RISING, callback=rpm_pulse_callback)
#GPIO.add_event_detect(SPEED_PIN, GPIO.RISING, callback=speed_pulse_callback)

def calculate_rpm():
    global rpm_count
    rpm = (rpm_count / calculation_interval) * (60 / pulses_per_revolution)
    rpm_count = 0  # reset count after calculation
    return rpm

def calculate_speed():
    global speed_count
    speed = (speed_count / calculation_interval) * (3600 / pulses_per_km)
    speed_count = 0  # reset count after calculation
    return speed

# Constants to adjust based on your car
pulses_per_revolution = 2  # Depends on your car's RPM signal source
#pulses_per_km = 637  # Depends on your car's wheel size and VSS

try:
    while True:
        time.sleep(calculation_interval)
        rpm = calculate_rpm()
        #speed = calculate_speed()

        #print(f"RPM: {rpm:.2f}, Speed: {speed:.2f} km/h")

except KeyboardInterrupt:
    GPIO.cleanup()
