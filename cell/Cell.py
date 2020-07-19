class Cell(object):
    x: int = 0
    y: int = 0
    x_dim = 0
    y_dim = 0
    position = (x, y)
    dimension = {'x_dim': x_dim,
                 'y_dim': y_dim}
    neighbours: set()

    def __init__(self, x=None, y=None):
        if x is None or y is None:
            super(Cell, self).__init__()
        else:
            self.x = x
            self.y = y
            self.position = (x, y)
            self.neighbours = set()
            self.set_neighbours()
            super(Cell, self).__init__()

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.set_neighbours()

    def set_neighbours(self):
        self.neighbours.clear()
        position_x = self.position[0]
        position_y = self.position[1]
        self.neighbours.add((position_x - 1, position_y + 1))
        self.neighbours.add((position_x, position_y + 1))
        self.neighbours.add((position_x + 1, position_y + 1))
        self.neighbours.add((position_x + 1, position_y))
        self.neighbours.add((position_x - 1, position_y))
        self.neighbours.add((position_x - 1, position_y - 1))
        self.neighbours.add((position_x, position_y - 1))
        self.neighbours.add((position_x + 1, position_y - 1))
