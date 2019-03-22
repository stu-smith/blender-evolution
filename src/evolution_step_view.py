from tkinter import Canvas, Frame, Label, PhotoImage, NW

from .evolution_step import EvolutionStepState
from .tkinter_png.tkinter_png import *


class EvolutionStepView(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self._parent = parent

        self.grid(row=0, column=0, sticky="nsew")  # spell-checker: ignore nsew
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._evolution_step = None
        self._last_state = None

        self._show_state()

    def set_evolution_step(self, evolution_step):
        if self._evolution_step:
            self._evolution_step.destroy()

        self._evolution_step = evolution_step

        self._show_state()

        if self._evolution_step:
            self._timer_tick()

    def _remove_all(self):
        all_widgets = list(self.children.values())

        for widget in all_widgets:
            widget.destroy()

    def _show_state(self):
        if self._evolution_step:

            if self._evolution_step.state != self._last_state:

                new_state = self._evolution_step.state

                if new_state == EvolutionStepState.not_started:
                    self._show_label('Not started')

                elif new_state == EvolutionStepState.mutating:
                    self._show_label('Mutating')

                elif new_state == EvolutionStepState.rendering:
                    self._show_label('Rendering')

                if new_state == EvolutionStepState.done:
                    self._show_image(self._evolution_step.output_image_path)

                self._last_state = new_state

            else:
                # Same state as before, no action.
                pass

        else:
            self._show_label('NONE')
            self._last_state = None

    def _show_image(self, image_path):
        self._remove_all()
        img = PngImageTk(self._evolution_step.output_image_path)
        img.convert()
        canvas = Canvas(self, width=200, height=200)
        canvas.grid(row=0, column=0)
        canvas.create_image(0, 0, anchor=NW, image=img.image)
        # Need to keep a reference to the image:
        # http://effbot.org/tkinterbook/photoimage.htm
        canvas.image = img.image

    def _show_label(self, text):
        self._remove_all()
        label = Label(self, text=text)
        label.grid(row=0, column=0)
        label.configure(background='green')

    def _timer_tick(self):
        self._show_state()

        if self._evolution_step and self._evolution_step.state != EvolutionStepState.done:
            self._parent.after(1000, self._timer_tick)
