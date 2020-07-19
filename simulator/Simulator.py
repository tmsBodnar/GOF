from cell.Cell import Cell

pre_size = 0
temp_cells = set()


def start_simulation(sim_canvas):
    calculate_died_cells(sim_canvas)
    print(len(temp_cells))
    calculate_born_cells(sim_canvas)
    print(len(temp_cells))
    sim_canvas.baby.cells.clear()
    sim_canvas.baby.cells = temp_cells.copy()
    sim_canvas.fill_canvas_to_live()


def calculate_born_cells(sim_canvas):
    global temp_cells
    temp_cell_positions = set()
    all_neighbours = set()
    for cell in sim_canvas.baby.cells:
        all_neighbours.update(cell.neighbours)
        temp_cell_positions.add(cell.position)
    all_neighbours.difference_update(temp_cell_positions)
    for neighbour in all_neighbours:
        live_neighbours = 0
        for cell in sim_canvas.baby.cells:
            if neighbour[0] - 2 < cell.position[0] < neighbour[0] + 2 \
                    and neighbour[1] - 2 < cell.position[1] < neighbour[1] + 2:
                live_neighbours += 1
        if live_neighbours == 3:
            new_cell = Cell(neighbour[0], neighbour[1])
            temp_cells.add(new_cell)


def calculate_died_cells(sim_canvas):
    global temp_cells
    temp_cells = sim_canvas.baby.cells.copy()
    for cell in sim_canvas.baby.cells:
        neighbours = cell.neighbours
        live_neighbours = 0
        for curr_cell in sim_canvas.baby.cells:
            if curr_cell.position in neighbours:
                live_neighbours += 1
        if live_neighbours < 2 or live_neighbours > 3:
            temp_cells.remove(cell)


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
