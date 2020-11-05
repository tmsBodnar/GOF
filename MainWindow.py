import tkinter as tk
from copy import copy, deepcopy
from tkinter import *
import sys
from tkinter import filedialog, messagebox
from rleloader import RleLoader
from pathlib import Path
from baby import Baby
import os
from canvas.PatternCanvas import PatternCanvas
from canvas.SimCanvas import SimCanvas
from simulator import Simulator


class MainWindow:

    # exit app
    def exit_callback(self):
        self.stop_simulation()
        sys.exit()

    # opens file dialog, and starts simulation with chosen file
    def open_file_dialog(self):
        self.is_simulated = False
        file = filedialog.askopenfile(mode='r')
        if file is not None:
            for widget in self.pattern_wrapper.winfo_children():
                widget.destroy()
            self.load_pattern(file, 0)
        self.sim_canvas.delete(ALL)

        self.create_and_draw_sim_canvas()

    # open folder to load all files from
    def open_folder_dialog(self):
        path = filedialog.askdirectory()
        self.is_simulated = False
        with os.scandir(path) as files:
            for i, file in enumerate(files, start=0):
                pattern = open(path + '/' + file.name)
                self.load_pattern(pattern, i)
                pattern.close()

    def pattern_clicked(self, event):
        self.sim_canvas.delete(ALL)
        self.sim_canvas.set_baby(None)
        self.create_and_draw_sim_canvas()
        self.is_simulated = False

    def simulation_start(self):
        Simulator.start_simulation(self.sim_canvas)

    def simulation(self):
        if len(self.sim_canvas.baby.cells) > 0:
            if self.is_simulated:
                Simulator.start_simulation(self.sim_canvas, self.size_mod)
                self.timer_id = self.master.after(self.timeout, self.simulation)
            else:
                self.stop_simulation()
        else:
            self.play_button['image'] = self.play_icon
            self.set_buttons(tk.DISABLED)
            self.is_play = False

    def stop_simulation(self):
        self.master.after_cancel(self.timer_id)

    def create_and_draw_sim_canvas(self):
        baby = deepcopy(self.loaded_baby)
        self.sim_canvas.set_baby(baby)
        self.sim_canvas.fill_sim_canvas_to_live(self.size_mod)
        self.play_button['image'] = self.play_icon
        self.is_play = False
        self.set_buttons(tk.NORMAL)

    # load patterns to canvas
    def load_pattern(self, file, row):
        extension = Path(file.name).suffix
        if extension.upper() != ".RLE":
            messagebox.showinfo("Wrong file type", "Please, load .rle files")
        else:
            self.loaded_baby = RleLoader.load_pattern(file)
            self.loaded_baby.name = (file.name.split("/")[-1]).split('.')[0]
            self.create_and_fill_pattern_canvas(row)

    # create patterns canvas to show patterns visually
    def create_and_fill_pattern_canvas(self, row):
        for widget in self.sim_canvas.winfo_children():
            widget.destroy()
        pattern_canvas = PatternCanvas(self.pattern_wrapper, self.pattern_canvas_options)
        pattern_canvas.grid(column=0, row=row, sticky=N + W)
        pattern_canvas.set_baby(self.loaded_baby)
        pattern_canvas.fill_pattern_canvas_with_baby_cells()
        self.pattern_wrapper.create_window(100, 108 * (1 + row) + row * 108, window=pattern_canvas)
        pattern_canvas.bind("<Button-1>", self.pattern_clicked)
        self.pattern_wrapper.configure(scrollregion=self.pattern_wrapper.bbox(ALL))

    def callback_zoom_plus(self):
        if self.is_simulated:
            self.is_simulated = False
            if self.size_mod < 1.4:
                self.size_mod += 0.01
            self.is_simulated = True
        else:
            if self.size_mod < 1.4:
                self.size_mod += 0.01
            self.sim_canvas.fill_sim_canvas_to_live(self.size_mod)

    def callback_zoom_minus(self):
        if self.is_simulated:
            self.is_simulated = False
            if self.size_mod > 0.93:
                self.size_mod += -0.01
            self.is_simulated = True
        else:
            if self.size_mod > 0.93:
                self.size_mod += -0.01
            self.sim_canvas.fill_sim_canvas_to_live(self.size_mod)

    def callback_speed_plus(self):
        self.timeout = int(self.timeout * 0.8)

    def callback_speed_minus(self):
        self.timeout = int(self.timeout * 1.2)

    def callback_step(self):
        self.is_simulated = True
        self.simulation()
        self.master.after_cancel(self.timer_id)

    def callback_play(self):
        print("play")
        if len(self.sim_canvas.baby.cells) > 0:
            self.is_play = not self.is_play
            if self.is_play:
                self.play_button['image'] = self.pause_icon
                self.is_simulated = True
                self.simulation()
                self.next_button['state'] = tk.DISABLED
                self.delete_button['state'] = tk.DISABLED
            else:
                self.next_button['state'] = tk.NORMAL
                self.play_button['image'] = self.play_icon
                self.delete_button['state'] = tk.NORMAL
                self.is_simulated = False
                self.master.after_cancel(self.timer_id)
                self.simulation()
        else:
            messagebox.showinfo("Choose a pattern!", "Please, click on a pattern")

    def callback_delete(self):
        self.is_simulated = False
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
        self.sim_canvas.clear_canvas()
        self.play_button['image'] = self.play_icon
        self.set_buttons(tk.DISABLED)
        self.size_mod = 1
        self.timeout = 100

    def set_buttons(self, arg):
        self.play_button['state'] = arg
        self.next_button['state'] = arg
        self.delete_button['state'] = arg
        self.speed_minus['state'] = arg
        self.speed_plus['state'] = arg
        self.zoom_minus['state'] = arg
        self.zoom_plus['state'] = arg

    def action(self):
        self.output.insert(Tk.END, self.variable.get())

    def __init__(self, master):
        self.pattern_wrapper_options = {
            'width': '220',
            'height': '700',
            'bg': 'White',
            'bd': '5'
        }
        self.pattern_canvas_options = {
            'width': '200',
            'height': '200',
            'bg': 'White',
            'bd': '5'
        }
        self.sim_canvas_options = {
            'width': '800',
            'bg': 'White',
            'height': '725',
            'bd': '5'
        }
        self.patterns = []
        self.is_simulated = False
        self.is_play = False
        self.timeout = 100
        self.loaded_baby = Baby.Baby()
        self.size_mod = 1

        self.timer_id = 0
        self.master = master

        self.pattern_wrapper = Canvas(master, self.pattern_wrapper_options, scrollregion=(0, 0, 1000, 1000))
        self.pattern_wrapper.grid(column=0, row=0, rowspan=2, sticky=W + S + N + E, padx=(2, 0), pady=(2, 2))
        self.vbar = Scrollbar(master, orient=VERTICAL)
        self.vbar.grid(column=1, row=0, rowspan=1, sticky=W + S + N)
        self.vbar.config(command=self.pattern_wrapper.yview)
        self.pattern_wrapper.configure(yscrollcommand=self.vbar.set)
        self.pattern_wrapper.config(scrollregion=self.pattern_wrapper.bbox(ALL))

        self.sim_canvas = SimCanvas(master, self.sim_canvas_options)
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

        self.zoom_wrapper = Frame(master)
        self.zoom_wrapper.config(bd=1, relief=tk.GROOVE)
        self.zoom_wrapper.grid(column=2, row=1, sticky=W + S, padx=4, pady=6)
        self.zoom_wrapper.grid_columnconfigure(2, weight=1)

        self.plus_icon = PhotoImage(file="src/plus.png")
        self.minus_icon = PhotoImage(file="src/minus.png")

        self.zoom_plus = Button(self.zoom_wrapper, image=self.plus_icon,
                                height=25, width=25, state=tk.DISABLED, command=self.callback_zoom_plus)
        self.zoom_plus.grid(column=2, row=1, sticky=W + S)

        self.zoom_text = Label(self.zoom_wrapper, text='Zoom')
        self.zoom_text.grid(column=1, row=1, sticky=W + S, padx=4, pady=4)

        self.zoom_minus = Button(self.zoom_wrapper, image=self.minus_icon,
                                 height=25, width=25, state=tk.DISABLED, command=self.callback_zoom_minus)
        self.zoom_minus.grid(column=0, row=1, sticky=W + S)

        self.speed_wrapper = Frame(master)
        self.speed_wrapper.config(bd=1, relief=tk.GROOVE)
        self.speed_wrapper.grid(column=3, row=1, sticky=W + S, padx=4, pady=6)
        self.speed_wrapper.grid_columnconfigure(2, weight=1)

        self.speed_plus = Button(self.speed_wrapper, image=self.plus_icon,
                                 height=25, width=25, state=tk.DISABLED, command=self.callback_speed_plus)
        self.speed_plus.grid(column=2, row=1, sticky=W + S)

        self.speed_text = Label(self.speed_wrapper, text='Speed')
        self.speed_text.grid(column=1, row=1, sticky=W + S, padx=4, pady=4)

        self.speed_minus = Button(self.speed_wrapper, image=self.minus_icon,
                                  height=25, width=25, state=tk.DISABLED, command=self.callback_speed_minus)
        self.speed_minus.grid(column=0, row=1, sticky=W + S)

        self.play_icon = PhotoImage(file="src/play.png")
        self.pause_icon = PhotoImage(file="src/pause.png")
        self.next_icon = PhotoImage(file="src/next.png")
        self.stop_icon = PhotoImage(file="src/stop.png")

        self.button_wrapper = Frame(master)
        self.button_wrapper.config(bd=1, relief=tk.GROOVE)
        self.button_wrapper.grid(column=4, row=1, sticky=W + S, padx=6, pady=3, )
        self.button_wrapper.grid_columnconfigure(4, weight=1)

        self.play_button = Button(self.button_wrapper, image=self.play_icon,
                                  height=25, width=25, state=tk.DISABLED, command=self.callback_play)
        self.play_button.grid(column=0, row=0, sticky=W + N, padx=4, pady=4)

        self.next_button = Button(self.button_wrapper, image=self.next_icon,
                                  height=25, width=25, state=tk.DISABLED, command=self.callback_step)
        self.next_button.grid(column=1, row=0, sticky=W + N, padx=4, pady=4)

        self.delete_button = Button(self.button_wrapper, image=self.stop_icon,
                                    height=25, width=25, state=tk.DISABLED, command=self.callback_delete)
        self.delete_button.grid(column=2, row=0, sticky=E + N, padx=4, pady=4)


root = Tk()
root.geometry('1024x800')
root.title('Game of life')
root.resizable(0, 0)
my_gui = MainWindow(root)
root.mainloop()
