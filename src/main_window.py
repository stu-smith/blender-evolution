import time
import tkinter as tk

from .evolution_step import EvolutionStep
from .evolution_step_view import EvolutionStepView

# spellchecker:ignore tkinter,winfo,NSEW


class MainWindow(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self._master = master
        self.init_window()
        self._last_width = None
        self._last_height = None
        self.after(200, self._resize_timer_tick)

    def init_window(self):
        self._master.title('blender-evolution')

        self.grid(row=0, column=0, sticky=tk.NSEW)
        self._master.grid_rowconfigure(0, weight=1)
        self._master.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._init_menus()
        self._init_grid()

    def _init_menus(self):
        menubar = tk.Menu(self._master)
        self._master.config(menu=menubar)

        file_menu = tk.Menu(menubar)
        file_menu.add_command(label='Exit', command=self._client_exit)

        menubar.add_cascade(label='File', menu=file_menu)

    def _init_grid(self):
        self.update()

        width = self.winfo_width()
        height = self.winfo_height()

        container = tk.Frame(self, width=width, height=height)
        container.grid(row=0, column=0)

        width_third = int(width / 3)
        height_third = int(height / 3)

        self._center_view = EvolutionStepView(
            container, width_third, height_third
        )
        self._center_view.set_evolution_step(EvolutionStep())

        self._outer_views = []

        for row in range(0, 3):
            for col in range(0, 3):
                if row == 1 and col == 1:
                    # Center of grid is special and has already been done.
                    continue
                view = EvolutionStepView(container, width_third, height_third)
                self._outer_views.append(view)

        self._place_views()

    def _client_exit(self):
        exit()

    def _place_views(self):
        #
        # I just couldn't get the tkinter grid to do what I wanted.
        # That's a competency issue on my side, not anything wrong with tkinter.
        # So, I've fudged it with a manual layout system.
        #
        width = self.winfo_width()
        height = self.winfo_height()

        width_third = int(width / 3)
        height_third = int(height / 3)

        self._center_view.place(
            x=width_third, y=height_third,
            width=width_third, height=height_third
        )
        self._center_view.set_size(width_third, height_third)

        index = 0

        for row in range(0, 3):
            for col in range(0, 3):
                if row == 1 and col == 1:
                    # Center of grid is special and has already been done.
                    continue

                view = self._outer_views[index]

                view.place(
                    x=row * width_third, y=col * height_third,
                    width=width_third, height=height_third
                )
                view.set_size(width_third, height_third)

                index = index + 1

    def _resize_timer_tick(self):
        width = self.winfo_width()
        height = self.winfo_height()

        if self._last_width != width or self._last_height != height:
            self._last_width = width
            self._last_height = height
            self._place_views()

        self.after(200, self._resize_timer_tick)
