# represent a cell in a baby
# has own equality method
# set the neighbours set automatically, when position is known


class Cell:

    def __init__(self, x=None, y=None):
        super().__init__()
        self.x_dim = 0
        self.y_dim = 0
        self.neighbours = set()
        if x is not None and y is not None:
            self.x = x
            self.y = y
            self.position = (x, y)
            self.set_neighbours()

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

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
