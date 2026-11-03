# Sistema de gestión para tienda de ropa

Aplicación de escritorio en Python para administrar el inventario de una tienda de ropa. Cuenta con una interfaz gráfica hecha con Tkinter y CustomTkinter, y utiliza SQLite para guardar productos y credenciales.

## Funcionalidades

- Iniciar sesión o registrar credenciales desde la pantalla inicial.
- Agregar productos con nombre, color, categoría, talle, cantidad y precios de costo y venta.
- Buscar productos por código o nombre.
- Seleccionar un producto de la tabla para modificarlo o eliminarlo.
- Actualizar la lista y limpiar el formulario.
- Elegir talles según la categoría: ropa de adultos, niños o bebés.

## Requisitos

- Python 3.10 o posterior.
- Tkinter, normalmente incluido con la instalación de Python.
- CustomTkinter.

Instala la dependencia externa con:

```bash
python -m pip install customtkinter
```

## Ejecución

Desde la carpeta del proyecto, ejecuta:

```bash
python proyectoFinal.py
```

La aplicación abre primero la ventana de inicio de sesión. Si las credenciales no existen, ofrece guardarlas para volver a ingresar. Después de acceder, se abre la ventana de gestión de inventario.

## Base de datos

El proyecto incluye el archivo SQLite `tiendaropa`, que el programa abre desde la carpeta de trabajo actual. Debe contener estas tablas y columnas:

- `ropa`: `codigo_barra`, `nombre_ropa`, `color`, `categoria`, `talle`, `cantidad`, `preciocosto`, `precioventa`.
- `datos`: `usuario`, `contrasena`.

El código no crea las tablas automáticamente. Si se mueve el programa, conserva el archivo `tiendaropa` en la carpeta desde la que se ejecuta o ajusta la ruta en `proyectoFinal.py`.

## Uso básico

1. Ingresa con una cuenta existente o registra las credenciales cuando la aplicación lo solicite.
2. Completa los datos del producto y pulsa **Guardar**.
3. Para encontrar un producto, escribe su nombre o código en la búsqueda.
4. Selecciona una fila de la tabla para cargar sus datos en el formulario.
5. Pulsa **Modificar** o **Eliminar** para aplicar cambios. La eliminación solicita confirmación.
6. Usa **Actualizar lista** para volver a mostrar todos los productos.

## Estructura del proyecto

```text
proyectoFinal/
├── proyectoFinal.py   # Interfaz, validaciones y operaciones de inventario
├── tiendaropa         # Base de datos SQLite
└── README.md
```
