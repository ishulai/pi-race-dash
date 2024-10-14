import gpiod
import time
import math

# Define the GPIO chip and line (output pin)
chip = gpiod.Chip('gpiochip0')  # The GPIO chip, typically 'gpiochip0'
output_line = chip.get_line(27)  # GPIO pin 27 (or any other pin you'd like to use)

# Define the RPM range and the number of pulses per engine revolution
min_rpm = 800  # Idle RPM (e.g., 800 RPM)
max_rpm = 6000  # Max RPM when revved (e.g., 6000 RPM)
pulses_per_revolution = 2  # Adjust for your engine's setup (e.g., 2 pulses per revolution)

# Define the acceleration/deceleration period (in seconds)
acceleration_period = 10  # Time to go from min RPM to max RPM and back down (in seconds)

# Request the GPIO pin as output
output_line.request(consumer="RPM_Simulator", type=gpiod.LINE_REQ_DIR_OUT)

# Function to calculate the pulse period (high + low time) based on RPM
def calculate_pulse_period(rpm):
    pulse_frequency = (rpm * pulses_per_revolution) / 60  # Frequency in Hz
    return 1 / pulse_frequency  # Period in seconds

# Main loop to simulate revving up and down
try:
    start_time = time.time()
    while True:
        # Calculate the elapsed time
        elapsed_time = time.time() - start_time

        # Use a sine wave to smoothly vary the RPM between min_rpm and max_rpm
        rpm = min_rpm + (max_rpm - min_rpm) / 2 * (1 + math.sin(2 * math.pi * elapsed_time / acceleration_period))

        # Calculate the pulse period for the current RPM
        pulse_period = calculate_pulse_period(rpm)

        # Generate the square wave signal
        output_line.set_value(1)  # Set GPIO pin HIGH (start of pulse)
        time.sleep(pulse_period / 2)  # High for half the period

        output_line.set_value(0)  # Set GPIO pin LOW (end of pulse)
        time.sleep(pulse_period / 2)  # Low for the other half of the period

        # Print the current RPM for debugging purposes
        print(f"Simulated RPM: {rpm:.2f}")

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Release the GPIO line when done
    output_line.release()
