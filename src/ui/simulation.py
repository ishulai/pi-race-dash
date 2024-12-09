import tkinter as tk

from src.data.rpm import set_sim_rpm
from src.data.speed import set_sim_speed
from src.data.signals import set_sim_left_signal, set_sim_right_signal
from src.data.fuelswitch import set_sim_fuel_switch  # Import the fuel switch simulation function
from src.data.tempsensor import set_sim_temp  # Import the temperature simulation function
from src.data.fuellevel import set_sim_fuel_level  # Import the fuel level simulation function
from src.data.oilpressure import set_sim_oil_pressure
from src.data.ignition import set_sim_ignition_state

def open_simulation_window(root, max_rpm, max_speed):
    sim_window = tk.Toplevel(root)
    sim_window.title("Simulation Controls")
    sim_window.geometry("400x600")
    
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

    # Fuel Level Slider
    fuel_slider = tk.Scale(sim_window, from_=0, to=100, orient=tk.HORIZONTAL, label="Fuel Level (%)", command=set_sim_fuel_level)
    fuel_slider.pack(fill=tk.X, padx=20, pady=10)

    # Water Temperature Slider
    water_temp_slider = tk.Scale(sim_window, from_=0, to=120, orient=tk.HORIZONTAL, label="Water Temperature (°C)", command=lambda x: set_sim_temp(1, x))
    water_temp_slider.pack(fill=tk.X, padx=20, pady=10)

    # Oil Temperature Slider
    oil_temp_slider = tk.Scale(sim_window, from_=0, to=120, orient=tk.HORIZONTAL, label="Oil Temperature (°C)", command=lambda x: set_sim_temp(2, x))
    oil_temp_slider.pack(fill=tk.X, padx=20, pady=10)

    # Oil Pressure Slider
    oil_pressure_slider = tk.Scale(sim_window, from_=0, to=100, orient=tk.HORIZONTAL, label="Oil Pressure (psi)", command=set_sim_oil_pressure)
    oil_pressure_slider.pack(fill=tk.X, padx=20, pady=10)

    # Ignition Toggle
    ignition_var = tk.IntVar()
    ignition_toggle = tk.Checkbutton(sim_window, text="Acc/Run/Start", variable=ignition_var, command=lambda: set_sim_ignition_state(ignition_var.get()))
    ignition_toggle.pack(fill=tk.X, padx=20, pady=5)