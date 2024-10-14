import gpiod
import time
import math
import threading

# Define the GPIO chip and lines (output pins)
chip = gpiod.Chip('gpiochip0')  # The GPIO chip, typically 'gpiochip0'
rpm_output_line = chip.get_line(27)  # GPIO pin 17 for RPM signal
speed_output_line = chip.get_line(23)  # GPIO pin 18 for Speed signal

# Define the RPM range and vehicle speed range
min_rpm = 800  # Idle RPM (e.g., 800 RPM)
max_rpm = 8000  # Max RPM when revved (e.g., 6000 RPM)
min_speed = 0  # Minimum speed (stationary)
max_speed = 120  # Max speed in mph (adjust as needed)

# Define the number of pulses per engine revolution and per kilometer
pulses_per_revolution = 2  # Adjust for your engine's setup (e.g., 2 pulses per revolution)
pulses_per_mi = 1025  # Adjust for your speed sensor (typical for an E30 is ~637 pulses per km)

# Define the acceleration/deceleration period (in seconds)
acceleration_period = 10  # Time to go from min to max RPM and speed and back down (in seconds)

# Function to calculate the pulse period (high + low time) based on frequency
def calculate_pulse_period(frequency):
    return 1 / frequency  # Period in seconds for a complete pulse cycle (high + low)

# Function to calculate RPM pulse frequency
def calculate_rpm_frequency(rpm):
    return (rpm * pulses_per_revolution) / 60  # Frequency in Hz

# Function to calculate speed pulse frequency
def calculate_speed_frequency(speed):
    return (speed * pulses_per_mi) / 3600  # Frequency in Hz (speed in km/h)

# Function to simulate the RPM signal in a separate thread
def generate_rpm_signal():
    rpm_output_line.request(consumer="RPM_Simulator", type=gpiod.LINE_REQ_DIR_OUT)
    start_time = time.time()
    
    try:
        while True:
            # Calculate the elapsed time
            elapsed_time = time.time() - start_time
            
            # Use a sine wave to smoothly vary the RPM between min and max
            rpm = min_rpm + (max_rpm - min_rpm) / 2 * (1 + math.sin(2 * math.pi * elapsed_time / acceleration_period))
            
            # Calculate the pulse period for the current RPM
            rpm_pulse_period = calculate_pulse_period(calculate_rpm_frequency(rpm))
            
            # Generate the RPM square wave signal
            rpm_output_line.set_value(1)  # Set GPIO pin HIGH (start of RPM pulse)
            time.sleep(rpm_pulse_period / 2)  # High for half the RPM period
            rpm_output_line.set_value(0)  # Set GPIO pin LOW (end of RPM pulse)
            time.sleep(rpm_pulse_period / 2)  # Low for the other half of the RPM period
            
            # Print the current RPM for debugging purposes
            print(f"Simulated RPM: {rpm:.2f}")

    except KeyboardInterrupt:
        print("Stopping RPM generation")
    finally:
        rpm_output_line.release()

# Function to simulate the Speed signal in a separate thread
def generate_speed_signal():
    speed_output_line.request(consumer="Speed_Simulator", type=gpiod.LINE_REQ_DIR_OUT)
    start_time = time.time()

    try:
        while True:
            # Calculate the elapsed time
            elapsed_time = time.time() - start_time

            # Use a sine wave to smoothly vary the speed between min and max
            speed = min_speed + (max_speed - min_speed) / 2 * (1 + math.sin(2 * math.pi * elapsed_time / acceleration_period))

            # Calculate the pulse period for the current speed
            speed_pulse_period = calculate_pulse_period(calculate_speed_frequency(speed))

            # Generate the Speed square wave signal
            speed_output_line.set_value(1)  # Set GPIO pin HIGH (start of speed pulse)
            time.sleep(speed_pulse_period / 2)  # High for half the Speed period
            speed_output_line.set_value(0)  # Set GPIO pin LOW (end of speed pulse)
            time.sleep(speed_pulse_period / 2)  # Low for the other half of the Speed period

            # Print the current speed for debugging purposes
            print(f"Simulated Speed: {speed:.2f} km/h")

    except KeyboardInterrupt:
        print("Stopping Speed generation")
    finally:
        speed_output_line.release()

# Main function to start both RPM and Speed threads
if __name__ == "__main__":
    # Create and start threads for RPM and Speed signal generation
    rpm_thread = threading.Thread(target=generate_rpm_signal)
    speed_thread = threading.Thread(target=generate_speed_signal)

    rpm_thread.start()
    speed_thread.start()

    try:
        # Keep the main thread running while the other threads do the work
        rpm_thread.join()
        speed_thread.join()

    except KeyboardInterrupt:
        print("Stopping both RPM and Speed signals")
