import tkinter as tk
from tkinter import messagebox
import requests

def dar_alta():
    nombre = entry_nombre.get()
    cantidad = int(entry_cantidad.get())
    codigo_de_barras = entry_codigo.get()
    response = requests.post('http://localhost:5000/productos', json={
        "nombre": nombre,
        "cantidad": cantidad,
        "codigo_de_barras": codigo_de_barras
    })
    if response.status_code == 201:
        messagebox.showinfo("Información", "Producto agregado con éxito")
    else:
        messagebox.showerror("Error", response.json().get("mensaje"))

def dar_baja():
    codigo_de_barras = entry_codigo.get()
    cantidad = int(entry_cantidad.get())
    response = requests.put(f'http://localhost:5000/productos/{codigo_de_barras}', json={
        "cantidad": -cantidad
    })
    if response.status_code == 200:
        messagebox.showinfo("Información", "Producto actualizado con éxito")
    else:
        messagebox.showerror("Error", response.json().get("mensaje"))

root = tk.Tk()
root.title("Control de Inventario")

tk.Label(root, text="Nombre").grid(row=0)
tk.Label(root, text="Cantidad").grid(row=1)
tk.Label(root, text="Código de Barras").grid(row=2)

entry_nombre = tk.Entry(root)
entry_cantidad = tk.Entry(root)
entry_codigo = tk.Entry(root)

entry_nombre.grid(row=0, column=1)
entry_cantidad.grid(row=1, column=1)
entry_codigo.grid(row=2, column=1)

tk.Button(root, text='Dar de Alta', command=dar_alta).grid(row=3, column=0, pady=4)
tk.Button(root, text='Dar de Baja', command=dar_baja).grid(row=3, column=1, pady=4)

root.mainloop()
