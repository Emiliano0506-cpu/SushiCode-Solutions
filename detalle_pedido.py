class DetallePedido:
    def __init__(self,id_pedido,id_platillo,cantidad,costo_unitario,id_detalle=None):
        self.id_detalle=id_detalle; self.id_pedido=id_pedido; self.id_platillo=id_platillo
        self.cantidad=cantidad; self.costo_unitario=costo_unitario
    @property
    def id_detalle(self): return self.__id_detalle
    @id_detalle.setter
    def id_detalle(self,v): self.__id_detalle=v
    @property
    def id_pedido(self): return self.__id_pedido
    @id_pedido.setter
    def id_pedido(self,v): self.__id_pedido=int(v)
    @property
    def id_platillo(self): return self.__id_platillo
    @id_platillo.setter
    def id_platillo(self,v): self.__id_platillo=int(v)
    @property
    def cantidad(self): return self.__cantidad
    @cantidad.setter
    def cantidad(self,v):
        v=int(v)
        if v<1: raise ValueError("La cantidad debe ser mayor a cero")
        self.__cantidad=v
    @property
    def costo_unitario(self): return self.__costo_unitario
    @costo_unitario.setter
    def costo_unitario(self,v):
        v=float(v)
        if v<0: raise ValueError("El costo no puede ser negativo")
        self.__costo_unitario=v
    @property
    def subtotal(self): return self.__cantidad*self.__costo_unitario
