from tkinter import Canvas
from baby import Baby

# super class of specific canvas types, the habitat of a Baby
# has x - y size
# has a Baby instance
# has a pre_size_mod, to store the previous size modificator to implement zooming


class GeneralCanvas(Canvas):

    def __init__(self, root, *args):
        Canvas.__init__(self, root, *args)
        self.x_size = int(args[0]['width'])
        self.y_size = int(args[0]['height'])
        self.baby = Baby.Baby()
        self.pre_size_mod = 1

    def set_baby(self, baby):
        self.baby = baby

    def clear_canvas(self):
        self.baby = None
        self.delete('all')
