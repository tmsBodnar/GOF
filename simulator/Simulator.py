pre_size = 0


def start_simulation(sim_canvas):
    print(len(sim_canvas.baby.cells))
    temp_cells = sim_canvas.baby.cells.copy()
    for cell in sim_canvas.baby.cells:
        neighbours = []
        live_neighbours = 0
        position_x = cell.position['x']
        position_y = cell.position['y']
        neighbours.append({'x': position_x - 1, 'y': position_y + 1})
        neighbours.append({'x': position_x, 'y': position_y + 1})
        neighbours.append({'x': position_x + 1, 'y': position_y + 1})
        neighbours.append({'x': position_x + 1, 'y': position_y})
        neighbours.append({'x': position_x - 1, 'y': position_y})
        neighbours.append({'x': position_x - 1, 'y': position_y - 1})
        neighbours.append({'x': position_x, 'y': position_y - 1})
        neighbours.append({'x': position_x + 1, 'y': position_y - 1})
        for neighbour in neighbours:
            for curr_cell in sim_canvas.baby.cells:
                position = curr_cell.position
                if position['x'] == neighbour['x'] and position['y'] == neighbour['y']:
                    live_neighbours += 1
        if live_neighbours < 2 or live_neighbours > 4:
            temp_cells.remove(cell)
    sim_canvas.baby.cells.clear()
    sim_canvas.baby.cells = temp_cells.copy()
    print(len(sim_canvas.baby.cells))
    sim_canvas.fill_canvas_to_live()


def change_size(size_value, hab_canvas):
    global pre_size
    if pre_size < float(size_value) or pre_size == 0:
        size_mod = 0.9
    else:
        size_mod = 1.111111
    hab_canvas.scale('all', 0, 0, size_mod, size_mod)
    pre_size = float(size_value)


def change_speed(speed_value):
    print(speed_value)
