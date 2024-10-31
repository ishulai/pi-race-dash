def calculate_gear(speed, rpm):
    if speed == 0:
        return "N"
    ratio = rpm / speed
    if ratio < 44:
        return 5
    elif ratio < 55:
        return 4
    elif ratio < 72:
        return 3
    elif ratio < 105:
        return 2
    else:
        return 1