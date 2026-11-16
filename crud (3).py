def crear_pedido(id_cliente, detalles, db):
    cur=db.cursor()
    try:
        cur.execute("INSERT INTO Pedidos(id_cliente,estado,total) VALUES(%s,'En preparación',0)",(id_cliente,))
        pedido_id=cur.lastrowid
        total=0
        for id_platillo,cantidad,precio in detalles:
            subtotal=cantidad*precio
            cur.execute("INSERT INTO DetallePedido(id_pedido,id_platillo,cantidad,costo_unitario,subtotal) VALUES(%s,%s,%s,%s,%s)",(pedido_id,id_platillo,cantidad,precio,subtotal))
            total += subtotal
        cur.execute("UPDATE Pedidos SET total=%s WHERE id_pedido=%s",(total,pedido_id))
        db.commit()
        return pedido_id,total
    except Exception:
        db.rollback()
        raise

def consultar(db):
    cur=db.cursor()
    cur.execute("""SELECT p.id_pedido,c.nombre,c.apellido_paterno,p.fecha_hora,p.estado,p.total
    FROM Pedidos p JOIN Clientes c ON c.id_cliente=p.id_cliente ORDER BY p.id_pedido""")
    return cur.fetchall()

def detalle(ident,db):
    cur=db.cursor()
    cur.execute("""SELECT d.id_detalle,d.id_platillo,pl.nombre,d.cantidad,d.costo_unitario,d.subtotal
    FROM DetallePedido d JOIN Platillos pl ON pl.id_platillo=d.id_platillo WHERE d.id_pedido=%s""",(ident,))
    return cur.fetchall()

def cambiar_estado(ident,estado,db):
    cur=db.cursor()
    cur.execute("UPDATE Pedidos SET estado=%s WHERE id_pedido=%s",(estado,ident))
    db.commit()
    return cur.rowcount>0

def eliminar(ident,db):
    cur=db.cursor()
    cur.execute("DELETE FROM Pedidos WHERE id_pedido=%s",(ident,))
    db.commit()
    return cur.rowcount>0
