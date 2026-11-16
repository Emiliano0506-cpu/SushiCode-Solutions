class Pedido:
    def __init__(self,id_cliente,estado="En preparación",total=0,id_pedido=None):
        self.id_pedido=id_pedido; self.id_cliente=id_cliente; self.estado=estado; self.total=total
    @property
    def id_pedido(self): return self.__id_pedido
    @id_pedido.setter
    def id_pedido(self,v): self.__id_pedido=v
    @property
    def id_cliente(self): return self.__id_cliente
    @id_cliente.setter
    def id_cliente(self,v): self.__id_cliente=int(v)
    @property
    def estado(self): return self.__estado
    @estado.setter
    def estado(self,v): self.__estado=str(v).strip()
    @property
    def total(self): return self.__total
    @total.setter
    def total(self,v): self.__total=float(v)
