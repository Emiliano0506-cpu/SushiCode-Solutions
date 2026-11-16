class Platillo:
    def __init__(self,id_menu,nombre,descripcion="",categoria="",precio=0,disponibilidad=True,id_platillo=None):
        self.id_platillo=id_platillo; self.id_menu=id_menu; self.nombre=nombre
        self.descripcion=descripcion; self.categoria=categoria; self.precio=precio; self.disponibilidad=disponibilidad
    @property
    def id_platillo(self): return self.__id_platillo
    @id_platillo.setter
    def id_platillo(self,v): self.__id_platillo=v
    @property
    def id_menu(self): return self.__id_menu
    @id_menu.setter
    def id_menu(self,v): self.__id_menu=int(v)
    @property
    def nombre(self): return self.__nombre
    @nombre.setter
    def nombre(self,v): self.__nombre=str(v).strip()
    @property
    def descripcion(self): return self.__descripcion
    @descripcion.setter
    def descripcion(self,v): self.__descripcion=str(v).strip()
    @property
    def categoria(self): return self.__categoria
    @categoria.setter
    def categoria(self,v): self.__categoria=str(v).strip()
    @property
    def precio(self): return self.__precio
    @precio.setter
    def precio(self,v):
        v=float(v)
        if v<0: raise ValueError("El precio no puede ser negativo")
        self.__precio=v
    @property
    def disponibilidad(self): return self.__disponibilidad
    @disponibilidad.setter
    def disponibilidad(self,v): self.__disponibilidad=bool(v)
