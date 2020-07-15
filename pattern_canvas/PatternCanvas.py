from tkinter import Canvas
from baby import Baby


class PatternCanvas(Canvas):
    baby: Baby

    def __init__(self, root, *args):
        Canvas.__init__(self, root, *args)

    def set_baby(self, baby):
        self.baby = baby

    def fill_canvas_with_baby_cells(self):
        self.update()
        x_mod = self.winfo_width()
        y_mod = self.winfo_height()
        x_dim_is_bigger = True if self.baby.dimension[0] >= self.baby.dimension[1] else False
        dim_mod = int(x_mod / (self.baby.dimension[0] + 2)) if x_dim_is_bigger else int(y_mod / (self.baby.dimension[1] + 2))
        center_mod = int((self.baby.dimension[0] - self.baby.dimension[1]) / 2) if x_dim_is_bigger else int(
            (self.baby.dimension[1] - self.baby.dimension[0]) / 2)
        side_mod = 1 if dim_mod < 10 else 0
        for cell in self.baby.cells:
            cell.dimension = {'x_dim': dim_mod,
                              'y_dim': dim_mod}
        for cell in self.baby.cells:
            x = cell.position['x'] + side_mod if x_dim_is_bigger else cell.position['x'] + center_mod
            y = cell.position['y'] + center_mod if x_dim_is_bigger else cell.position['y'] + side_mod
            wn_x = int(cell.dimension['x_dim'] + cell.dimension['x_dim'] * x)
            wn_y = int(cell.dimension['y_dim'] + cell.dimension['y_dim'] * y)
            es_x = int(cell.dimension['x_dim'] * 2 + cell.dimension['x_dim'] * x)
            es_y = int(cell.dimension['y_dim'] * 2 + cell.dimension['y_dim'] * y)
            self.create_rectangle(wn_x, wn_y, es_x, es_y, fill='#000000', outline='#D3D3D3', tags=self.baby.name)

        self.create_text(100, 10, text=self.baby.name)

    def fill_canvas_to_live(self):
        self.update()
        x_mod = self.winfo_width()
        y_mod = self.winfo_height()
        x_dim_is_bigger = True if self.baby.dimension[0] >= self.baby.dimension[1] else False
        canvas_ratio = x_mod / self.baby.dimension[0] / 10 if x_dim_is_bigger else y_mod / self.baby.dimension[0] / 10
        dim_mod = int(x_mod / (self.baby.dimension[0] * canvas_ratio + 2)) if x_dim_is_bigger else int(
            y_mod / (self.baby.dimension[1] * canvas_ratio + 2))
        center_mod = int((y_mod - (self.baby.dimension[1] * canvas_ratio) * 4) / 2)
        side_mod = int((x_mod - (self.baby.dimension[0] * canvas_ratio) * 4) / 2)
        for cell in self.baby.cells:
            cell.dimension = {'x_dim': dim_mod,
                              'y_dim': dim_mod}
        for cell in self.baby.cells:
            x = cell.position['x'] * cell.dimension['x_dim'] + side_mod if x_dim_is_bigger else cell.position['x'] * \
                cell.dimension['x_dim'] + center_mod
            y = cell.position['y'] * cell.dimension['y_dim'] + center_mod if x_dim_is_bigger else cell.position['y'] * \
                cell.dimension['y_dim'] + side_mod
            wn_x = int(cell.dimension['x_dim'] + cell.dimension['x_dim'] + x)
            wn_y = int(cell.dimension['y_dim'] + cell.dimension['y_dim'] + y)
            es_x = int(cell.dimension['x_dim'] * 2 + cell.dimension['x_dim'] + x)
            es_y = int(cell.dimension['y_dim'] * 2 + cell.dimension['y_dim'] + y)
            self.create_rectangle(wn_x, wn_y, es_x, es_y, fill='#000000', outline='#D3D3D3')
