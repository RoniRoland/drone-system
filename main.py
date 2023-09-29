import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, simpledialog
from tkinter import messagebox
from tkinter import font
import webbrowser
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
        self.root.geometry("850x600")
        self.root.configure(bg="#212325")
        self.lista_drones = ListaDobleCircular()
        self.lista_sistema_drones = ListaDobleCircular()
        self.lista_mensajes = ListaDobleCircular()

        # Barra de menú
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        # Cuadro de texto
        self.text_box = tk.Text(root, wrap=tk.WORD, width=75, height=35)
        self.text_box.place(relx=0.40, rely=0.5, anchor="center")
        # Cambiar el tamaño de la letra en el cuadro de texto

        self.text_box.configure(
            background="#23262e", foreground="white", insertbackground="white"
        )

        text_style = (
            "Helvetica",
            18,
        )  # Cambia "Helvetica" y 12 al estilo y tamaño de fuente que desees

        # Aplicar el estilo de fuente al texto del cuadro de texto
        self.text_box.tag_configure("my_font", font=text_style)

        # Crear el marco para los botones de "Archivo"
        self.marco_archivo = tk.LabelFrame(
            self.root,
            text="Archivo",
            font=("Roboto Medium", 20),
            background="#263238",
            foreground="white",
            width=200,  # Ancho del marco
            height=400,  # Alto del marco
        )
        self.marco_archivo.place(relx=0.95, rely=0.5, anchor="e")

        # Crear los botones de "Archivo"
        self.boton_cargar = tk.Button(
            master=self.marco_archivo,
            text="Cargar Archivo XML",
            font=("Roboto Medium", 11),
            bg="#0059b3",
            activebackground="#0059b3",
            foreground="white",
            activeforeground="white",
            width=15,
            height=1,
            command=self.cargar_xml,
        )
        self.boton_cargar.pack(side="top", pady=25)

        self.boton_generar = tk.Button(
            self.marco_archivo,
            text="Generar Archivo XML",
            font=("Roboto Medium", 11),
            bg="#6F16FD",
            activebackground="#0059b3",
            foreground="white",
            activeforeground="white",
            width=15,
            height=1,
            command=self.generar_xml,
        )
        self.boton_generar.pack(side="top", pady=25)

        self.boton_inicializar = tk.Button(
            self.marco_archivo,
            text="Inicializar",
            font=("Roboto Medium", 11),
            bg="#ff6c37",
            activebackground="#D35B58",
            foreground="white",
            activeforeground="white",
            width=15,
            height=1,
            command=self.inicio,
        )
        self.boton_inicializar.pack(side="top", pady=25)

        self.boton_salir = tk.Button(
            self.marco_archivo,
            text="Salir",
            font=("Roboto Medium", 11),
            bg="#D35B58",
            activebackground="#D35B58",
            foreground="white",
            activeforeground="white",
            width=15,
            height=1,
            command=self.salir,
        )
        self.boton_salir.pack(side="top", pady=25)

        # Menú Gestión de Drones
        drones_menu = tk.Menu(menubar, tearoff=0, bg="#263238", fg="white")
        menubar.add_cascade(label="Gestión de Drones", menu=drones_menu)
        drones_menu.add_command(
            label="Ver listado de drones ordenado alfabéticamente",
            command=self.ver_drones,
        )
        drones_menu.add_command(
            label="Agregar un nuevo dron", command=self.agregar_dron
        )

        # Menú Gestión de Sistemas de Drones
        sistemas_menu = tk.Menu(menubar, tearoff=0, bg="#263238", fg="white")
        menubar.add_cascade(label="Gestión de Sistemas de Drones", menu=sistemas_menu)
        sistemas_menu.add_command(
            label="Ver gráficamente listado de sistemas de drones",
            command=self.ver_sistemas,
        )

        # Menú Gestión de Mensajes
        mensajes_menu = tk.Menu(menubar, tearoff=0, bg="#263238", fg="white")
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
        ayuda_menu = tk.Menu(menubar, tearoff=0, bg="#263238", fg="white")
        menubar.add_cascade(label="Ayuda", menu=ayuda_menu)
        ayuda_menu.add_command(label="Acerca de...", command=self.acerca_de)

    def cargar_xml(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos XML", "*.xml")])
        if file_path:
            messagebox.showinfo("Carga de Archivo", "Archivo cargado con éxito")
            self.lista_drones.inicilizacion()
            self.lista_sistema_drones.inicilizacion()
            self.lista_mensajes.inicilizacion()
            self.text_box.delete(1.0, tk.END)
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

    def inicio(self):
        self.lista_drones.inicilizacion()
        self.lista_sistema_drones.inicilizacion()
        self.lista_mensajes.inicilizacion()
        self.text_box.delete(1.0, tk.END)
        messagebox.showinfo(
            "Sistema LIMPIO",
            f"El sistema ha sido limpiado correctamente",
        )

    def generar_xml(self):
        # Lógica para generar un archivo XML
        pass

    def ver_drones(self):
        listado = self.lista_drones.mostrar()
        if listado:
            self.text_box.delete(1.0, tk.END)  # Limpiar el cuadro de texto
            for dron in listado:
                self.text_box.insert(tk.END, dron, "my_font")
        else:
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, "No hay drones para mostrar.", "my_font")

    def agregar_dron(self):
        listado = self.lista_drones.mostrar()
        if listado:
            nuevo_dron = self.ventana_agregar_dron()
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
                    self.ver_drones()

        else:
            messagebox.showerror(
                "SIN DATOS",
                "Primero cargue el archivo xml para verificar el listado de drones",
            )

    def ventana_agregar_dron(self):
        # Crear una nueva ventana emergente personalizada
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar nuevo dron")

        # Cambiar el color de fondo de la ventana emergente
        dialog.configure(bg="#23262e")

        # Crear una etiqueta y un cuadro de texto para la entrada del usuario
        label = tk.Label(
            dialog, text="Ingrese el nombre del nuevo dron:", bg="#23262e", fg="white"
        )
        label.pack(padx=20, pady=10)

        entry_value = (
            tk.StringVar()
        )  # Variable para almacenar el valor del cuadro de texto
        entry = tk.Entry(dialog, textvariable=entry_value)
        entry.pack(padx=20, pady=10)

        # Función para obtener el valor del cuadro de texto
        def get_value():
            result = entry_value.get()  # Obtener el valor de la variable
            dialog.destroy()
            return result

        # Crear un botón de aceptar
        button = tk.Button(
            dialog, text="Aceptar", command=get_value, bg="#0059b3", fg="white"
        )
        button.pack(padx=20, pady=10)

        dialog.transient(self.root)  # Establece la ventana principal como padre
        dialog.grab_set()  # Bloquea la ventana principal
        self.root.wait_window(dialog)  # Espera hasta que se cierre la ventana

        return entry_value.get()

    def ver_sistemas(self):
        pass

    def ver_mensajes(self):
        listado_mens = self.lista_mensajes.mostrar_listadoMensajes_Instrucciones()

        if listado_mens:
            self.text_box.delete(1.0, tk.END)  # Limpiar el cuadro de texto
            self.text_box.insert(
                tk.END,
                "\n==LISTADO DE MENSAJES CON INSTRUCCIONES==\n\n\n",
                "my_font",
            )
            for mens in listado_mens:
                self.text_box.insert(tk.END, mens, "my_font")

    def ver_instrucciones(self):
        # Lógica para ver las instrucciones para enviar un mensaje
        pass

    def acerca_de(self):
        ventana_estudiante = tk.Toplevel()
        ventana_estudiante.title("Estudiante")
        ventana_estudiante.geometry("700x515")
        ventana_estudiante.configure(bg="#212325")

        datos_estudiante = tk.Label(
            ventana_estudiante,
            text=(
                "\n** Edgar Rolando Ramirez Lopez **\n\n"
                "201212891\n\n"
                "Introduccion a la Programacion y Computacion 2\n\n"
                "Seccion B\n\n"
                "Ingenieria en Ciencias y Sistemas\n\n"
                "4to Semestre"
            ),
            font=("Helvetica", 18),
            bg="#263238",
            foreground="white",
        )
        datos_estudiante.pack()

        pdf_manual_T = tk.Label(
            ventana_estudiante,
            text="Manual Tecnico",
            font=("Helvetica", 14),
            bg="#263238",
            foreground="white",
            cursor="hand2",
        )
        pdf_manual_T.pack()
        ruta_manual_T = os.path.join("Manuales", "manual_tecnico_ProyectoNO2.pdf")
        pdf_manual_T.bind("<Button-1>", lambda e: self.abrir_pdf(ruta_manual_T))

        pdf_manual_U = tk.Label(
            ventana_estudiante,
            text="Manual Usuario",
            font=("Helvetica", 14),
            bg="#263238",
            foreground="white",
            cursor="hand2",
        )
        pdf_manual_U.pack()
        ruta_manual_U = os.path.join("Manuales", "manual_tecnico_ProyectoNO2.pdf")
        pdf_manual_U.bind("<Button-1>", lambda e: self.abrir_pdf(ruta_manual_U))

    def abrir_pdf(self, ruta):
        try:
            os.startfile(
                ruta
            )  # Abre el archivo con el programa predeterminado en Windows
        except Exception as e:
            print(f"Error al abrir el archivo PDF: {e}")

    def salir(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
