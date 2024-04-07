import tkinter as tk
from tkinter import ttk

def seleccionar_opcion():
    seleccion = opcion_var.get()
    print("Opción seleccionada:", seleccion)

# Crear la ventana principal
root = tk.Tk()
root.title("Frame con Botón y Radio Button")

# Crear el frame principal
frame = ttk.Frame(root, padding="20")
frame.pack()

# Crear el botón a la izquierda
boton = ttk.Button(frame, text="Botón")
boton.grid(row=0, column=0, padx=10, pady=10)

# Crear el radio button con dos opciones a la derecha
opcion_var = tk.StringVar()
radio1 = ttk.Radiobutton(frame, text="Opción 1", variable=opcion_var, value="opcion1", command=seleccionar_opcion)
radio1.grid(row=0, column=1, padx=10, pady=10, sticky="w")
radio2 = ttk.Radiobutton(frame, text="Opción 2", variable=opcion_var, value="opcion2", command=seleccionar_opcion)
radio2.grid(row=1, column=1, padx=10, pady=10, sticky="w")

root.mainloop()
