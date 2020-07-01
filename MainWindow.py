import tkinter as tk
from tkinter import *
import sys
from tkinter import filedialog
from simulator import Simulator

pattern_canvas_options ={
    'width': '200',
    'height': '727',
    'bg': 'White',
    'bd': '5'
}
habitat_canvas_options ={
    'width': '800',
    'bg': 'White',
    'height': '753',
    'bd': '5'
}

root = Tk()
root.geometry('1024x768')
root.title('Game of life')
root.configure(bg='black')
root.resizable(0, 0)


# start app
def start_callback():
    print('started')


# exit app
def exit_callback():
    sys.exit()


# opens file dialog, and starts simulation with chosen file
def open_file_dialog():
    file = filedialog.askopenfile(mode='r')
    if file is not None:
        Simulator.start_simulation(file)


def start_simulation_callback():
    print('sim started')


# menu
menu_bar = Menu(root)
app_menu = Menu(menu_bar, tearoff=0)
exit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='File', menu=app_menu)
app_menu.add_command(label="Start", compound='left', command=start_callback)
app_menu.add_command(label="Load", compound='left', command=open_file_dialog)
app_menu.add_command(label="Exit", compound='left', command=exit_callback)
root.config(menu=menu_bar)

# pattern canvas
start_button = Button(root, text='Start simulation', command=start_simulation_callback)
start_button.grid(column=0, row=1, sticky=N+S+E+W)


pattern_canvas = Canvas(root, pattern_canvas_options)
pattern_canvas.grid(column=0, row=0, sticky=N+S+E+W)


habitat_canvas = Canvas(root, habitat_canvas_options)
habitat_canvas.grid(column=1, row=0, rowspan=2, sticky=E+N)


root.mainloop()
