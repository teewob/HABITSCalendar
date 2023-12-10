import tkinter as tk
import sqlite3
from main_application import MainApplication

if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(width=800, height=600)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    app = MainApplication(master=root)
    app.grid(sticky='nsew')
    root.mainloop()