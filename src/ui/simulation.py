import tkinter as tk

from src.data.rpm import set_sim_rpm
from src.data.speed import set_sim_speed
from src.data.signals import set_sim_left_signal, set_sim_right_signal
from src.data.fuelswitch import set_sim_fuel_switch  # Import the fuel switch simulation function
from src.data.tempsensor import set_sim_temp  # Import the temperature simulation function
from src.data.fuellevel import set_sim_fuel_level  # Import the fuel level simulation function

def open_simulation_window(root, max_rpm, max_speed):
    sim_window = tk.Toplevel(root)
    sim_window.title("Simulation Controls")
    sim_window.geometry("400x450")
    
    # RPM and Speed Sliders
    rpm_slider = tk.Scale(sim_window, from_=0, to=max_rpm, orient=tk.HORIZONTAL, label="RPM", command=set_sim_rpm)
    rpm_slider.pack(fill=tk.X, padx=20, pady=10)
    
    speed_slider = tk.Scale(sim_window, from_=0, to=max_speed, orient=tk.HORIZONTAL, label="Speed", command=set_sim_speed)
    speed_slider.pack(fill=tk.X, padx=20, pady=10)

    # Left and Right Turn Signal Toggles
    left_signal_var = tk.IntVar()
    right_signal_var = tk.IntVar()

    left_signal_toggle = tk.Checkbutton(sim_window, text="Left Turn Signal", variable=left_signal_var, command=lambda: set_sim_left_signal(left_signal_var.get()))
    left_signal_toggle.pack(fill=tk.X, padx=20, pady=5)

    right_signal_toggle = tk.Checkbutton(sim_window, text="Right Turn Signal", variable=right_signal_var, command=lambda: set_sim_right_signal(right_signal_var.get()))
    right_signal_toggle.pack(fill=tk.X, padx=20, pady=5)

    # Low Fuel Toggle
    low_fuel_var = tk.IntVar()
    low_fuel_toggle = tk.Checkbutton(sim_window, text="Low Fuel", variable=low_fuel_var, command=lambda: set_sim_fuel_switch(low_fuel_var.get()))
    low_fuel_toggle.pack(fill=tk.X, padx=20, pady=5)

    # Temperature Slider
    temp_slider = tk.Scale(sim_window, from_=0, to=120, orient=tk.HORIZONTAL, label="Water Temperature (°C)", command=set_sim_temp)
    temp_slider.pack(fill=tk.X, padx=20, pady=10)

    # Fuel Level Slider
    fuel_slider = tk.Scale(sim_window, from_=0, to=100, orient=tk.HORIZONTAL, label="Fuel Level (%)", command=set_sim_fuel_level)
    fuel_slider.pack(fill=tk.X, padx=20, pady=10)
