class Baby(object):
    dimension = tuple()
    cells = set()
    cells_positions = set()
    neighbours = set()
    name = ''

    def __init__(self):
        super(Baby, self).__init__()

    def calculate_positions_and_neighbours_set(self, cells):
        self.cells_positions.clear()
        self.neighbours.clear()
        for cell in cells:
            self.cells_positions.add(cell.position)
            self.neighbours = self.neighbours.union(cell.neighbours)
        #self.neighbours.difference_update(self.cells_positions)