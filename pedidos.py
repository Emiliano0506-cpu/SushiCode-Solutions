"""Flujo de pedidos para clientes y administración."""
import funciones
from pedidos import crud
from menu import crud as menu_crud
from clientes import clientes as clientes_ui

def realizar_pedido(db):
    id_cliente=clientes_ui.seleccionar_o_registrar(db)
    if not id_cliente:
        print("No fue posible identificar al cliente.")
        return
    platillos=menu_crud.platillos(db,True)
    if not platillos:
        print("No hay platillos disponibles.")
        return
    print("\n=== PLATILLOS DISPONIBLES ===")
    for p in platillos:
        print(f"ID {p[0]} | {p[1]} | {p[2]} | ${float(p[3]):.2f} | {p[4]}")
    detalles=[]
    while True:
        try:
            pid=int(input("ID del platillo (0 para terminar): "))
            if pid==0: break
            p=next((x for x in platillos if x[0]==pid),None)
            if not p:
                print("Ese platillo no está disponible.")
                continue
            cantidad=int(input("Cantidad: "))
            if cantidad<1:
                print("La cantidad debe ser mayor a cero.")
                continue
            detalles.append((pid,cantidad,float(p[3])))
        except ValueError:
            print("Ingresa números válidos.")
            continue
        if not funciones.si_no("¿Agregar otro platillo?"):
            break
    if detalles:
        ident,total=crud.crear_pedido(id_cliente,detalles,db)
        print(f"\n¡Pedido registrado! Número: {ident} | Total: ${total:.2f}")
    else:
        print("No se agregó ningún producto.")

def menu_cliente(db):
    while True:
        print("\n=== PEDIDOS DEL CLIENTE ===\n1. Realizar pedido\n2. Consultar mis pedidos por ID de cliente\n3. Regresar")
        op=input("Opción: ").strip()
        if op=="1":
            realizar_pedido(db)
        elif op=="2":
            try:
                ident=int(input("ID de cliente: "))
                cur=db.cursor()
                cur.execute("""SELECT id_pedido,fecha_hora,estado,total FROM Pedidos
                               WHERE id_cliente=%s ORDER BY fecha_hora DESC""",(ident,))
                resultados=cur.fetchall()
                for r in resultados: print(r)
                if not resultados: print("No hay pedidos para ese cliente.")
            except ValueError: print("ID no válido.")
        elif op=="3": return
        else: print("Opción no válida")
        funciones.espereTecla()

def menuPrincipal(db):
    """Opciones administrativas de pedidos: solo se llama desde sesión admin."""
    while True:
        print("\n=== ADMINISTRACIÓN DE PEDIDOS ===\n1. Registrar pedido\n2. Mostrar todos\n3. Ver detalle\n4. Cambiar estado\n5. Eliminar\n6. Regresar")
        op=input("Opción: ").strip()
        try:
            if op=="1": realizar_pedido(db)
            elif op=="2":
                for r in crud.consultar(db): print(r)
            elif op=="3":
                ident=int(input("ID del pedido: "))
                for r in crud.detalle(ident,db): print(r)
            elif op=="4":
                ident=int(input("ID del pedido: "))
                estado=input("Nuevo estado: ")
                print("Actualizado" if crud.cambiar_estado(ident,estado,db) else "No encontrado")
            elif op=="5":
                ident=int(input("ID del pedido: "))
                print("Eliminado" if crud.eliminar(ident,db) else "No encontrado")
            elif op=="6": return
            else: print("Opción no válida")
        except Exception as e: print("Error:",e)
        funciones.espereTecla()
