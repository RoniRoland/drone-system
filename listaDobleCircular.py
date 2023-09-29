class ListaDobleCircular:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamaño = 0

    def inicilizacion(self):
        self.primero = None
        self.ultimo = None

    def esta_vacia(self):
        return self.primero is None

    def tamano(self):
        return self.tamaño

    def indice(self, i):
        actual = self.primero
        contador = 0
        while contador < self.tamano():
            if (contador + 1) == i:
                return actual
            actual = actual.siguiente
            contador += 1

    def i_individual(self, numero):
        contador = 0
        actual = self.primero
        while contador < self.tamaño:
            if (contador + 1) == numero:
                return actual
            actual = actual.siguiente
            contador += 1

    def agregar_al_final(self, dato):
        if self.esta_vacia():
            self.primero = dato
            self.ultimo = dato
            self.tamaño += 1
        else:
            actual = self.primero
            while actual.siguiente is not None:
                actual = actual.siguiente
            dato.anterior = actual
            self.final = dato
            actual.siguiente = dato
            self.tamaño += 1

    def agregar_en_orden(self, dato):
        if self.esta_vacia():
            self.primero = dato
            self.ultimo = dato
        else:
            actual = self.primero

            # Buscar la posición correcta para insertar en orden alfabético
            while actual is not None and actual.nombre < dato.nombre:
                actual = actual.siguiente

            # Si el dato debe ir al principio de la lista
            if actual == self.primero:
                dato.siguiente = self.primero
                self.primero.anterior = dato
                self.primero = dato
            # Si el dato debe ir al final de la lista
            elif actual is None:
                dato.anterior = self.ultimo
                self.ultimo.siguiente = dato
                self.ultimo = dato
            # Si el dato debe ir en algún lugar del medio de la lista
            else:
                dato.anterior = actual.anterior
                dato.siguiente = actual
                actual.anterior.siguiente = dato
                actual.anterior = dato

    def eliminar(self, dato):
        if not self.esta_vacia():
            actual = self.primero
            while actual.dato != dato:
                actual = actual.siguiente
                if actual == self.primero:
                    return
            if actual == self.primero:
                self.primero = actual.siguiente
                self.ultimo.siguiente = self.primero
                self.primero.anterior = self.ultimo
            elif actual == self.ultimo:
                self.ultimo = actual.anterior
                self.ultimo.siguiente = self.primero
                self.primero.anterior = self.ultimo
            else:
                actual.anterior.siguiente = actual.siguiente
                actual.siguiente.anterior = actual.anterior

    def buscar_nombre(self, nombre):
        if not self.esta_vacia():
            actual = self.primero
            while actual is not None:
                if actual.nombre == nombre:
                    return nombre  # Se encontró un dron con el nombre especificado
                actual = actual.siguiente

            return None

    def mostrar(self):
        if not self.esta_vacia():
            actual = self.primero
            texto = "Listado de Drones en el Sistema\n"
            numero = 1
            while actual:
                texto += f"{numero}. {actual.mostrar_Nombre_dron()}\n"
                actual = actual.siguiente
                numero += 1
            return texto

    def mostrar_listadoMensajes_Instrucciones(self):
        listado_con_formato = ""
        actual = self.primero

        while actual:
            listado_con_formato += actual.mostrar_instrucciones() + "\n\n"
            actual = actual.siguiente

        return listado_con_formato
