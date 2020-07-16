pre_size = 0


def start_simulation(habitat_canvas):
    print(len(habitat_canvas.baby.cells), habitat_canvas.baby.name)


def change_size(size_value, hab_canvas):
    print(size_value)
    global pre_size
    if pre_size < float(size_value) or pre_size == 0:
        size_mod = 0.9
    else:
        size_mod = 1.111111
    hab_canvas.scale('all', 0, 0, size_mod, size_mod)
    pre_size = float(size_value)


def change_speed(speed_value):
    print(speed_value)
