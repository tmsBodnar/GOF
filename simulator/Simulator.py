from cell.Cell import Cell

temp_cells = set()


def start_simulation(sim_canvas, size_mod):
    calculate_next_gen_cells(sim_canvas)
    sim_canvas.baby.cells.clear()
    sim_canvas.baby.cells = temp_cells.copy()
    sim_canvas.baby.calculate_positions_and_neighbours_set(sim_canvas.baby.cells)
    sim_canvas.fill_canvas_to_live(size_mod)


def calculate_next_gen_cells(sim_canvas):
    global temp_cells
    temp_cells.clear()
    temp_cells = sim_canvas.baby.cells.copy()
    for cell in sim_canvas.baby.cells:
        temp = cell.neighbours.copy()
        temp.intersection_update(sim_canvas.baby.cells_positions)
        dead = len(temp)
        if dead < 2 or dead > 3:
            temp_cells.remove(cell)
        for neighbour in cell.neighbours:
            neighbour_cell = Cell(neighbour[0], neighbour[1])
            neighbour_cell.neighbours.intersection_update(sim_canvas.baby.cells_positions)
            live_neighbours = len(neighbour_cell.neighbours)
            if live_neighbours == 3:
                new_cell = Cell(neighbour[0], neighbour[1])
                temp_cells.add(new_cell)


