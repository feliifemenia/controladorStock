from tkinter import *
from tkinter import ttk
import pymysql
from tkinter import messagebox
from ttkbootstrap import Style
from ttkbootstrap.widgets import Button

root = Tk()
style = Style(theme='superhero')

def conectar_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Felipe46636141*",
        database="stock"
    )

def guardar_producto(nombre, codigo, descripcion):
    conexion = conectar_db()
    cursor = conexion.cursor()

    sql = "INSERT INTO infoProductos (nombre, codigo, descripcion) VALUES (%s, %s, %s)"
    val = (nombre, codigo, descripcion)
    cursor.execute(sql, val)
    conexion.commit()

    cursor.close()
    conexion.close()
    
    messagebox.showinfo("Información", "Producto guardado exitosamente")

def cargar_nuevo_producto():
    window_cargar_producto = Toplevel(root)
    window_cargar_producto.title("Cargar Nuevo Producto")
    window_cargar_producto.geometry("500x250")

    # Frame para contener el formulario
    frame_formulario = ttk.Frame(window_cargar_producto, padding=(20, 10, 20, 10))
    frame_formulario.grid(row=0, column=0, sticky="ew")
    
    # Widgets de entrada
    label_nombre = ttk.Label(frame_formulario, text="Nombre:")
    label_codigo = ttk.Label(frame_formulario, text="Código:")
    label_descripcion = ttk.Label(frame_formulario, text="Descripción:")

    entry_nombre = ttk.Entry(frame_formulario, width=50)
    entry_codigo = ttk.Entry(frame_formulario, width=50)
    entry_descripcion = ttk.Entry(frame_formulario, width=50)

    def guardar_datos():
        nombre = entry_nombre.get()
        codigo = entry_codigo.get()
        descripcion = entry_descripcion.get()
        guardar_producto(nombre, codigo, descripcion)

    # Botón de guardar
    button_guardar = Button(frame_formulario, text="Guardar", command=guardar_datos)

    # Posicionamiento de los widgets con padding
    label_nombre.grid(row=0, column=0, pady=5, sticky="w")
    entry_nombre.grid(row=0, column=1, pady=5, sticky="ew")
    label_codigo.grid(row=1, column=0, pady=5, sticky="w")
    entry_codigo.grid(row=1, column=1, pady=5, sticky="ew")
    label_descripcion.grid(row=2, column=0, pady=5, sticky="w")
    entry_descripcion.grid(row=2, column=1, pady=5, sticky="ew")
    button_guardar.grid(row=3, column=1, pady=10)

    # Expansión automática
    frame_formulario.columnconfigure(1, weight=1)

def eliminar_producto_db(codigo):
    conexion = conectar_db()
    cursor = conexion.cursor()

    sql = "DELETE FROM infoProductos WHERE codigo = %s"
    val = (codigo,)

    cursor.execute(sql, val)
    conexion.commit()

    cursor.close()
    conexion.close()
    
    messagebox.showinfo("Información", "Producto eliminado exitosamente")

def eliminar_producto():

    window_eliminar_producto = Toplevel(root)
    window_eliminar_producto.title("Eliminar un Producto")
    window_eliminar_producto.geometry("600x150")

    # Frame para contener el formulario
    frame_formulario = ttk.Frame(window_eliminar_producto, padding=(20, 10, 20, 10))
    frame_formulario.grid(row=0, column=0, sticky="ew")
    
    # Widgets de entrada
    label_codigo = ttk.Label(frame_formulario, text="Ingrese el Código del Producto a eliminar:")
    entry_codigo = ttk.Entry(frame_formulario, width=30)

    def borrar_datos():
        codigo = entry_codigo.get()
        if codigo:
            eliminar_producto_db(codigo)
        else:
            messagebox.showerror("Error", "Debe ingresar un código para eliminar")

    # Botón de borrar
    button_borrar = Button(frame_formulario, text="Borrar", command=borrar_datos, bootstyle="danger")

    # Posicionamiento de los widgets con padding
    label_codigo.grid(row=0, column=0, pady=10, sticky="w")
    entry_codigo.grid(row=0, column=1, pady=10, sticky="ew")
    button_borrar.grid(row=1, column=1, pady=10, sticky="e")

    # Expansión automática
    frame_formulario.columnconfigure(1, weight=1)

def consultar_db(codigo):
    conexion = conectar_db()
    cursor = conexion.cursor()

    sql = "SELECT cantidad FROM infoProductos WHERE codigo = %s"
    val = (codigo,)

    cursor.execute(sql, val)
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()
    
    return resultado[0]

def consultar_stock():
    
    window_consultar_producto = Toplevel(root)
    window_consultar_producto.title("Consultar Stock")
    window_consultar_producto.geometry("600x150")

    # Frame para contener el formulario
    frame_formulario = ttk.Frame(window_consultar_producto, padding=(20, 10, 20, 10))
    frame_formulario.grid(row=0, column=0, sticky="ew")

    # Widgets de entrada
    label_codigo = ttk.Label(frame_formulario, text="Ingrese el código del Producto a consultar:")
    entry_codigo = ttk.Entry(frame_formulario, width=30)

    def realizar_consulta():
        codigo = entry_codigo.get()
        cantidad_producto = consultar_db(codigo)
        if cantidad_producto is not None:
            messagebox.showinfo("Información", f"La cantidad del producto con código {codigo} es: {cantidad_producto}")
        else:
            messagebox.showwarning("Advertencia", "No se encontró ningún producto con ese código")

    # Botón de consultar
    button_consultar = Button(frame_formulario, text="Consultar", command=realizar_consulta, bootstyle="primary")

    # Posicionamiento de los widgets con padding
    label_codigo.grid(row=0, column=0, pady=10, sticky="w")
    entry_codigo.grid(row=0, column=1, pady=10, sticky="ew")
    button_consultar.grid(row=1, column=1, pady=10, sticky="e")

    # Expansión automática
    frame_formulario.columnconfigure(1, weight=1)

def agregar_db(codigo, cantidad):
    conexion = conectar_db()
    cursor = conexion.cursor()

    sql_select = "SELECT cantidad FROM infoProductos WHERE codigo = %s"
    val = (codigo,)
    cursor.execute(sql_select, val)
    resultado = cursor.fetchone()

    if resultado:
        cantidad_actual = resultado[0]
        nueva_cantidad = cantidad_actual + cantidad

        # Actualizar la cantidad del producto en la base de datos
        sql_update = "UPDATE infoProductos SET cantidad = %s WHERE codigo = %s"
        val_update = (nueva_cantidad, codigo)
        cursor.execute(sql_update, val_update)
        conexion.commit()

        messagebox.showinfo("Información", f"Cantidad actualizada: {nueva_cantidad}")
    else:
        messagebox.showwarning("Advertencia", "No se encontró ningún producto con ese código")

    cursor.close()
    conexion.close()
    

def modificar_stock():
    window_modificar_stock=Toplevel(root)
    window_modificar_stock.title("Modificar Stock")

    label_codigo = Label(window_modificar_stock, text="Ingrese el codigo de Producto")
    entry_codigo = Entry(window_modificar_stock, width=100)

    label_cantidad = Label(window_modificar_stock, text="Ingrese la Cantidad a Agregar")
    entry_cantidad =  Entry(window_modificar_stock, width=100)

    def agregar_cantidad():
        codigo = entry_codigo.get()
        cantidad = int(entry_cantidad.get())

        if cantidad < 0:
            cantidad = 0
            messagebox.showwarning("Advertencia", "Ingrese una cantidad mayor a 0")
            return

        agregar_db(codigo, cantidad)

    button_agregar = Button(window_modificar_stock, text="Agregar Unidades", command=agregar_cantidad)

    label_codigo.grid(row=0, column=0)
    entry_codigo.grid(row=0, column=1)
    label_cantidad.grid(row=1, column=0)
    entry_cantidad.grid(row=1, column=1)
    button_agregar.grid(row=3, column=1)



def actualizar_stock_productos(lista_productos):
    conexion = conectar_db()
    cursor = conexion.cursor()

    for codigo, cantidad in lista_productos:
        print(f"Procesando producto: {codigo} con cantidad: {cantidad}")
        sql_select = "SELECT cantidad FROM infoProductos WHERE codigo = %s"
        val = (codigo,)
        cursor.execute(sql_select, val)
        resultado = cursor.fetchone()

        if resultado:
            cantidad_actual = resultado[0]
            nueva_cantidad = cantidad_actual - cantidad

            # Actualizar la cantidad del producto en la base de datos
            sql_update = "UPDATE infoProductos SET cantidad = %s WHERE codigo = %s"
            val_update = (nueva_cantidad, codigo)
            cursor.execute(sql_update, val_update)
            conexion.commit()
        else:
            messagebox.showwarning("Advertencia", f"No se encontró ningún producto con el código: {codigo}")

    cursor.close()
    conexion.close()

def ventana_modificar_stock_multiple():
    window_modificar_stock = Toplevel(root)
    window_modificar_stock.title("Modificar Stock Múltiple")
    window_modificar_stock.geometry("500x300")

    # Frame para contener el formulario
    frame_formulario = ttk.Frame(window_modificar_stock, padding=(20, 10, 20, 10))
    frame_formulario.grid(row=0, column=0, sticky="ew")

    # Widgets de entrada
    label_codigo = ttk.Label(frame_formulario, text="Ingrese el código de Producto:")
    entry_codigo = ttk.Entry(frame_formulario, width=30)

    label_cantidad = ttk.Label(frame_formulario, text="Ingrese la Cantidad a dar de Baja:")
    entry_cantidad = ttk.Entry(frame_formulario, width=30)
    entry_cantidad.insert(0, '1')

    productos = []

    def agregar_producto():
        codigo = entry_codigo.get()
        try:
            cantidad = int(entry_cantidad.get())
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Advertencia", "Ingrese una cantidad mayor a 0")
            return

        productos.append((codigo, cantidad))
        entry_codigo.delete(0, END)
        entry_cantidad.delete(0, END)

    def finalizar():
        if productos:
            actualizar_stock_productos(productos)
            messagebox.showinfo("Información", "Stock actualizado para los productos ingresados")
        else:
            messagebox.showinfo("Información", "No se ingresaron productos para actualizar")
        window_modificar_stock.destroy()

    # Botones
    button_agregar = Button(frame_formulario, text="Agregar Producto", command=agregar_producto, bootstyle="primary")
    button_finalizar = Button(frame_formulario, text="Finalizar", command=finalizar, bootstyle="success")

    # Posicionamiento de los widgets con padding
    label_codigo.grid(row=0, column=0, pady=10, sticky="w")
    entry_codigo.grid(row=0, column=1, pady=10, sticky="ew")
    label_cantidad.grid(row=1, column=0, pady=10, sticky="w")
    entry_cantidad.grid(row=1, column=1, pady=10, sticky="ew")
    button_agregar.grid(row=2, column=1, pady=10, sticky="e")
    button_finalizar.grid(row=3, column=1, pady=10, sticky="e")

    # Expansión automática
    frame_formulario.columnconfigure(1, weight=1)

root.title("Manejador de Stock")
#root.attributes('-fullscreen', True)
root.state('zoomed')
# Crear un marco para los botones
frame = Frame(root)
frame.pack(expand=True, fill='both', padx=20, pady=20)

button_cargar_producto = Button(frame, text="Cargar nuevo producto", command=cargar_nuevo_producto)
button_eliminar_producto = Button(frame, text="Eliminar producto", command=eliminar_producto)
button_consultar_stock = Button(frame, text="Consultar Stock de Producto", command=consultar_stock)
button_cambiar_cantidades = Button(frame, text="Agregar Stock", command=modificar_stock)
button_cargar_pedido = Button(frame, text="Cargar Pedido", command=ventana_modificar_stock_multiple)

# Organiza los botones dentro del marco usando grid
button_cargar_producto.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
button_eliminar_producto.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
button_consultar_stock.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
button_cambiar_cantidades.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)
button_cargar_pedido.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

# Configura las filas y columnas para que se expandan
for i in range(3):
    frame.grid_rowconfigure(i, weight=1)
for i in range(2):
    frame.grid_columnconfigure(i, weight=1)

root.mainloop()