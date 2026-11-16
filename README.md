# SushiCode

Sistema de pedidos y administración de un restaurante de sushi, con interfaz gráfica en **Tkinter** y base de datos MySQL.

## Estructura
- `main.py`: inicia la aplicación gráfica.
- `interface.py`: ventanas, formularios, tablas, confirmaciones y navegación con Tkinter.
- `funciones.py`: conexión MySQL y funciones auxiliares.
- `modelos/`: clases (`cliente.py`, `menu.py`, `platillo.py`, `pedido.py`, `detalle_pedido.py`).
- `clientes/`: operaciones CRUD y captura de clientes.
- `menu/`: operaciones CRUD de menús y platillos.
- `pedidos/`: registro, consulta y administración de pedidos.
- `sql/schema.sql`: creación de las tablas de la base de datos.

## Permisos
- **Administrador:** usuario `admin`, contraseña `admin123`. Puede crear menús, agregar platillos, consultar platillos, cambiar su disponibilidad, eliminarlos y administrar pedidos.
- **Cliente:** no inicia sesión. Solo puede consultar los platillos disponibles y realizar pedidos. No tiene acceso a las pantallas de administración.

Las acciones que modifican información solicitan confirmación. Después de guardar un menú o platillo, el formulario queda limpio para capturar otro. Después de realizar un pedido aparece una pantalla de confirmación con opción de hacer otro pedido.

## Instalación y ejecución
1. Ejecuta `sql/schema.sql` en MySQL para crear la base de datos `bd_sushicode` y sus tablas.
2. Abre `funciones.py` y configura `HOST`, `USUARIO` y `PASSWORD` según tu instalación de MySQL.
3. Instala el conector: `pip install mysql-connector-python`.
4. Ejecuta desde la carpeta del proyecto: `python main.py`.

Tkinter normalmente viene incluido con Python. En algunas distribuciones de Linux puede ser necesario instalar el paquete `python3-tk`.

## Acceso de demostración
- Usuario: `admin`
- Contraseña: `admin123`

Cambia estas credenciales antes de utilizar el sistema en un entorno real.
