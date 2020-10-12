from tkinter import Canvas
from baby import Baby

x_size = 1
y_size = 1
pre_size_mod = 1;


class PatternCanvas(Canvas):
    baby = Baby.Baby()

    def __init__(self, root, *args):
        Canvas.__init__(self, root, *args)

    def set_baby(self, baby):
        self.baby = baby

    def fill_canvas_with_baby_cells(self):
        global x_size
        global y_size
        self.update()
        x_size = self.winfo_width()
        y_size = self.winfo_height()
        x_mod = x_size
        y_mod = y_size
        x_dim_is_bigger = True if self.baby.dimension[0] >= self.baby.dimension[1] else False
        dim_mod = int(x_mod / (self.baby.dimension[0] + 2)) if x_dim_is_bigger \
            else int(y_mod / (self.baby.dimension[1] + 2))
        center_mod = int((self.baby.dimension[0] - self.baby.dimension[1]) / 2) if x_dim_is_bigger \
            else int((self.baby.dimension[1] - self.baby.dimension[0]) / 2)
        side_mod = 1 if dim_mod < 10 else 0
        for cell in self.baby.cells:
            cell.dimension = {'x_dim': dim_mod,
                              'y_dim': dim_mod}
        for cell in self.baby.cells:
            x = cell.position[0] + side_mod if x_dim_is_bigger else cell.position[0] + center_mod
            y = cell.position[1] + center_mod if x_dim_is_bigger else cell.position[1] + side_mod
            wn_x = int(cell.dimension['x_dim'] + cell.dimension['x_dim'] * x)
            wn_y = int(cell.dimension['y_dim'] + cell.dimension['y_dim'] * y)
            es_x = int(cell.dimension['x_dim'] * 2 + cell.dimension['x_dim'] * x)
            es_y = int(cell.dimension['y_dim'] * 2 + cell.dimension['y_dim'] * y)
            self.create_rectangle(wn_x, wn_y, es_x, es_y, fill='#000000', outline='#D3D3D3', tags=self.baby.name)

        self.create_text(100, 10, text=self.baby.name)

    def fill_canvas_to_live(self, size_mod):
        global x_size
        global y_size
        global pre_size_mod
        self.update()
        if pre_size_mod != size_mod:
            self.change_size(size_mod)
            pre_size_mod = size_mod
        x_mod = x_size
        y_mod = y_size
        x_dim_is_bigger = True if self.baby.dimension[0] >= self.baby.dimension[1] else False
        canvas_ratio = x_mod / self.baby.dimension[0] / 10 if x_dim_is_bigger else y_mod / self.baby.dimension[0] / 10
        dim_mod = int(x_mod / (self.baby.dimension[0] * canvas_ratio + 20)) if x_dim_is_bigger else int(
            y_mod / (self.baby.dimension[1] * canvas_ratio + 20))
        center_mod_y = int((y_mod - (self.baby.dimension[1] * canvas_ratio) * 4) / 2)
        center_mod_x = int((x_mod - (self.baby.dimension[0] * canvas_ratio) * 4) / 2)
        print(x_mod, y_mod, canvas_ratio, x_dim_is_bigger)
        print(dim_mod, center_mod_x, center_mod_y)
        for cell in self.baby.cells:
            cell.dimension = {'x_dim': dim_mod,
                              'y_dim': dim_mod}
        self.delete('all')
        for cell in self.baby.cells:
            x = cell.position[0] * cell.dimension['x_dim'] + center_mod_x if x_dim_is_bigger else cell.position[0] * \
                cell.dimension['x_dim'] + center_mod_y
            y = cell.position[1] * cell.dimension['y_dim'] + center_mod_y if x_dim_is_bigger else cell.position[1] * \
                cell.dimension['y_dim'] + center_mod_x
            wn_x = int(cell.dimension['x_dim'] + cell.dimension['x_dim'] + x)
            wn_y = int(cell.dimension['y_dim'] + cell.dimension['y_dim'] + y)
            es_x = int(cell.dimension['x_dim'] * 2 + cell.dimension['x_dim'] + x)
            es_y = int(cell.dimension['y_dim'] * 2 + cell.dimension['y_dim'] + y)
            self.create_rectangle(wn_x, wn_y, es_x, es_y, fill='#000000', outline='#D3D3D3')
        self.update()

    def change_size(self, size_value):
        global x_size
        global y_size
        if size_value > pre_size_mod:
            x_size *= 1.3
            y_size *= 1.3
        else:
            x_size *= 0.7
            y_size *= 0.7
        self.scale('all', 0, 0, size_value, size_value)

