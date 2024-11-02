import os
import math
import tkinter as tk
from src.helpers import calculate_gear
from src.ui.signals import render_left_signal, render_right_signal, update_signal
from src.ui.rpm import render_rpm_bar, update_rpm_bar
from src.ui.textgauge import render_textgauge_large, render_textgauge_small, update_textgauge_value_large, update_textgauge_value_small
from src.ui.simulation import open_simulation_window
from src.ui.fuelswitch import render_low_fuel_symbol, update_low_fuel_symbol
from src.ui.mileage import render_mileage, update_mileage
from src.data.rpm import listen_rpm, get_rpm
from src.data.speed import listen_speed, get_speed
from src.data.signals import listen_signals, get_left_signal, get_right_signal
from src.data.fuelswitch import listen_fuel_switch, get_fuel_switch_state
from src.data.tempsensor import listen_temp, get_temp
from src.data.fuellevel import listen_fuel, get_fuel_level

simulation_mode = os.environ.get("SIMULATION_MODE") != None

redline_rpm = 7000
max_rpm = 9000

ADC_WATER_TEMP = 1
ADC_OIL_TEMP = 2

def start(root):
    root.title("Dash")
    root.geometry("800x480")
    root.config(bg="black")

    signal_y = 30
    rpm_bar_y = 100
    row1_y = 170
    row2_y = 310
    row3_y = 420
    
    left_signal_canvas, left_arrow = render_left_signal(root, 300, signal_y)
    right_signal_canvas, right_arrow = render_right_signal(root, 420, signal_y)
    
    rpm_bar, rpm_bar_fill = render_rpm_bar(root, max_rpm, redline_rpm, rpm_bar_y)

    # Large text gauges without unit labels
    rpm_label, rpm_label_value = render_textgauge_large(root, "RPM", 40, row1_y)
    speed_label, speed_label_value = render_textgauge_large(root, "MPH", 340, row1_y)
    gear_label, gear_label_value = render_textgauge_large(root, "GEAR", 640, row1_y, "N")

    # Small text gauges with unit labels
    water_temp_label, water_temp_label_value, water_temp_unit_label = render_textgauge_small(root, "WATER TEMP", "°F", 40, row2_y)
    oil_temp_label, oil_temp_label_value, oil_temp_unit_label = render_textgauge_small(root, "OIL TEMP", "°F", 240, row2_y)
    oil_pressure_label, oil_pressure_label_value, oil_pressure_unit_label = render_textgauge_small(root, "OIL PRESSURE", "PSI", 440, row2_y)
    fuel_label, fuel_label_value, fuel_unit_label = render_textgauge_small(root, "FUEL", "%", 640, row2_y)

    fuel_switch_canvas, fuel_switch_image_item, fuel_switch_image = render_low_fuel_symbol(root, 725, row2_y)

    mileage_label, mileage_label_value = render_mileage(root, 40, row3_y)

    def update_ui():
        # Update RPM and speed gauges
        rpm_value = get_rpm()
        update_rpm_bar(rpm_bar, rpm_value, max_rpm)
        update_textgauge_value_large(root, rpm_label_value, rpm_value)

        speed_value = get_speed()
        update_textgauge_value_large(root, speed_label_value, speed_value)

        # Update gear gauge
        gear_value = calculate_gear(speed_value, rpm_value)
        update_textgauge_value_large(root, gear_label_value, gear_value)

        # Update turn signal states
        left_signal_on = get_left_signal()
        right_signal_on = get_right_signal()
        update_signal(left_signal_canvas, left_arrow, left_signal_on)
        update_signal(right_signal_canvas, right_arrow, right_signal_on)

        # Update low fuel symbol
        fuel_switch_on = get_fuel_switch_state()
        update_low_fuel_symbol(fuel_switch_canvas, fuel_switch_image_item, fuel_switch_on)
        
        fuel_level = math.floor(get_fuel_level())
        update_textgauge_value_small(root, fuel_label_value, fuel_level, fuel_unit_label)

        water_temp = math.floor(get_temp(ADC_WATER_TEMP))
        update_textgauge_value_small(root, water_temp_label_value, water_temp, water_temp_unit_label)

        oil_temp = math.floor(get_temp(ADC_OIL_TEMP))
        update_textgauge_value_small(root, oil_temp_label_value, oil_temp, oil_temp_unit_label)

        update_mileage(root, mileage_label_value, 30000.6, mileage_label)

        root.after(100, update_ui)

    root.after(100, update_ui)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()

    if not simulation_mode:
        import gpiod
        chip = gpiod.Chip('gpiochip0')
        listen_rpm(chip.get_line(17))
        listen_speed(chip.get_line(27))
        listen_signals(chip.get_line(5), chip.get_line(6))
        listen_fuel_switch(chip.get_line(23))
        listen_fuel()
        listen_temp(1, True)  # water temp
        listen_temp(2, False) # oil temp
    else:
        open_simulation_window(root, 9000, 150)

    start(root)
