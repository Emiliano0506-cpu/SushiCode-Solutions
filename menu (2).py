import funciones
from menu import crud

def menuPrincipal(db):
    while True:
        print("\\n=== MENÚ Y PLATILLOS ===\\n1. Crear menú\\n2. Mostrar menús\\n3. Agregar platillo\\n4. Mostrar platillos\\n5. Cambiar disponibilidad de platillo\\n6. Eliminar platillo\\n7. Regresar")
        op=input("Opción: ").strip()
        try:
            if op=="1":
                ident=crud.agregar_menu(input("Nombre del menú: "),input("Descripción: "),db)
                print("Menú creado. ID:",ident)
            elif op=="2":
                for r in crud.menus(db): print(r)
            elif op=="3":
                for m in crud.menus(db): print(m)
                ident=funciones.leer_entero("ID del menú: ",1)
                nombre=input("Nombre del platillo: ")
                descripcion=input("Descripción: ")
                categoria=input("Categoría: ")
                precio=funciones.leer_decimal("Precio: $")
                disponible=input("¿Disponible? (s/n): ").lower() in ("s","si","sí")
                print("Platillo agregado. ID:",crud.agregar_platillo(ident,nombre,descripcion,categoria,precio,disponible,db))
            elif op=="4":
                for r in crud.platillos(db): print(r)
            elif op=="5":
                ident=funciones.leer_entero("ID del platillo: ",1)
                disp=input("¿Disponible? (s/n): ").lower() in ("s","si","sí")
                cur=db.cursor(); cur.execute("UPDATE Platillos SET disponibilidad=%s WHERE id_platillo=%s",(disp,ident)); db.commit()
                print("Actualizado" if cur.rowcount else "No encontrado")
            elif op=="6":
                print("Eliminado" if crud.eliminar_platillo(funciones.leer_entero("ID: ",1),db) else "No encontrado")
            elif op=="7": return
            else: print("Opción no válida")
        except Exception as e: print("Error:",e)
        funciones.espereTecla()
