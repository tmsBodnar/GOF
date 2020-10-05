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
from simulator import Simulator


class MainWindow:

    pattern_wrapper_options = {
        'width': '220',
        'height': '700',
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
        'height': '725',
        'bd': '5'
    }
    patterns = []
    is_simulated = False
    timeout = 100
    timer_id = 0
    root: tk

    # exit app
    @staticmethod
    def exit_callback():
        sys.exit()

    # opens file dialog, and starts simulation with chosen file
    def open_file_dialog(self):
        file = filedialog.askopenfile(mode='r')
        if file is not None:
            for widget in self.pattern_wrapper.winfo_children():
                widget.destroy()
            self.load_pattern(file, 0)

    # open folder to load all files from
    def open_folder_dialog(self):
        path = filedialog.askdirectory()

        with os.scandir(path) as files:
            for i, file in enumerate(files, start=0):
                pattern = open(path + '/' + file.name)
                self.load_pattern(pattern, i)
                pattern.close()

    def pattern_clicked(self, event):
        self.sim_canvas.delete(ALL)
        self.create_and_draw_sim_canvas(event.widget.baby)

    def simulation_start(self):
        Simulator.start_simulation(self.sim_canvas)

    def simulation(self):
        if len(self.sim_canvas.baby.cells) > 0:
            if self.is_simulated:
                Simulator.start_simulation(self.sim_canvas)
                self.timer_id = self.master.after(self.timeout, self.simulation)
            else:
                self.stop_simulation()
        else:
            messagebox.showinfo("Choose a pattern!", "Please, click on a pattern")

    def run_simulation(self):
        Simulator.start_simulation(self.sim_canvas)

    def stop_simulation(self):
        self.master.after_cancel(self.timer_id)

    def create_and_draw_sim_canvas(self, baby):
        self.sim_canvas.set_baby(baby)
        self.sim_canvas.fill_canvas_to_live()

    # load patterns to pattern_canvas
    def load_pattern(self, file, row):
        extension = Path(file.name).suffix
        if extension.upper() != ".RLE":
            messagebox.showinfo("Wrong file type", "Please, load .rle files")
        else:
            baby = RleLoader.load_pattern(file)
            baby.name = (file.name.split("/")[-1]).split('.')[0]
            self.create_and_fill_pattern_canvas(baby, row)

    # create patterns canvas to show patterns visually
    def create_and_fill_pattern_canvas(self, baby, row):
        for widget in self.sim_canvas.winfo_children():
            widget.destroy()
        pattern_canvas = PatternCanvas(self.pattern_wrapper, self.pattern_canvas_options)
        pattern_canvas.grid(column=0, row=row, sticky=N + W)
        pattern_canvas.set_baby(baby)
        pattern_canvas.fill_canvas_with_baby_cells()
        self.pattern_wrapper.create_window(100, 108 * (1 + row) + row * 108, window=pattern_canvas)
        pattern_canvas.bind("<Button-1>", self.pattern_clicked)
        self.pattern_wrapper.configure(scrollregion=self.pattern_wrapper.bbox(ALL))

    def callback_zoom_plus(self, event):
        self.is_simulated = False
        self.sim_canvas.change_size(1.3)
        self.is_simulated = True

    def callback_zoom_minus(self, event):
        self.is_simulated = False
        self.sim_canvas.change_size(0.7)
        self.is_simulated = True

    def callback_speed_plus(self, event):
        self.timeout = int(self.timeout * 0.8)

    def callback_speed_minus(self, event):
        self.timeout = int(self.timeout * 1.2)

    def callback_step(self, event):
        self.is_simulated = True
        self.simulation()
        self.master.after_cancel(self.timer_id)

    def callback_pause(self, event):
        self.is_simulated = False
        self.master.after_cancel(self.timer_id)
        self.simulation()

    def callback_play(self, event):
        self.is_simulated = True
        self.simulation()

    def action(self):
        self.output.insert(Tk.END, self.variable.get())

    def __init__(self, master):
        self.timer_id = 0

        self.master = master

        self.pattern_wrapper = Canvas(master, self.pattern_wrapper_options, scrollregion=(0, 0, 1000, 1000))
        self.pattern_wrapper.grid(column=0, row=0, rowspan=2, sticky=W + S + N + E, padx=(2, 0), pady=(2, 2))
        self.vbar = Scrollbar(master, orient=VERTICAL)
        self.vbar.grid(column=1, row=0, rowspan=1, sticky=W + S + N)
        self.vbar.config(command=self.pattern_wrapper.yview)
        self.pattern_wrapper.configure(yscrollcommand=self.vbar.set)
        self.pattern_wrapper.config(scrollregion=self.pattern_wrapper.bbox(ALL))

        self.sim_canvas = PatternCanvas(master, self.habitat_canvas_options)
        self.sim_canvas.grid(column=2, row=0, sticky=E + N, columnspan=3, padx=2, pady=2)

        # menu
        self.menu_bar = Menu(master)
        self.app_menu = Menu(self.menu_bar, tearoff=0)
        self.exit_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='File', menu=self.app_menu)
        self.app_menu.add_command(label="Load file", compound='left', command=self.open_file_dialog)
        self.app_menu.add_command(label="Load folder", compound='left', command=self.open_folder_dialog)
        self.app_menu.add_command(label="Exit", compound='left', command=self.exit_callback)
        self.master.config(menu=self.menu_bar)

        self.zoom_wrapper = Entry(master)
        self.zoom_wrapper.grid(column=2, row=1, sticky=W + S, padx=4, pady=6)
        self.zoom_wrapper.grid_columnconfigure(2, weight=1)

        self.zoom_plus = Button(self.zoom_wrapper, text='+')
        self.zoom_plus.grid(column=2, row=1, sticky=W + S)
        self.zoom_plus.bind('<Button-1>', self.callback_zoom_plus)

        self.zoom_text = Label(self.zoom_wrapper, text='Zoom')
        self.zoom_text.grid(column=1, row=1, sticky=W + S, padx=4, pady=4)

        self.zoom_minus = Button(self.zoom_wrapper, text='-')
        self.zoom_minus.grid(column=0, row=1, sticky=W + S)
        self.zoom_minus.bind('<Button-1>', self.callback_zoom_minus)

        self.speed_wrapper = Entry(master)
        self.speed_wrapper.grid(column=3, row=1, sticky=W + S, padx=4, pady=6)
        self.speed_wrapper.grid_columnconfigure(3, weight=1)

        self.speed_plus = Button(self.speed_wrapper, text='+')
        self.speed_plus.grid(column=2, row=1, sticky=W + S)
        self.speed_plus.bind('<Button-1>', self.callback_speed_plus)

        self.speed_text = Label(self.speed_wrapper, text='Speed')
        self.speed_text.grid(column=1, row=1, sticky=W + S, padx=4, pady=4)

        self.speed_minus = Button(self.speed_wrapper, text='-')
        self.speed_minus.grid(column=0, row=1, sticky=W + S)
        self.speed_minus.bind('<Button-1>', self.callback_speed_minus)

        self.play_icon = PhotoImage(file="src/play.png")
        self.pause_icon = PhotoImage(file="src/pause.png")
        self.next_icon = PhotoImage(file="src/next.png")

        self.button_wrapper = Entry(master)
        self.button_wrapper.grid(column=4, row=1, sticky=W + S, padx=6, pady=3)
        self.button_wrapper.grid_columnconfigure(4, weight=2)

        self.play_button = Button(self.button_wrapper, image=self.play_icon, height=25, width=25)
        self.play_button.grid(column=0, row=0, sticky=W + N, padx=4, pady=4)
        self.play_button.bind('<Button-1>', self.callback_play)
        # play_button.grid_columnconfigure(0, weight=2)

        self.pause_button = Button(self.button_wrapper, image=self.pause_icon, height=25, width=25)
        self.pause_button.grid(column=1, row=0, sticky=W + N, padx=4, pady=4)
        self.pause_button.bind('<Button-1>', self.callback_pause)
        # pause_button.grid_columnconfigure(0, weight=2)

        self.next_button = Button(self.button_wrapper, image=self.next_icon, height=25, width=25)
        self.next_button.grid(column=2, row=0, sticky=W + N, padx=4, pady=4)
        self.next_button.bind('<Button-1>', self.callback_step)
        # next_button.grid_columnconfigure(0, weight=2)


root = Tk()
root.geometry('1024x800')
root.title('Game of life')
root.resizable(0, 0)
my_gui = MainWindow(root)
root.mainloop()
