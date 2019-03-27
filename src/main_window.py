import time
import tkinter as tk

from .evolution_step import EvolutionStep
from .evolution_step_view import EvolutionStepView


class MainWindow(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self._master = master
        self.init_window()

    def init_window(self):
        self._master.title('blender-evolution')

        self.grid(row=0, column=0, sticky='NSEW')
        self._master.grid_rowconfigure(0, weight=1)
        self._master.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.init_menus()
        self.init_grid()

    def init_menus(self):
        menubar = tk.Menu(self._master)
        self._master.config(menu=menubar)

        file_menu = tk.Menu(menubar)
        file_menu.add_command(label='Exit', command=self.client_exit)

        menubar.add_cascade(label='File', menu=file_menu)

    def init_grid(self):
        self.update()

        width = self.winfo_width()
        height = self.winfo_height()

        container = tk.Frame(self, width=width, height=height)
        container.grid(row=0, column=0)

        print('W={} H={}'.format(width, height))

        width_third = int(width / 3)
        height_third = int(height / 3)

        # grid.grid(row=0, column=0, sticky="nsew")  # spell-checker: ignore nsew

        # for row in range(0, 3):
        #     grid.grid_rowconfigure(row, weight=1)
        # for col in range(0, 3):
        #     grid.grid_columnconfigure(col, weight=1)

        _center_esv = EvolutionStepView(container, width_third, height_third)
        _center_esv.place(x=width_third, y=height_third,
                          width=width_third, height=height_third)
        _center_esv.set_evolution_step(EvolutionStep())

        _outer_esvs = []

        for row in range(0, 3):
            for col in range(0, 3):
                if row == 1 and col == 1:
                    # Center of grid is special and has already been done.
                    continue
                esv = EvolutionStepView(container, width_third, height_third)
                esv.place(x=row * width_third, y=col * height_third,
                          width=width_third, height=height_third)
                _outer_esvs.append(esv)

        self.update()

    def client_exit(self):
        exit()
