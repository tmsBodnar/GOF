# represent a 'Baby', a pattern, which is a creature to live
# has a dimension, size in x - y aspect
# has set of cells
# has set of cell's positions
# has set of cell's neighbours


class Baby:

    def __init__(self):
        super().__init__()
        self.dimension = tuple()
        self.cells = set()
        self.cells_positions = set()
        self.neighbours = set()
        self.name = ''

    def calculate_positions_and_neighbours_set(self):
        self.cells_positions.clear()
        self.neighbours.clear()
        for cell in self.cells:
            self.cells_positions.add(cell.position)
            self.neighbours = self.neighbours.union(cell.neighbours)