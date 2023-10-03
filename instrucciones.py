from nodo import Nodo


class Instrucciones:
    def __init__(self, dron, altura):
        Nodo.__init__(self)
        self.dron = dron
        self.altura = altura

    def mostrar_instrucciones(self):
        return f"        ** Instrucción {self.dron} es de altura: {self.altura} **   "

    def mostrar_instrucciones_individual(self):
        return f" ** Instrucción del {self.dron} es de altura: {self.altura} ** "
