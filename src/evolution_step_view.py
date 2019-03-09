from tkinter import Frame, Label


class EvolutionStepView(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._evolution_step = None

        self._label = Label(self, text='ABC')
        self._label.grid(row=0, column=0)
        self._label.configure(background='green')
