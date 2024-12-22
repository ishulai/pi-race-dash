def calculate_gear(speed, rpm, clutch):
    if speed == 0 or clutch == 1:
        return "N"
    ratio = rpm / speed
    if ratio < 44:
        return 5
    elif ratio < 55:
        return 4
    elif ratio < 75:
        return 3
    elif ratio < 115:
        return 2
    else:
        return 1