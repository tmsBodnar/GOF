from pattern_canvas.GeneralCanvas import GeneralCanvas


class SimCanvas(GeneralCanvas):

    def fill_sim_canvas_to_live(self, size_mod):
        self.update()
        if self.pre_size_mod != size_mod:
            self.change_size(size_mod)
            self.pre_size_mod = size_mod
        x_mod = self.x_size
        y_mod = self.y_size
        x_dim_is_bigger = True if self.baby.dimension[0] >= self.baby.dimension[1] else False
        canvas_ratio = x_mod / self.baby.dimension[0] / 10 if x_dim_is_bigger else y_mod / self.baby.dimension[0] / 10
        dim_mod = int(x_mod / (self.baby.dimension[0] * canvas_ratio + 20)) if x_dim_is_bigger else int(
            y_mod / (self.baby.dimension[1] * canvas_ratio + 20))
        center_mod_y = int(self.winfo_height() / 2) - self.baby.dimension[1] * dim_mod
        center_mod_x = int(self.winfo_width() / 2) - self.baby.dimension[0] * dim_mod
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
        if size_value > self.pre_size_mod:
            size_value = 1.3
            self.x_size *= 1.3
            self.y_size *= 1.3
        else:
            size_value = 0.7
            self.x_size *= 0.7
            self.y_size *= 0.7
        self.scale('all', 0, 0, size_value, size_value)
