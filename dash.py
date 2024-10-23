import os
import tkinter as tk
from src.helpers import calculate_gear
from src.ui.signals import render_left_signal, render_right_signal, update_signal
from src.ui.rpm import render_rpm_bar, update_rpm_bar
from src.ui.textgauge import render_textgauge_large, render_textgauge_small, update_textgauge_value
from src.ui.simulation import open_simulation_window
from src.data.rpm import listen_rpm, get_rpm
from src.data.speed import listen_speed, get_speed
from src.data.signals import listen_signals, get_left_signal, get_right_signal

simulation_mode = os.environ.get("SIMULATION_MODE") != None

redline_rpm = 7000
max_rpm = 9000

def start(root):
    root.title("Dash")
    root.geometry("800x480")
    root.config(bg="black")

    signal_y = 30
    rpm_bar_y = 100
    row1_y = 170
    row2_y = 310
    
    left_signal_canvas, left_arrow = render_left_signal(root, 300, signal_y)
    right_signal_canvas, right_arrow = render_right_signal(root, 420, signal_y)
    
    rpm_bar, rpm_bar_fill = render_rpm_bar(root, max_rpm, redline_rpm, rpm_bar_y)

    rpm_label, rpm_label_value = render_textgauge_large(root, "RPM", 40, row1_y)
    speed_label, speed_label_value = render_textgauge_large(root, "MPH", 340, row1_y)
    gear_label, gear_label_value = render_textgauge_large(root, "GEAR", 640, row1_y, "N")

    water_temp_label, water_temp_label_value = render_textgauge_small(root, "WATER TEMP", "°F", 40, row2_y)
    oil_temp_label, oil_temp_label_value = render_textgauge_small(root, "OIL TEMP", "°F", 240, row2_y)
    oil_pressure_label, oil_pressure_label_value = render_textgauge_small(root, "OIL PRESSURE", "PSI", 440, row2_y)
    fuel_label, fuel_label_value = render_textgauge_small(root, "FUEL", "KG", 640, row2_y)

    def update_ui():
        rpm_value = get_rpm()
        update_rpm_bar(rpm_bar, rpm_value, max_rpm)
        update_textgauge_value(rpm_label_value, rpm_value)

        speed_value = get_speed()
        gear_value = calculate_gear(speed_value, rpm_value)
        update_textgauge_value(speed_label_value, speed_value)
        update_textgauge_value(gear_label_value, gear_value)

        left_signal_on = get_left_signal()
        right_signal_on = get_right_signal()
        update_signal(left_signal_canvas, left_arrow, left_signal_on)
        update_signal(right_signal_canvas, right_arrow, right_signal_on)

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
    else:
        open_simulation_window(root, 9000, 150)

    start(root)
