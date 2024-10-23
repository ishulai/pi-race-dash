import tkinter as tk

def render_rpm_bar(root, max_rpm, redline, y):
    rpm_bar = tk.Canvas(root, width=720, height=60, bg="gray", highlightthickness=0)
    rpm_bar.place(x=40, y=y)
    rpm_bar_fill = rpm_bar.create_rectangle(0, 0, 0, 50, fill="white", outline="white")
    rpm_bar.create_rectangle(0, 50, (redline - 500) / max_rpm * 720, 60, fill="green", outline="green")
    rpm_bar.create_rectangle((redline - 500) / max_rpm * 720, 50, redline / max_rpm * 720, 60, fill="orange", outline="orange")
    rpm_bar.create_rectangle(redline / max_rpm * 720, 50, 720, 60, fill="red", outline="red")
    return rpm_bar, rpm_bar_fill

def update_rpm_bar(rpm_bar, rpm_value, max_rpm):
    max_bar_width = 720
    fill_width = int(rpm_value / max_rpm * max_bar_width)
    rpm_bar.coords(rpm_bar.find_withtag("all")[0], 0, 0, fill_width, 50)
