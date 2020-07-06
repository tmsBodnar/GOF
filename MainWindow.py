import tkinter as tk
from tkinter import *
import sys
from tkinter import filedialog, messagebox
from simulator import Simulator
from rleloader import RleLoader
from pathlib import Path

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


# load pattern to pattern_canvas
def load_pattern(file):
    extension = Path(file.name).suffix
    print(extension)
    if extension.upper() != ".RLE":
        messagebox.showinfo("Wrong file type", "Please, load .rle files")
    else:
        RleLoader.load_pattern(file)


# opens file dialog, and starts simulation with chosen file
def open_file_dialog():
    file = filedialog.askopenfile(mode='r')
    if file is not None:
        load_pattern(file)


#open folder to load all files from
def open_folder_dialog():
    path = filedialog.askdirectory()
    print(path)
    base_path = Path(path)
    files_in_basepath = base_path.iterdir()
    for item in files_in_basepath:
        load_pattern(item)


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
pattern_canvas = Canvas(pattern_wrapper, pattern_canvas_options, scrollregion=(0, 0, 750, 750))
pattern_canvas.grid(column=0, row=0, sticky=N + W)
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
