from listaDobleCircular import ListaDobleCircular
from nodo import Nodo


class SistemaDrones:
    def __init__(self, nombre, altura_maxima, cantidad_drones):
        Nodo.__init__(self)
        self.nombre = nombre
        self.altura_maxima = altura_maxima
        self.cantidad_drones = cantidad_drones
        self.lista_contenidos = ListaDobleCircular()
