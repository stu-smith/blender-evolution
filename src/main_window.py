import time
from tkinter import Frame, Menu, Label

from .evolution_step_view import EvolutionStepView


class MainWindow(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self._master = master
        self.init_window()

    def init_window(self):
        self._master.title('blender-evolution')

        self.grid(row=0, column=0, sticky="nsew")
        self._master.grid_rowconfigure(0, weight=1)
        self._master.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.init_menus()
        self.init_grid()

        self.timer_tick()

    def init_menus(self):
        menubar = Menu(self._master)
        self._master.config(menu=menubar)

        file_menu = Menu(menubar)
        file_menu.add_command(label='Exit', command=self.client_exit)

        menubar.add_cascade(label='File', menu=file_menu)

    def init_grid(self):
        grid = Frame(self)

        grid.grid(row=0, column=0, sticky="nsew")

        for row in range(0, 3):
            grid.grid_rowconfigure(row, weight=1)
        for col in range(0, 3):
            grid.grid_columnconfigure(col, weight=1)

        self._label = Label(grid, text='00')
        self._label.configure(background='red')
        self._label.grid(row=0, column=0)
        Label(grid, text='01').grid(row=0, column=1)
        Label(grid, text='02').grid(row=0, column=2)

        Label(grid, text='10').grid(row=1, column=0)
        Label(grid, text='11').grid(row=1, column=1)
        Label(grid, text='12').grid(row=1, column=2)

        Label(grid, text='20').grid(row=2, column=0)
        Label(grid, text='21').grid(row=2, column=1)
        EvolutionStepView(grid).grid(row=2, column=2)

    def client_exit(self):
        exit()

    def timer_tick(self):
        now = time.strftime("%H:%M:%S")
        self._label.configure(text=now)
        self._master.after(1000, self.timer_tick)
