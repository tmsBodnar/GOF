from tkinter import Canvas
from baby import Baby


class GeneralCanvas(Canvas):
    baby = Baby.Baby()
    x_size: int
    y_size: int
    pre_size_mod = 1

    def __init__(self, root, *args):
        Canvas.__init__(self, root, *args)
        self.x_size = int(args[0]['width'])
        self.y_size = int(args[0]['height'])

    def set_baby(self, baby):
        self.baby = baby

    def clear_canvas(self):
        self.baby = None
        self.delete('all')
