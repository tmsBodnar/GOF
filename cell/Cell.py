class Cell(object):
    x: int = 0
    y: int = 0
    x_dim = 0
    y_dim = 0
    position = {'x': x,
                'y': y}
    dimension = {'x_dim': x_dim,
                 'y_dim': y_dim}

    def __init__(self):
        super(Cell, self).__init__()
