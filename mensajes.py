from listaDobleCircular import ListaDobleCircular
from nodo import Nodo


class Mensajes:
    def __init__(self, nombre, sistemaDrones):
        Nodo.__init__(self)
        self.nombre = nombre
        self.sistemaDrones = sistemaDrones
        self.lista_instrucciones = ListaDobleCircular()

    def mostrar_instrucciones(self):
        mensaje = f"-Mensaje: *{self.nombre}* -> Sistema de drones {self.sistemaDrones} -> \n\nInstrucciones son: \n\n"
        instrucciones_texto = (
            self.lista_instrucciones.mostrar_listadoMensajes_Instrucciones()
        )
        return mensaje + instrucciones_texto

    def mostrar_instrucciones_individual(self):
        mensaje = f"Sistema de Dron *{self.sistemaDrones}* \n\n"
        instrucciones_texto = (
            self.lista_instrucciones.mostrar_listadoMensajes_Instrucciones_individuales()
        )
        return mensaje + instrucciones_texto
