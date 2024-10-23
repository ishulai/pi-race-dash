import os
import time
import threading
import tkinter as tk
from src.helpers import calculate_gear
from src.ui.simulation import open_simulation_window
from src.data.rpm import listen_rpm, get_rpm
from src.data.speed import listen_speed, get_speed
from src.data.signals import listen_signals, get_left_signal, get_right_signal
from src.data.fuelswitch import listen_fuel_switch, get_fuel_switch_state

simulation_mode = os.environ.get("SIMULATION_MODE") != None

def start_cli():
    # if not simulation_mode:
    #     import gpiod
    #     chip = gpiod.Chip('gpiochip0')
    #     listen_rpm(chip.get_line(17))
    #     listen_speed(chip.get_line(27))
    #     listen_signals(chip.get_line(5), chip.get_line(6))
    #     listen_fuel_switch(chip.get_line(23))

    def log_signals():
        while True:
            rpm_value = get_rpm()
            speed_value = get_speed()
            gear_value = calculate_gear(speed_value, rpm_value)
            left_signal_on = get_left_signal()
            right_signal_on = get_right_signal()
            fuel_switch_on = get_fuel_switch_state()

            print("\033[H\033[J", end="")  # Clears the terminal
            print(f"RPM: {rpm_value}")
            print(f"Speed: {speed_value} MPH")
            print(f"Gear: {gear_value}")
            print(f"Left Signal: {'On' if left_signal_on else 'Off'}")
            print(f"Right Signal: {'On' if right_signal_on else 'Off'}")
            print(f"Low Fuel: {'On' if fuel_switch_on else 'Off'}")
            print("-" * 50)

            time.sleep(0.1)

    if simulation_mode:
        root = tk.Tk()
        open_simulation_window(root, 9000, 150)
        root.mainloop()

        thread = threading.Thread(target=log_signals)
        thread.daemon = True
        thread.start()
    else:
        log_signals()

if __name__ == "__main__":
    start_cli()
