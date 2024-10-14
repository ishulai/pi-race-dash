import gpiod
import time

# Define GPIO chip and lines (pins)
chip = gpiod.Chip('gpiochip0')  # The GPIO chip name may vary; 'gpiochip0' is typical
rpm_line = chip.get_line(17)  # GPIO pin 17 for RPM
speed_line = chip.get_line(18)  # GPIO pin 18 for speedometer

# Request both lines as input with edge detection for rising events (pulses)
rpm_line.request(consumer="RPM_Reader", type=gpiod.LINE_REQ_EV_RISING_EDGE)
speed_line.request(consumer="Speed_Reader", type=gpiod.LINE_REQ_EV_RISING_EDGE)

# Variables to store counts
rpm_count = 0
speed_count = 0
calculation_interval = 1.0  # Time window for calculating frequency in seconds

# Constants based on vehicle setup
pulses_per_revolution = 2  # Adjust for your engine's setup (e.g., 2 pulses per revolution)
pulses_per_km = 637  # Adjust for your speed sensor (typical value for E30)

def calculate_rpm(pulse_count, interval, pulses_per_revolution):
    return (pulse_count / interval) * (60 / pulses_per_revolution)

def calculate_speed(pulse_count, interval, pulses_per_km):
    return (pulse_count / interval) * (3600 / pulses_per_km)  # Speed in km/h

# Main loop to count pulses and calculate RPM and speed
try:
    while True:
        # Clear counts at the start of each interval
        rpm_count = 0
        speed_count = 0
        
        # Record start time
        start_time = time.time()

        # Poll for events within the time interval
        while time.time() - start_time < calculation_interval:
            # Poll for RPM event
            rpm_event = rpm_line.event_wait()
            if rpm_event:
                rpm_event = rpm_line.event_read()
                if rpm_event.type == gpiod.LineEvent.RISING_EDGE:
                    rpm_count += 1

            # Poll for speed event
            speed_event = speed_line.event_wait()
            if speed_event:
                speed_event = speed_line.event_read()
                if speed_event.type == gpiod.LineEvent.RISING_EDGE:
                    speed_count += 1

        # Calculate RPM and speed based on the pulse counts
        rpm = calculate_rpm(rpm_count, calculation_interval, pulses_per_revolution)
        speed = calculate_speed(speed_count, calculation_interval, pulses_per_km)

        # Print the results
        print(f"RPM: {rpm:.2f}, Speed: {speed:.2f} km/h")

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Release the lines when done
    rpm_line.release()
    speed_line.release()
