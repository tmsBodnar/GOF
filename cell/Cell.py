class Cell(object):

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
        self.x_dim = 0
        self.y_dim = 0

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

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
