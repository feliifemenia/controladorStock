from tkinter import *

root = Tk()

def dar_alta_producto():
    label_nombre = Label(root, text="Nombre")
    label_codigo = Label(root, text="Código")
    label_descripcion = Label(root, text="Descripción")

    entry_nombre = Entry(root, width=100)
    entry_cantidad = Entry(root)
    entry_codigo = Entry(root)

    label_nombre.grid(row=0, column=0)
    entry_nombre.grid(row=0, column=1)
    label_codigo.grid(row=1, column=0)
    entry_codigo.grid(row=1, column=1)
    label_descripcion.grid(row=2, column=0)
    entry_cantidad.grid(row=2, column=1)

myLabel2 = Label(root, text = "Es god no?")

myButton = Button(root, text="Cargar nuevo producto", command=dar_alta_producto)
# myButton.pack()
myButton.grid(row=2, column=1)

root.mainloop()