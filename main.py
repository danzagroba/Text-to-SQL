import tkinter as tk
from tkinter import Radiobutton, IntVar, W, Label

root = tk.Tk(screenName = None, baseName=None, className='Text-to-SQL', useTk=1)

w = Label(root, text='Selecione o banco de dados:')
w.pack()

v = IntVar()
Radiobutton(root, text='MySQL', variable=v, value=1).pack(side=tk.LEFT, padx=5)
Radiobutton(root, text='PostgreSQL', variable=v, value=2).pack(side=tk.LEFT, padx=5) 


root.mainloop()