from tkinter import Tk, TclError

from .main_window import MainWindow


def main():
    root = Tk()
    root.geometry('800x800')
    root.option_add('*tearOff', False)
    app = MainWindow(master=root)

    app.mainloop()

    try:
        root.destroy()
    except TclError:
        pass


if __name__ == '__main__':
    main()
