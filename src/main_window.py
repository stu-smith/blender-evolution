from tkinter import *

class MainWindow(Frame):

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self._master = master
		self.init_window()

	def init_window(self):
		self._master.title('blender-evolution')

		self.init_menus()
		self.init_grid()

	def init_menus(self):
		menubar = Menu(self._master)
		self._master.config(menu=menubar)

		file_menu = Menu(menubar)
		file_menu.add_command(label='Exit', command=self.client_exit)

		menubar.add_cascade(label='File', menu=file_menu)

	def init_grid(self):
		Label(self._master, text='First').grid(row=0)

	def client_exit(self):
		exit()
