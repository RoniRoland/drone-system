from listaDobleCircular import ListaDobleCircular
from nodo import Nodo


class Contenidos:
    def __init__(self, dron):
        Nodo.__init__(self)
        self.dron = dron
        self.lista_alturas = ListaDobleCircular()
