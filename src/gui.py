import tkinter as tk
from .main import minesweeper

mode = 0

def run():
	master = tk.Tk()
	master.minsize(400, 300)
	master.configure(background='white')

	def easy_mode():
		# minesweeper(50)
		global mode
		mode = 50
		master.destroy()

	def medium_mode():
		# minesweeper(40)
		global mode
		mode = 40
		master.destroy()

	def hard_mode():
		# minesweeper(20)
		global mode
		mode = 20
		master.destroy()

	title = tk.Label(master, text='Minesweeper', font=('Fixedsys', 30), fg='#666666', bg='#ffffff', anchor=tk.N)
	btn_easy = tk.Button(master, text='Easy', font=('Fixedsys', 19), fg='#707070', anchor=tk.N, command=easy_mode)
	btn_medium = tk.Button(master, text='Medium', font=('Fixedsys', 19), fg='#707070', anchor=tk.N, command=medium_mode)
	btn_hard = tk.Button(master, text='Hard', font=('Fixedsys', 19), fg='#707070', anchor=tk.N, command=hard_mode)

	title.pack()
	btn_easy.pack(pady=10)
	btn_medium.pack(pady=10)
	btn_hard.pack(pady=10)

	master.mainloop()
	minesweeper(mode)

