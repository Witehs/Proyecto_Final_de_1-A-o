import sqlite3
from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

def ConfgBoton_estilo(master, texto, comando= None, icono=None, posicion_img= "left"):
    boton= ctk.CTkButton(
        master=master,
        text=texto,
        command=comando,
        image=icono,
        compound=posicion_img,
        corner_radius=10,
        hover=False,
        cursor="hand2",
        font=("Arial", 16, "bold"),
        width=180,
        height=40,
        text_color="white"
    )
    return boton

def contenedor_boton(master):
    contenedor= ctk.CTkFrame(
        master=master,
        corner_radius=10,
        fg_color= "transparent"
    )
    return contenedor

def guardar_datos():
    if entry_nombre.get() == "" or entry_color.get() == "" or entry_categoria.get() == "" or entry_talle.get() == "" or entry_cantidad.get() == "" or entry_precio_costo.get() == "" or entry_precio_venta.get() == "":
        messagebox.showerror(title="Error", message="Por favor complete todos los campos")
        return
    
    if int(entry_precio_venta.get()) < int(entry_precio_costo.get()):
        messagebox.showerror(title="Error", message="El numero de venta no puede ser menor que el costo")
        return
    #isalpha : si es que detecta alguna letra letras, isdigit(): si es que decta un numero, 
    if entry_nombre.get().isdigit() or entry_color.get().isdigit():
        messagebox.showerror(title="Error", message="solo caracteres en las casillas nombre o color")
        return
    elif len(entry_nombre.get())<=3 or len(entry_color.get())<=3:
        messagebox.showinfo("Incorrecto", "no se permite caracteres cortos en nombre o color")
        return

    try:
        float(entry_cantidad.get())
        float(entry_precio_costo.get())
        float(entry_precio_venta.get())
    except ValueError:
        messagebox.showerror(title="Error", message="Ingrese valores numéricos válidos en las casillas de cantidad y precios")
        return

    conexion = sqlite3.connect("tiendaropa")
    cursor = conexion.cursor()
    datos = (entry_nombre.get(), entry_color.get(), entry_categoria.get(), entry_talle.get(), entry_cantidad.get(), entry_precio_costo.get(), entry_precio_venta.get())
    datos_verificar = (entry_nombre.get(), entry_color.get(), entry_talle.get())

    verificar = "SELECT nombre_ropa, color, talle FROM ropa WHERE nombre_ropa = ? AND color = ? AND talle = ?"
    cursor.execute(verificar, datos_verificar)
    resultados= cursor.fetchone()
    if resultados:
        messagebox.showerror(title="Error", message="El producto ya existe")
    else:
        cursor.execute("INSERT INTO ropa (nombre_ropa, color, categoria, talle, cantidad, preciocosto, precioventa) VALUES(?, ?, ?, ?, ?, ?, ?)", datos)
        messagebox.showinfo(title="Info", message="Datos guardados")    
    
    conexion.commit()
    cursor.close()
    conexion.close()
    
    entry_nombre.delete(0, tk.END)
    entry_color.delete(0, tk.END)
    entry_categoria.set("")
    entry_talle.set("")
    entry_cantidad.delete(0, tk.END)
    entry_precio_costo.delete(0, tk.END)
    entry_precio_venta.delete(0, tk.END)
    
def buscar_datos():
    dato_buscar = entry_buscar.get().strip().lower()

    if dato_buscar == "":
        messagebox.showerror(title="Error", message="No se coloco nada en la barra de buscar")
        return

    for fila in tabla.get_children():
        tabla.delete(fila)

    try:
        conexion = sqlite3.connect("tiendaropa")
        cursor = conexion.cursor()

        if dato_buscar != "":
            sql = "SELECT * FROM ropa WHERE(codigo_barra) LIKE ? OR LOWER(nombre_ropa) LIKE ?"
            parametro = f"%{dato_buscar}%"

            cursor.execute(sql, (parametro, parametro))
        else:
            cursor.execute("SELECT * FROM ropa")

        resultado = cursor.fetchall()

        for fila in resultado:
            tabla.insert("", tk.END, values=fila)

        conexion.close()

        if len(resultado) == 0 and dato_buscar != "":
            messagebox.showinfo(
                "Sin resultados",
                f"No se encontraron productos con: '{dato_buscar}'",
            )
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al realizar la búsqueda: {e}")

    
def mostrar_datos_tabla(tabla):
    for item in tabla.get_children():
        tabla.delete(item)
    try:
        conexion = sqlite3.connect("tiendaropa")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM ropa")
        datos = cursor.fetchall()
        for fila in datos:
            tabla.insert("", tk.END, values=fila)
        conexion.close()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al mostrar los datos: {e}")
id_seleccionado = None
def modificar():
    global id_seleccionado

    if id_seleccionado is None:
        messagebox.showinfo("Atencion", "No se a selecciono ningun dato")
        return
    

    nuevo_nombre = entry_nombre.get().strip()
    nuevo_color= entry_color.get().strip()
    nuevo_categoria = entry_categoria.get()
    nuevo_talle = entry_talle.get()
    nuevo_cantidad = entry_cantidad.get().strip()
    nuevo_costo = entry_precio_costo.get()
    nuevo_venta = entry_precio_venta.get()

    if entry_nombre.get() == "" or entry_color.get() == "" or entry_categoria.get() == "" or entry_talle.get() == "" or entry_cantidad.get() == "" or entry_precio_costo.get() == "" or entry_precio_venta.get() == "":
            messagebox.showerror(title="Error", message="No se selecciono ningun dato o no se completo todos los campos")
            return
    valor_costo= float(nuevo_costo)
    valor_venta= float(nuevo_venta)
    try:
        if valor_venta <= valor_costo:
            messagebox.showerror(title="Error", message="El numero de venta no puede ser menor que el costo")
            return
    except ValueError:
            messagebox.showerror(title="Error", message="Ingrese valores numéricos válidos en las casillas de cantidad y precios")
            return
    #isalpha : si es que detecta alguna letra letras, isdigit(): si es que decta un numero, 
    if nuevo_nombre.isdigit() or nuevo_color.isdigit():
        messagebox.showerror(title="Error", message="solo valores en texto en las casillas de nombre y color")
        return
    elif len(entry_nombre.get())<=3 or len(entry_color.get())<=3:
            messagebox.showinfo("Incorrecto", "no se permite caracteres cortos en las casillas nombre o color")
            return
    if entry_cantidad.get().isalpha() or entry_precio_costo.get().isalpha() or entry_precio_venta.get().isalpha():
            messagebox.showerror(title="ERROR", message="Solo numeros")
            return
    try:
        conexion= sqlite3.connect("tiendaropa")
        cursor = conexion.cursor()

        sql="UPDATE ropa SET nombre_ropa = ?, color = ?, categoria = ?, talle = ?, cantidad = ?, preciocosto = ?, precioventa = ? WHERE codigo_barra = ?"

        cursor.execute(sql, (nuevo_nombre, nuevo_color, nuevo_categoria, nuevo_talle, nuevo_cantidad, nuevo_costo, nuevo_venta, id_seleccionado,),)

        conexion.commit()
        conexion.close()

        messagebox.showinfo("Exito", "Se actualizo con exito")

        mostrar_datos_tabla(tabla)

        id_seleccionado=None
    except:
        messagebox.showerror(f"Error", f"Error al modificar")
    entry_buscar.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_color.delete(0, tk.END)
    entry_categoria.set("")
    entry_talle.set("")
    entry_cantidad.delete(0, tk.END)
    entry_precio_costo.delete(0, tk.END)
    entry_precio_venta.delete(0, tk.END)
def validacion():
    valor_seleccionado = entry_categoria.get()
    if valor_seleccionado == "Damas" or valor_seleccionado == "Hombres":
        values = ["XS", "S", "M", "L", "XL", "XXL",("XS,S,M,L,XL,XXL")]
    elif valor_seleccionado == "Niños":
        values = [ "4", "6", "8", "10", "12", "14", "16"]
    elif valor_seleccionado == "Bebes":
        values = ["0-3 meses", "3-6 meses", "6-9 meses", "9-12 meses"]
    else:
        values = []
    entry_talle.configure(values=values)

def eliminacion():
    global id_seleccionado

    if entry_nombre.get() == "" or entry_color.get() == "" or entry_categoria.get() == "" or entry_talle.get() == "" or entry_cantidad.get() == "" or entry_precio_costo.get() == "" or entry_precio_venta.get() == "":
            messagebox.showerror(title="Error", message="no hay nigun dato seleccionado")
            return

    if id_seleccionado is None:
        messagebox.showwarning("Atencion", "Porfavor selecciona un producto de la tabla")
        return
    confirmacion = messagebox.askquestion("Confirmar eliminacion", "¿Estas seguro de eliminar este dato permanentemente?")

    if confirmacion == "no":
        messagebox.showinfo("Info", "El dato no fue eliminado")
        return
    try:
        conexion = sqlite3.connect("tiendaropa")
        cursor = conexion.cursor()
        sql = "DELETE FROM ropa WHERE codigo_barra = ?"
        cursor.execute(sql, (id_seleccionado,))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Exito", "El dato fue eliminado correctamente")
        mostrar_datos_tabla(tabla)
        id_seleccionado=None
    except:
        messagebox.showerror("Error", "No se pudo eliminar el dato")
    entry_nombre.delete(0, tk.END)
    entry_color.delete(0, tk.END)
    entry_categoria.set("")
    entry_talle.set("")
    entry_cantidad.delete(0, tk.END)
    entry_precio_costo.delete(0, tk.END)
    entry_precio_venta.delete(0, tk.END)

def registro():
    dato_correo= entry_secion.get()
    dato_contrasena= entry_contra.get()

    if len(dato_correo)<= 3 or len(dato_contrasena)<=3:
        messagebox.showerror("Error", "Los caracteres no pueden ser muy chicos")
        return
    elif len(dato_contrasena)>=9:
        messagebox.showinfo("Info", "solo 8 caracteres")
        return

    try:

        conexion = sqlite3.connect("tiendaropa", timeout=5)
        cursor = conexion.cursor()
        datos= dato_correo, dato_contrasena
        datos_verificar = (dato_correo, dato_contrasena)
        validar =  "SELECT usuario, contrasena FROM datos WHERE usuario = ? AND contrasena = ?"
        cursor.execute(validar, datos_verificar)
        respuesta= cursor.fetchone()
        if respuesta:
            inicio_ventana.destroy()
            return
        else:
            messagebox.showinfo("datos", "no esta registrado")
            conf = messagebox.askquestion("Registrar", "¿Deseas agregar estos datos para ingresar de nuevo?")
            if conf:
                cursor.execute("INSERT INTO datos (usuario, contrasena) VALUES(?, ?)", datos)
                conexion.commit()
                messagebox.showinfo(title="Info", message="Datos guardados")       
    except sqlite3.OperationalError as error:
        messagebox.showerror("Error en la base de datos", f"No se pudo guardar")
    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass

inicio_ventana = tk.Tk()
inicio_ventana.configure(bg="#F3F3F3")
inicio_ventana.geometry("250x400")

secion = ctk.CTkLabel(inicio_ventana, text="Inicio de Secion",font=("Arial", 16, "bold"))
secion.pack(pady=(10,2))
entry_secion = ctk.CTkEntry(inicio_ventana, placeholder_text="Ingrese un Usuario")
entry_secion.pack(pady=(5,2))
contra = ctk.CTkLabel(inicio_ventana, text="Contraseña",font=("Arial", 16, "bold"))
contra.pack(pady=(5,2))
entry_contra = ctk.CTkEntry(inicio_ventana, placeholder_text="Ingrese una Contraseña")
entry_contra.pack(pady=(5,2))

boton=ConfgBoton_estilo (inicio_ventana, texto="Ingresar", comando=lambda:registro(), icono=None, posicion_img="left")
boton.configure(fg_color="#70D146")
boton.pack(pady = 10)


inicio_ventana.mainloop()

ventana = tk.Tk()
ventana.geometry("1180x750")
ventana.configure(bg="#F3F3F3")
ventana.title("Tienda de Ropa")

barra_de_navegacio = ctk.CTkFrame(ventana,
                                  bg_color="#F3F3F3",
                                  fg_color="transparent")
barra_de_navegacio.grid_columnconfigure((0, 1, 2, 3), weight=1)
barra_de_navegacio.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

boton_1_cont = contenedor_boton(barra_de_navegacio)
boton_1_cont.grid(row=0, column=0, padx=10, pady=(2, 4))

boton_2_cont = contenedor_boton(barra_de_navegacio)
boton_2_cont.grid(row=0, column=1, padx=10, pady=(2, 4))

boton_3_cont = contenedor_boton(barra_de_navegacio)
boton_3_cont.grid(row=0, column=2, padx=10, pady=(2, 4))

boton_4_cont = contenedor_boton(barra_de_navegacio)
boton_4_cont.grid(row=0, column=3, padx=10, pady=(2, 4))

boton_Buscar=ConfgBoton_estilo(boton_1_cont, texto="Buscar", comando=buscar_datos, icono=None, posicion_img="left")
boton_Buscar.configure(fg_color="#3DC1E2")
boton_Buscar.grid(padx=5, pady=(2,4), sticky="snew")

boton_Registrar=ConfgBoton_estilo(boton_2_cont, texto="Guardar", comando=guardar_datos, icono=None, posicion_img="left")
boton_Registrar.configure(fg_color="#3DC1E2")
boton_Registrar.grid(padx=5, pady=(2,4), sticky="snew")

boton_Actualizar=ConfgBoton_estilo(boton_3_cont, texto="Modificar", comando=modificar, icono=None, posicion_img="left")
boton_Actualizar.configure(fg_color="#3DC1E2")
boton_Actualizar.grid(padx=5, pady=(2,4), sticky="snew")

boton_Eliminar=ConfgBoton_estilo(boton_4_cont, texto="Eliminar", comando=eliminacion, icono=None, posicion_img="left")
boton_Eliminar.configure(fg_color="#E00909")
boton_Eliminar.grid(padx=5, pady=(2,4), sticky="snew")

contenedor_Busqueda = ctk.CTkFrame(ventana, fg_color="transparent")
contenedor_Busqueda.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

contenedor_datos_lista = ctk.CTkFrame(ventana, fg_color="transparent")
contenedor_datos_lista.grid_columnconfigure(0, weight=0)
contenedor_datos_lista.grid_columnconfigure(1, weight=1)
contenedor_datos_lista.grid_rowconfigure(0, weight=1)
contenedor_datos_lista.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

contenedor_datos = ctk.CTkFrame(contenedor_datos_lista)
contenedor_datos.grid(row=1, column=0, sticky="nsew",padx=5, pady=5)

contenedor_lista= ctk.CTkFrame(contenedor_datos_lista)
contenedor_lista.grid(row=1, column=1, sticky ="nsew", padx=5, pady=5)

buscar = ctk.CTkLabel(contenedor_Busqueda, text="Buscar:", font=("Arial", 16, "bold"))
buscar.grid(row=0, column=0, padx=(10, 2), pady=2, sticky="w")

entry_buscar = ctk.CTkEntry(contenedor_Busqueda, font=("Arial", 14),
                             placeholder_text="Ingrese el nombre del producto a buscar o codigo",
                             width=1000,
                             height=40)
entry_buscar.bind("<KeyRelease>", lambda event: verificar_estado_buscar())
entry_buscar.grid(row=0, column=1, padx=(2, 10), pady=2, sticky="w")

nombre = ctk.CTkLabel(contenedor_datos, text="Nombre del Producto:", font=("Arial", 16, "bold"))
nombre.grid(row=1, column=0, padx=10, pady=2, sticky="w")

entry_nombre = ctk.CTkEntry(contenedor_datos, font=("Arial", 14),
                             placeholder_text="Ingrese el nombre del producto",
                             width=250,
                             height=40)
#entry_nombre.bind("<KeyRelease>", lambda event: verificar_estado_formulario())
entry_nombre.grid(row=2, column=0, padx=10, pady=2, sticky="w")

color = ctk.CTkLabel(contenedor_datos, text="Color:", font=("Arial", 16, "bold"))
color.grid(row=3, column=0, padx=10, pady=2, sticky="w")

entry_color = ctk.CTkEntry(contenedor_datos, font=("Arial", 14),
                            placeholder_text="Ingrese el color del producto",
                            width=250,
                            height=40)
#entry_color.bind("<KeyRelease>", lambda event: verificar_estado_formulario())
entry_color.grid(row=4, column=0, padx=10, pady=2, sticky="w")

categoria = ctk.CTkLabel(contenedor_datos, text="Categoría:", font=("Arial", 16, "bold"))
categoria.grid(row=5, column=0, padx=10, pady=2, sticky="w")

entry_categoria = ctk.CTkOptionMenu(contenedor_datos,
                                  values=["","Hombres", "Damas", "Niños", "Bebes"],
                                  command=lambda x: (validacion()),
                                  width=250,
                                  height=40,
                                  fg_color="white",
                                  font=("Arial", 14),
                                  text_color="black")
entry_categoria.grid(row=6, column = 0, padx=10, pady=(0, 5), sticky = "w")

talle= ctk.CTkLabel(contenedor_datos, text="Talle:", font=("Arial", 16, "bold"))
talle.grid(row=7, column=0, padx=10, pady=2, sticky="w")

entry_talle = ctk.CTkOptionMenu(contenedor_datos,
                                values=[""],
                                #command=lambda x: verificar_estado_formulario(),
                                width=250,
                                height=40,
                                fg_color="white",
                                font=("Arial", 16),
                                text_color="black")
entry_talle.grid(row=8, column=0, padx=10, pady=(0, 5), sticky="w")

cantidad = ctk.CTkLabel(contenedor_datos, text="Cantidad:", font=("Arial", 16, "bold"))
cantidad.grid(row=9, column=0, padx=10, pady=2, sticky="w")

entry_cantidad = ctk.CTkEntry(contenedor_datos, font=("Arial", 14),
                               placeholder_text="Ingrese la cantidad del producto",
                               width=250,
                               height=40)
#entry_cantidad.bind("<KeyRelease>", lambda event: verificar_estado_formulario())
entry_cantidad.grid(row=10, column=0, padx=10, pady=2, sticky="w")

precio_costo = ctk.CTkLabel(contenedor_datos, text="Precio costo:", font=("Arial", 16, "bold"))
precio_costo.grid(row=11, column=0, padx=10, pady=2, sticky="w")

entry_precio_costo = ctk.CTkEntry(contenedor_datos, font=("Arial", 14),
                            placeholder_text="Ingrese el precio del costo",
                            width=250,
                            height=40)
#entry_precio_costo.bind("<KeyRelease>", lambda event: verificar_estado_formulario())
entry_precio_costo.grid(row=12, column=0, padx=10, pady=2, sticky="w")

precio_venta = ctk.CTkLabel(contenedor_datos, text="Precio Venta:", font=("Arial", 16, "bold"))
precio_venta.grid(row=13, column=0, padx=10, pady=2, sticky="w")

entry_precio_venta = ctk.CTkEntry(contenedor_datos, font=("Arial", 14),
                            placeholder_text="Ingrese el precio a vender",
                            width=250,
                            height=40)
#entry_precio_venta.bind("<KeyRelease>", lambda event: verificar_estado_formulario())
entry_precio_venta.grid(row=14, column=0, padx=10, pady=2, sticky="w")

campos = [entry_nombre, entry_color, entry_categoria, entry_talle, entry_cantidad]
def verificar_estado_buscar(*args):
    if entry_buscar.get().strip() != "":
        for campo in campos:
            campo.configure(state="disabled")
    else:
        for campo in campos:
            campo.configure(state="normal")
    
#def verificar_estado_formulario(*args):
#    algunos_textos = any(campo.get().strip() != "" for campo in campos)
#    if algunos_textos:
#        entry_buscar.configure(state="disabled")
#    else:
#        entry_buscar.configure(state="normal")
        

def seleccion_de_fila(event):
    global id_seleccionado
    seleccion=tabla.selection()

    if not seleccion:
        return
    valores = tabla.item(seleccion[0], "values")
    id_seleccionado = valores[0]
    entry_nombre.delete(0, tk.END)
    entry_nombre.insert(0, valores[1])

    entry_color.delete(0, tk.END)
    entry_color.insert(0, valores[2])

    entry_categoria.set(valores[3])
    entry_talle.set(valores[4])

    entry_cantidad.delete(0, tk.END)
    entry_cantidad.insert(0, valores[5])

    entry_precio_costo.delete(0, tk.END)
    entry_precio_costo.insert(0, valores[6])

    entry_precio_venta.delete(0, tk.END)
    entry_precio_venta.insert(0, valores[7])

columna=("Codigo", "Nombre", "Color", "Categoria", "Talle", "Cantidad", "PrecioCosto", "PrecioVenta")
tabla= ttk.Treeview(contenedor_lista, columns=columna, show="headings", height=10)
tabla.bind("<<TreeviewSelect>>", seleccion_de_fila)

tabla.heading("Codigo", text="Codigo")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Color", text="Color")
tabla.heading("Categoria", text="Categoria")
tabla.heading("Talle", text="Talle")
tabla.heading("Cantidad", text="Cantidad")
tabla.heading("PrecioCosto", text="Precio Costo")
tabla.heading("PrecioVenta", text="Precio Venta")

tabla.column("Codigo", width=100, anchor="center")
tabla.column("Nombre", width=150, anchor="center")
tabla.column("Color", width=100, anchor="center")
tabla.column("Categoria", width=100, anchor="center")
tabla.column("Talle", width=100, anchor="center")
tabla.column("Cantidad", width=100, anchor="center")
tabla.column("PrecioCosto", width=100, anchor="center")
tabla.column("PrecioVenta", width=100, anchor="center")

tabla.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

boton_Actualizarlista=ConfgBoton_estilo(contenedor_lista, texto= "Actualizar lista", comando=lambda: mostrar_datos_tabla(tabla))
boton_Actualizarlista.configure(fg_color="#30BE2B")
boton_Actualizarlista.grid(row=1, column=0, padx=10, pady=(2,4), sticky="snew")

def limpiar_formulario():
    entry_nombre.delete(0, tk.END)
    entry_color.delete(0, tk.END)
    entry_categoria.set("")
    entry_talle.set("")
    entry_cantidad.delete(0, tk.END)
    entry_precio_costo.delete(0, tk.END)
    entry_precio_venta.delete(0, tk.END)

eliminar_datos_del_formulario = ctk.CTkButton(contenedor_lista, text="Limpiar formulario", command=lambda: limpiar_formulario())
eliminar_datos_del_formulario.configure(fg_color="#E08309")
eliminar_datos_del_formulario.grid(row=2, column=0, padx=10, pady=(2, 4), sticky="snew")

mostrar_datos_tabla(tabla)

ventana.mainloop()
