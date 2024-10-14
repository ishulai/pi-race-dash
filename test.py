import gpiod
import time

# Define the GPIO chip and line (output pin)
chip = gpiod.Chip('gpiochip0')  # The GPIO chip, typically 'gpiochip0'
output_line = chip.get_line(27)  # GPIO pin 17 (or any other pin you'd like to use)

# Define the desired RPM and conversion factors
desired_rpm = 3000  # Example RPM you want to simulate
pulses_per_revolution = 2  # Number of pulses per engine revolution (adjust as needed)

# Calculate the pulse frequency
# Formula: frequency (in Hz) = (RPM * pulses_per_revolution) / 60
pulse_frequency = (desired_rpm * pulses_per_revolution) / 60

# Calculate the time for each pulse (period)
# Formula: period (in seconds) = 1 / frequency
pulse_period = 1 / pulse_frequency  # Time in seconds for a complete pulse cycle (high + low)

# Request the GPIO pin as output
output_line.request(consumer="RPM_Simulator", type=gpiod.LINE_REQ_DIR_OUT)

# Main loop to generate the square wave signal
try:
    while True:
        # Set the GPIO pin HIGH (start of pulse)
        output_line.set_value(1)
        time.sleep(pulse_period / 2)  # High for half the period

        # Set the GPIO pin LOW (end of pulse)
        output_line.set_value(0)
        time.sleep(pulse_period / 2)  # Low for the other half of the period

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Release the line when done
    output_line.release()
