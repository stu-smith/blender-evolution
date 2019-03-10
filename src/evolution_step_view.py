from tkinter import Frame, Label

from .evolution_step import EvolutionStepState


class EvolutionStepView(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self._parent = parent

        self.grid(row=0, column=0, sticky="nsew")  # spell-checker: ignore nsew
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._evolution_step = None

        self._label = Label(self, text='ABC')
        self._label.grid(row=0, column=0)
        self._label.configure(background='green')

        self._show_state()

    def set_evolution_step(self, evolution_step):
        if self._evolution_step:
            self._evolution_step.destroy()

        self._evolution_step = evolution_step

        self._show_state()

        if self._evolution_step:
            self._timer_tick()

    def _show_state(self):
        if self._evolution_step:
            self._label.configure(text=str(self._evolution_step.state))
        else:
            self._label.configure(text='NONE')

    def _timer_tick(self):
        self._show_state()

        if self._evolution_step and self._evolution_step.state != EvolutionStepState.done:
            self._parent.after(1000, self._timer_tick)
