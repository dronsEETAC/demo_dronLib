import tkinter as tk

master = tk.Tk()
var1 = tk.IntVar()
var1.set(1)

tk.Checkbutton(master, text = 'check', variable = var1).pack()

def print_var1():
    print(var1.get())

tk.Button(master, text = "Print Var1", command = print_var1).pack()
tk.Button(master, text = 'Close', command = lambda: master.destroy()).pack()

master.mainloop()