from listaDobleCircular import ListaDobleCircular
from nodo import Nodo


class Mensajes:
    def __init__(self, nombre, sistemaDrones):
        Nodo.__init__(self)
        self.nombre = nombre
        self.sistemaDrones = sistemaDrones
        self.lista_instrucciones = ListaDobleCircular()

    def mostrar_instrucciones(self):
        mensaje = f"-Mensaje: *{self.nombre}* -> utiliza el sistema de drones {self.sistemaDrones} -> \n\nInstrucciones son: \n\n"
        instrucciones_texto = (
            self.lista_instrucciones.mostrar_listadoMensajes_Instrucciones()
        )
        return mensaje + instrucciones_texto
