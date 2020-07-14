import tkinter as tk
from tkinter import *
import sys
from tkinter import filedialog, messagebox
from simulator import Simulator
from rleloader import RleLoader
from pathlib import Path
from baby import Baby

pattern_wrapper_options = {
    'width': '200',
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


# start app
def start_callback():
    print('started')


# exit app
def exit_callback():
    sys.exit()


# create pattern canvas to show pattern visually
def create_pattern_canvas(baby, row):
    wn_x = 0
    wn_y = 0
    es_x = 0
    es_y = 0
    pattern_canvas = Canvas(pattern_wrapper, pattern_canvas_options, scrollregion=(0, 0, 750, 750))
    pattern_canvas.grid(column=0, row=row, sticky=N + W)
    x_mod = int(pattern_canvas_options.get('width'))
    y_mod = int(pattern_canvas_options.get('height'))
    x_dim_is_bigger = True if baby.dimension[0] >= baby.dimension[1] else False
    dim_mod = x_mod / (baby.dimension[0] + 2) if x_dim_is_bigger else y_mod / (baby.dimension[1] + 2)
    center_mod = (baby.dimension[0] - baby.dimension[1]) / 2 if x_dim_is_bigger else (baby.dimension[1] - baby.dimension[0]) / 2
    for cell in baby.cells:
        cell.dimension = {'x_dim': dim_mod,
                          'y_dim': dim_mod}
    for cell in baby.cells:
        x = cell.position['x'] if x_dim_is_bigger else cell.position['x'] + center_mod
        y = cell.position['y'] + center_mod if x_dim_is_bigger else cell.position['y']
        wn_x = int(cell.dimension['x_dim'] + cell.dimension['x_dim'] * x)
        wn_y = int(cell.dimension['y_dim'] + cell.dimension['y_dim'] * y)
        es_x = int(cell.dimension['x_dim'] * 2 + cell.dimension['x_dim'] * x)
        es_y = int(cell.dimension['y_dim'] * 2 + cell.dimension['y_dim'] * y)
        pattern_canvas.create_rectangle(wn_x, wn_y, es_x, es_y, fill='#000000')


# load pattern to pattern_canvas
def load_pattern(file, row):
    extension = Path(file.name).suffix
    if extension.upper() != ".RLE":
        messagebox.showinfo("Wrong file type", "Please, load .rle files")
    else:
        baby = RleLoader.load_pattern(file)
        for widget in pattern_wrapper.winfo_children():
            widget.destroy()
        create_pattern_canvas(baby, row)


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
    print(path)
    base_path = Path(path)
    files_in_basepath = base_path.iterdir()
    pattern_wrapper.delete(ALL)
    for i, item in files_in_basepath:
        load_pattern(item, i)


def start_simulation_callback():
    print('sim started')


# menu
menu_bar = Menu(root)
app_menu = Menu(menu_bar, tearoff=0)
exit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='File', menu=app_menu)
app_menu.add_command(label="Start", compound='left', command=start_callback)
app_menu.add_command(label="Load file", compound='left', command=open_file_dialog)
app_menu.add_command(label="Load folder", compound='left', command=open_folder_dialog)
app_menu.add_command(label="Exit", compound='left', command=exit_callback)
root.config(menu=menu_bar)

pattern_wrapper = Canvas(root, pattern_wrapper_options)
pattern_wrapper.grid(column=0, row=0, rowspan=2, sticky=W + S + N + E)
# pattern_canvas = Canvas(pattern_wrapper, pattern_canvas_options, scrollregion=(0, 0, 750, 750))
# pattern_canvas.grid(column=0, row=0, sticky=N + W)
vbar = Scrollbar(root, orient=VERTICAL)
vbar.grid(column=1, row=0, rowspan=2, sticky=W + S + N)
vbar.config(command=pattern_wrapper.yview)
pattern_wrapper.configure(yscrollcommand=vbar.set)
pattern_wrapper.config(scrollregion=[0, 0, 800, 800])
# pattern_canvas2 = Canvas(pattern_wrapper, pattern_canvas_options)
# pattern_canvas2.grid(column=0, row=1, sticky=N+W)
# pattern_canvas3 = Canvas(pattern_wrapper, pattern_canvas_options)
# pattern_canvas3.grid(column=0, row=2, sticky=N+W)
# pattern_canvas4 = Canvas(pattern_wrapper, pattern_canvas_options)
# pattern_canvas4.grid(column=0, row=3, sticky=N+W)
start_button = Button(root, text='Start simulation', command=start_simulation_callback)
start_button.grid(column=0, row=1, sticky=S + E + W)

habitat_canvas = Canvas(root, habitat_canvas_options)
habitat_canvas.grid(column=2, row=0, rowspan=2, sticky=E + N)

root.mainloop()
