import tkinter as tk
from tkinter import *
import sys
from tkinter import filedialog, messagebox
from simulator import Simulator
from rleloader import RleLoader
from pathlib import Path
from baby import Baby
import os
from pattern_canvas.PatternCanvas import PatternCanvas

pattern_wrapper_options = {
    'width': '220',
    'height': '725',
    'bg': 'White',
    'bd': '5'
}
pattern_canvas_options = {
    'width': '200',
    'height': '200',
    'bg': 'White',
    'bd': '5'
}
habitat_canvas_options = {
    'width': '800',
    'bg': 'White',
    'height': '753',
    'bd': '5'
}
patterns = []

root = Tk()
root.geometry('1024x768')
root.title('Game of life')
root.resizable(0, 0)


# exit app
def exit_callback():
    sys.exit()


# opens file dialog, and starts simulation with chosen file
def open_file_dialog():
    file = filedialog.askopenfile(mode='r')
    if file is not None:
        for widget in pattern_wrapper.winfo_children():
            widget.destroy()
        load_pattern(file, 0)


# open folder to load all files from
def open_folder_dialog():
    path = filedialog.askdirectory()

    with os.scandir(path) as files:
        for i, file in enumerate(files, start=0):
            pattern = open(path + '/' + file.name)
            load_pattern(pattern, i)
            pattern.close()


def start_simulation():
    print('sim started')


def pattern_clicked(event):
    for widget in habitat_canvas.winfo_children():
        widget.destroy()

    print(len(event.widget.baby.cells), event.widget.baby.name)
    print(event.widget.find_closest(event.x, event.y))
    sim_canvas = PatternCanvas(habitat_canvas, habitat_canvas_options)
    sim_canvas.grid(column=0, row=0, sticky=N + W + S + E)
    create_and_draw_sim_canvas(event.widget.baby, sim_canvas)


def create_and_draw_sim_canvas(baby, sim_canvas):
    sim_canvas.set_baby(baby)
    sim_canvas.fill_canvas_to_live()


# load patterns to pattern_canvas
def load_pattern(file, row):
    extension = Path(file.name).suffix
    if extension.upper() != ".RLE":
        messagebox.showinfo("Wrong file type", "Please, load .rle files")
    else:
        baby = RleLoader.load_pattern(file)
        baby.name = (file.name.split("/")[-1]).split('.')[0]
        create_and_fill_pattern_canvas(baby, row)


# create patterns canvas to show patterns visually
def create_and_fill_pattern_canvas(baby, row):
    for widget in habitat_canvas.winfo_children():
        widget.destroy()
    pattern_canvas = PatternCanvas(pattern_wrapper, pattern_canvas_options)
    pattern_canvas.grid(column=0, row=row, sticky=N + W)
    pattern_canvas.set_baby(baby)
    pattern_canvas.fill_canvas_with_baby_cells()
    pattern_wrapper.create_window(100, 108 * (1 + row) + row * 108, window=pattern_canvas)
    pattern_canvas.bind("<Button-1>", pattern_clicked)


# menu
menu_bar = Menu(root)
app_menu = Menu(menu_bar, tearoff=0)
exit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='File', menu=app_menu)
app_menu.add_command(label="Load file", compound='left', command=open_file_dialog)
app_menu.add_command(label="Load folder", compound='left', command=open_folder_dialog)
app_menu.add_command(label="Exit", compound='left', command=exit_callback)
root.config(menu=menu_bar)

pattern_wrapper = Canvas(root, pattern_wrapper_options, scrollregion=(0, 0, 1000, 1000))
pattern_wrapper.grid(column=0, row=0, rowspan=2, sticky=W + S + N + E, )
vbar = Scrollbar(root, orient=VERTICAL)
vbar.grid(column=1, row=0, rowspan=2, sticky=W + S + N)
vbar.config(command=pattern_wrapper.yview)

pattern_wrapper.configure(yscrollcommand=vbar.set)
pattern_wrapper.config(scrollregion=pattern_wrapper.bbox(ALL))

start_button = Button(root, text='Start simulation', command=start_simulation)
start_button.grid(column=0, row=1, sticky=S + E + W)

habitat_canvas = Canvas(root, habitat_canvas_options)
habitat_canvas.grid(column=2, row=0, rowspan=2, sticky=E + N)

root.mainloop()
