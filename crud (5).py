def insertar(c, db):
    cur=db.cursor()
    cur.execute("""INSERT INTO Clientes
    (nombre,apellido_paterno,apellido_materno,telefono,correo,RFC,calle,numero_exterior,numero_interior,colonia,codigo_postal,ciudad,estado)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
    (c.nombre,c.apellido_paterno,c.apellido_materno,c.telefono,c.correo,c.rfc,c.calle,c.numero_exterior,c.numero_interior,c.colonia,c.codigo_postal,c.ciudad,c.estado))
    db.commit()
    return cur.lastrowid

def consultar(db):
    cur=db.cursor()
    cur.execute("SELECT id_cliente,nombre,apellido_paterno,apellido_materno,telefono,correo,ciudad,estado FROM Clientes ORDER BY id_cliente")
    return cur.fetchall()

def buscar(ident,db):
    cur=db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Clientes WHERE id_cliente=%s",(ident,))
    return cur.fetchone()

def actualizar(c,ident,db):
    cur=db.cursor()
    cur.execute("""UPDATE Clientes SET nombre=%s,apellido_paterno=%s,apellido_materno=%s,telefono=%s,correo=%s,RFC=%s,calle=%s,numero_exterior=%s,numero_interior=%s,colonia=%s,codigo_postal=%s,ciudad=%s,estado=%s WHERE id_cliente=%s""",
    (c.nombre,c.apellido_paterno,c.apellido_materno,c.telefono,c.correo,c.rfc,c.calle,c.numero_exterior,c.numero_interior,c.colonia,c.codigo_postal,c.ciudad,c.estado,ident))
    db.commit()
    return cur.rowcount > 0

def eliminar(ident,db):
    cur=db.cursor()
    cur.execute("DELETE FROM Clientes WHERE id_cliente=%s",(ident,))
    db.commit()
    return cur.rowcount > 0
