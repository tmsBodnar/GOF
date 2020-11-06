from tkinter import *
from main_window import MainWindow

root = Tk()
root.geometry('1024x800')
root.title('Game of life')
root.resizable(0, 0)
my_gui = MainWindow.MainWindow(root)
root.mainloop()
