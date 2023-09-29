from nodo import Nodo


class Instrucciones:
    def __init__(self, dron, altura):
        Nodo.__init__(self)
        self.dron = dron
        self.altura = altura

    def mostrar_instrucciones(self):
        return f"        ** La instrucción para {self.dron} es de altura: {self.altura} **   "
