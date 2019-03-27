import tkinter as tk

from .evolution_step import EvolutionStepState
from .tkinter_png.tkinter_png import PngImageTk


class EvolutionStepView(tk.Frame):

    def __init__(self, parent, width, height):
        tk.Frame.__init__(self, parent, width=width, height=height, bg='red')

        self._parent = parent
        self._width = width
        self._height = height

        self._evolution_step = None
        self._last_state = None

        self._show_state()

    def set_evolution_step(self, evolution_step):
        if self._evolution_step:
            self._evolution_step.destroy()

        self._evolution_step = evolution_step

        self._show_state()

        if self._evolution_step:
            self.update()
            width = self.winfo_width()
            height = self.winfo_height()
            self._evolution_step.set_render_size(width, height)
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
        canvas = tk.Canvas(self)
        canvas.place(x=0, y=0, width=self._width, height=self._height)
        canvas.create_image(0, 0, anchor=tk.NW, image=img.image)
        # Need to keep a reference to the image:
        # http://effbot.org/tkinterbook/photoimage.htm
        canvas.image = img.image

    def _show_label(self, text):
        self._remove_all()
        canvas = tk.Canvas(self)
        canvas.place(x=0, y=0, width=self._width, height=self._height)
        canvas.create_text(self._width / 2, self._height / 2, fill="darkblue",
                           font="Times 20 italic bold", text=text)

    def _timer_tick(self):
        self._show_state()

        if self._evolution_step and self._evolution_step.state != EvolutionStepState.done:
            self._parent.after(1000, self._timer_tick)
