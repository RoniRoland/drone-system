import tkinter as tk
from tkinter import filedialog, simpledialog
from tkinter import messagebox
import xml.etree.ElementTree as Et
from dron import Dron
from listaDobleCircular import ListaDobleCircular
from sistemaDrones import SistemaDrones
from contenidos import Contenidos
from alturas import Alturas
from mensajes import Mensajes
from instrucciones import Instrucciones
import os
from graphviz import Digraph


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Drones")
        self.root.geometry("800x600")
        self.lista_drones = ListaDobleCircular()
        self.lista_sistema_drones = ListaDobleCircular()
        self.lista_mensajes = ListaDobleCircular()

        # Barra de menú
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Cargar archivo XML", command=self.cargar_xml)
        file_menu.add_command(label="Generar archivo XML", command=self.generar_xml)

        # Menú Gestión de Drones
        drones_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Gestión de Drones", menu=drones_menu)
        drones_menu.add_command(
            label="Ver listado de drones ordenado alfabéticamente",
            command=self.ver_drones,
        )
        drones_menu.add_command(
            label="Agregar un nuevo dron", command=self.agregar_dron
        )

        # Menú Gestión de Sistemas de Drones
        sistemas_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Gestión de Sistemas de Drones", menu=sistemas_menu)
        sistemas_menu.add_command(
            label="Ver gráficamente listado de sistemas de drones",
            command=self.ver_sistemas,
        )

        # Menú Gestión de Mensajes
        mensajes_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Gestión de Mensajes", menu=mensajes_menu)
        mensajes_menu.add_command(
            label="Ver listado de mensajes y sus instrucciones",
            command=self.ver_mensajes,
        )
        mensajes_menu.add_command(
            label="Ver instrucciones para enviar un mensaje",
            command=self.ver_instrucciones,
        )

        # Menú Ayuda
        ayuda_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=ayuda_menu)
        ayuda_menu.add_command(label="Acerca de...", command=self.acerca_de)

        # Cuadro de texto
        self.text_box = tk.Text(root, wrap=tk.WORD)
        self.text_box.pack(fill=tk.BOTH, expand=True)

    def cargar_xml(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos XML", "*.xml")])
        if file_path:
            messagebox.showinfo("Carga de Archivo", "Archivo cargado con éxito")
            self.lista_drones.inicilizacion()
            tree = Et.parse(file_path)
            root = tree.getroot()

            # dron(nombre)
            for lista_drones in root.findall("listaDrones"):
                for dron in lista_drones.findall("dron"):
                    dron_nuevo = Dron(dron.text)
                    self.lista_drones.agregar_en_orden(dron_nuevo)

            # sistemadrones(nombre, altura_maxima, cantidad_drones, [listacontenidos])
            for lista_sistemas in root.findall("listaSistemasDrones"):
                for sistemaDron in lista_sistemas.findall("sistemaDrones"):
                    nombre = sistemaDron.get("nombre")
                    altura_maxima = sistemaDron.find("alturaMaxima").text
                    cantidad_drones = sistemaDron.find("cantidadDrones").text
                    sistema_nuevo = SistemaDrones(
                        nombre, altura_maxima, cantidad_drones
                    )

                    for contenido in sistemaDron.findall("contenido"):
                        dron = contenido.find("dron").text
                        contenido_nuevo = Contenidos(dron)
                        sistema_nuevo.lista_contenidos.agregar_al_final(contenido_nuevo)
                        for alturas in contenido.findall("alturas"):
                            for altura in alturas.findall("altura"):
                                valor = altura.get("valor")
                                letra = altura.text
                                altura_nueva = Alturas(valor, letra)
                                contenido_nuevo.lista_alturas.agregar_al_final(
                                    altura_nueva
                                )
                    self.lista_sistema_drones.agregar_al_final(sistema_nuevo)

            # mensajes(nombre, sistemaDrones, [listainstrucciones])
            for mensajes in root.findall("listaMensajes"):
                for mensaje in mensajes.findall("Mensaje"):
                    nombre = mensaje.get("nombre")
                    sistemaDrones = mensaje.find("sistemaDrones").text
                    mensaje_nuevo = Mensajes(nombre, sistemaDrones)
                    for instrucciones in mensaje.findall("instrucciones"):
                        for instruccion in instrucciones.findall("instruccion"):
                            dron = instruccion.get("dron")
                            altura = instruccion.text
                            instruccion_nueva = Instrucciones(dron, altura)
                            mensaje_nuevo.lista_instrucciones.agregar_al_final(
                                instruccion_nueva
                            )
                    self.lista_mensajes.agregar_en_orden(mensaje_nuevo)

            self.lista_mensajes.mostrar_listadoMensajes_Instrucciones()

    def generar_xml(self):
        # Lógica para generar un archivo XML
        pass

    def ver_drones(self):
        listado = self.lista_drones.mostrar()
        if listado:
            self.text_box.delete(1.0, tk.END)  # Limpiar el cuadro de texto
            for dron in listado:
                self.text_box.insert(tk.END, dron)
        else:
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, "No hay drones para mostrar.")

    def agregar_dron(self):
        listado = self.lista_drones.mostrar()
        if listado:
            nuevo_dron = simpledialog.askstring(
                "Agregar nuevo dron", "Ingrese el nombre del nuevo dron:"
            )
            if nuevo_dron:
                nombre_nuevo = self.lista_drones.buscar_nombre(nuevo_dron)
                if nombre_nuevo:
                    messagebox.showerror(
                        "DRON YA EXISTE", f"El {nuevo_dron} ya existe en el sistema"
                    )
                else:
                    messagebox.showinfo(
                        "EXITO",
                        f"El Dron {nuevo_dron} ha sido agregado exitosamente al sistema",
                    )
                    self.lista_drones.agregar_en_orden(Dron(nuevo_dron))
                    self.actualizar_grafo_drones()
        else:
            messagebox.showerror(
                "SIN DATOS",
                "Primero cargue el archivo xml para verificar el listado de drones",
            )

    def ver_sistemas(self):
        pass

    def ver_mensajes(self):
        listado_mens = self.lista_mensajes.mostrar_listadoMensajes_Instrucciones()

        if listado_mens:
            self.text_box.delete(1.0, tk.END)  # Limpiar el cuadro de texto
            self.text_box.insert(
                tk.END,
                "\n=======================LISTADO DE MENSAJES CON INSTRUCCIONES============\n\n\n",
            )
            for mens in listado_mens:
                self.text_box.insert(tk.END, mens)

    def ver_instrucciones(self):
        # Lógica para ver las instrucciones para enviar un mensaje
        pass

    def acerca_de(self):
        # Lógica para mostrar información "Acerca de"
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
