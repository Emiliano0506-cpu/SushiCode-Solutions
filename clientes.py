"""Funciones de captura y consulta de clientes para el flujo de compra."""
from modelos import Cliente
from clientes import crud

def registrar_cliente_rapido(db):
    print("\n=== DATOS DEL CLIENTE ===")
    cliente=Cliente(
        input("Nombre: "), input("Apellido paterno: "), input("Apellido materno (opcional): "),
        input("Teléfono: "), input("Correo (opcional): "), ciudad=input("Ciudad: "), estado=input("Estado: "))
    return crud.insertar(cliente,db)

def seleccionar_o_registrar(db):
    print("\n¿Ya estás registrado?")
    print("1. Sí, ingresar mi ID de cliente")
    print("2. No, registrar mis datos")
    op=input("Opción: ").strip()
    if op=="1":
        try:
            ident=int(input("ID de cliente: "))
            if crud.buscar(ident,db):
                return ident
            print("No se encontró ese cliente.")
        except ValueError:
            print("ID no válido.")
    elif op=="2":
        return registrar_cliente_rapido(db)
    return None
