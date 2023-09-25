from nodo import Nodo


class Dron:
    def __init__(self, nombre):
        Nodo.__init__(self)
        self.nombre = nombre

    def mostrar_Nombre_dron(self):
        return self.nombre
