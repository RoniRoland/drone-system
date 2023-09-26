from nodo import Nodo


class Alturas:
    def __init__(self, valor, letra):
        Nodo.__init__(self)
        self.valor = valor
        self.letra = letra

    def mostrar_alturas(self):
        f"altura: {self.valor} , letra: {self.letra}"
