class Menu:
    def __init__(self,nombre,descripcion="",disponibilidad=True,id_menu=None):
        self.id_menu=id_menu; self.nombre=nombre; self.descripcion=descripcion; self.disponibilidad=disponibilidad
    @property
    def id_menu(self): return self.__id_menu
    @id_menu.setter
    def id_menu(self,v): self.__id_menu=v
    @property
    def nombre(self): return self.__nombre
    @nombre.setter
    def nombre(self,v): self.__nombre=str(v).strip()
    @property
    def descripcion(self): return self.__descripcion
    @descripcion.setter
    def descripcion(self,v): self.__descripcion=str(v).strip()
    @property
    def disponibilidad(self): return self.__disponibilidad
    @disponibilidad.setter
    def disponibilidad(self,v): self.__disponibilidad=bool(v)
