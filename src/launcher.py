import tkinter as tk

from .main_window import MainWindow


def main():
    root = tk.Tk()
    root.state('zoomed')
    root.geometry('800x600')
    root.option_add('*tearOff', False)
    app = MainWindow(master=root)

    app.mainloop()

    try:
        root.destroy()
    except tk.TclError:
        pass


if __name__ == '__main__':
    main()
