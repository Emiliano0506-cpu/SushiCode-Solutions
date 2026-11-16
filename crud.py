def menus(db):
    cur=db.cursor()
    cur.execute("SELECT id_menu,nombre,descripcion,disponibilidad FROM Menu ORDER BY id_menu")
    return cur.fetchall()

def platillos(db, disponibles=False):
    cur=db.cursor()
    sql="SELECT p.id_platillo,p.nombre,p.categoria,p.precio,p.descripcion,p.disponibilidad,m.nombre FROM Platillos p JOIN Menu m ON m.id_menu=p.id_menu"
    if disponibles: sql += " WHERE p.disponibilidad=TRUE AND m.disponibilidad=TRUE"
    sql += " ORDER BY p.id_platillo"
    cur.execute(sql)
    return cur.fetchall()

def agregar_menu(nombre,descripcion,db):
    cur=db.cursor()
    cur.execute("INSERT INTO Menu(nombre,descripcion) VALUES(%s,%s)",(nombre,descripcion))
    db.commit()
    return cur.lastrowid

def agregar_platillo(id_menu,nombre,descripcion,categoria,precio,disponible,db):
    """Inserta el platillo y su relación con el menú en una sola transacción."""
    cur=db.cursor()
    try:
        cur.execute("SELECT id_menu FROM Menu WHERE id_menu=%s",(id_menu,))
        if cur.fetchone() is None:
            raise ValueError("El menú seleccionado no existe. Actualiza la lista de menús.")
        cur.execute("INSERT INTO Platillos(id_menu,nombre,descripcion,categoria,precio,disponibilidad) VALUES(%s,%s,%s,%s,%s,%s)",(id_menu,nombre,descripcion,categoria,precio,disponible))
        ident=cur.lastrowid
        cur.execute("INSERT INTO Platillos_Menu(id_platillo,id_menu) VALUES(%s,%s)",(ident,id_menu))
        db.commit()
        return ident
    except Exception:
        db.rollback()
        raise

def eliminar_platillo(ident,db):
    cur=db.cursor()
    cur.execute("DELETE FROM Platillos WHERE id_platillo=%s",(ident,))
    db.commit()
    return cur.rowcount>0
