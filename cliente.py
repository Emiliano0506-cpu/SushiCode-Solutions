class Cliente:
    def __init__(self, nombre, apellido_paterno, apellido_materno="", telefono="", correo="",
                 rfc="", calle="", numero_exterior="", numero_interior="", colonia="",
                 codigo_postal="", ciudad="", estado="", id_cliente=None):
        self.id_cliente=id_cliente
        self.nombre=nombre
        self.apellido_paterno=apellido_paterno
        self.apellido_materno=apellido_materno
        self.telefono=telefono
        self.correo=correo
        self.rfc=rfc
        self.calle=calle
        self.numero_exterior=numero_exterior
        self.numero_interior=numero_interior
        self.colonia=colonia
        self.codigo_postal=codigo_postal
        self.ciudad=ciudad
        self.estado=estado

    @property
    def id_cliente(self): return self.__id_cliente
    @id_cliente.setter
    def id_cliente(self,v): self.__id_cliente=v
    @property
    def nombre(self): return self.__nombre
    @nombre.setter
    def nombre(self,v): self.__nombre=str(v).strip()
    @property
    def apellido_paterno(self): return self.__apellido_paterno
    @apellido_paterno.setter
    def apellido_paterno(self,v): self.__apellido_paterno=str(v).strip()
    @property
    def apellido_materno(self): return self.__apellido_materno
    @apellido_materno.setter
    def apellido_materno(self,v): self.__apellido_materno=str(v).strip()
    @property
    def telefono(self): return self.__telefono
    @telefono.setter
    def telefono(self,v): self.__telefono=str(v).strip()
    @property
    def correo(self): return self.__correo
    @correo.setter
    def correo(self,v): self.__correo=str(v).strip()
    @property
    def rfc(self): return self.__rfc
    @rfc.setter
    def rfc(self,v): self.__rfc=str(v).strip().upper()
    @property
    def calle(self): return self.__calle
    @calle.setter
    def calle(self,v): self.__calle=str(v).strip()
    @property
    def numero_exterior(self): return self.__numero_exterior
    @numero_exterior.setter
    def numero_exterior(self,v): self.__numero_exterior=str(v).strip()
    @property
    def numero_interior(self): return self.__numero_interior
    @numero_interior.setter
    def numero_interior(self,v): self.__numero_interior=str(v).strip()
    @property
    def colonia(self): return self.__colonia
    @colonia.setter
    def colonia(self,v): self.__colonia=str(v).strip()
    @property
    def codigo_postal(self): return self.__codigo_postal
    @codigo_postal.setter
    def codigo_postal(self,v): self.__codigo_postal=str(v).strip()
    @property
    def ciudad(self): return self.__ciudad
    @ciudad.setter
    def ciudad(self,v): self.__ciudad=str(v).strip()
    @property
    def estado(self): return self.__estado
    @estado.setter
    def estado(self,v): self.__estado=str(v).strip()
