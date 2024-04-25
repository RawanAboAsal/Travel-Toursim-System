import tkinter as tk
from UI import *

master = tk.Tk()
master.title("Travel Management System")
master.geometry("500x350")
master.resizable(False, False)

icon = tk.PhotoImage(file = 'assets/icon.png')
master.iconphoto(False, icon)

ui = UI(master = master)

master.mainloop()