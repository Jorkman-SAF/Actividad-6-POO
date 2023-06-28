import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os

class AgendaAmigos:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Agenda de Amigos")
        self.ventana.geometry("300x300")

        self.etiqueta = tk.Label(self.ventana, text="")
        self.etiqueta.pack()

        self.frame_botones = tk.Frame(self.ventana)
        self.frame_botones.pack(pady=10)

        self.boton_crear = tk.Button(self.frame_botones, text="Crear", command=self.crear_amigo)
        self.boton_crear.pack(side="left", padx=5)

        self.boton_leer = tk.Button(self.frame_botones, text="Leer", command=self.leer_amigo)
        self.boton_leer.pack(side="left", padx=5)

        self.boton_actualizar = tk.Button(self.frame_botones, text="Actualizar", command=self.abrir_ventana_actualizar)
        self.boton_actualizar.pack(side="left", padx=5)

        self.boton_borrar = tk.Button(self.frame_botones, text="Borrar", command=self.abrir_ventana_borrar)
        self.boton_borrar.pack(side="left", padx=5)

        self.carpeta_destino = ""

    def crear_amigo(self):
        if not self.carpeta_destino:
            self.seleccionar_carpeta()

        archivo = os.path.join(self.carpeta_destino, "contacto_de_amigos.txt")

        if os.path.exists(archivo):
            messagebox.showinfo("Crear Amigo", "La agenda ya existe")
        else:
            with open(archivo, "w") as f:
                f.write("Nombre".ljust(20) + "Número\n")
            messagebox.showinfo("Crear Amigo", f"Archivo creado exitosamente en:\n{archivo}")

    def seleccionar_carpeta(self):
        self.carpeta_destino = filedialog.askdirectory()
        if self.carpeta_destino:
            self.etiqueta.config(text="Carpeta seleccionada:\n" + self.carpeta_destino)

    def leer_amigo(self):
        if not self.carpeta_destino:
            messagebox.showinfo("Leer Amigo", "No se ha seleccionado una carpeta")
            return

        archivo = os.path.join(self.carpeta_destino, "contacto_de_amigos.txt")

        if os.path.exists(archivo):
            with open(archivo, "r") as f:
                contenido = f.read()
            messagebox.showinfo("Leer Amigo", f"Contenido del archivo:\n{contenido}")
        else:
            messagebox.showinfo("Leer Amigo", "La agenda no existe")

    def abrir_ventana_actualizar(self):
        ventana_actualizar = tk.Toplevel(self.ventana)
        ventana_actualizar.title("Nuevo contacto")

        label_nombre = tk.Label(ventana_actualizar, text="Nombre de contacto:")
        label_nombre.pack()
        self.entry_nombre = tk.Entry(ventana_actualizar, validate="key")
        self.entry_nombre.pack()
        self.entry_nombre.config(validatecommand=(self.entry_nombre.register(self.validar_nombre), "%P"))

        label_telefono = tk.Label(ventana_actualizar, text="Teléfono:")
        label_telefono.pack()
        self.entry_telefono = tk.Entry(ventana_actualizar, validate="key")
        self.entry_telefono.pack()
        self.entry_telefono.config(validatecommand=(self.entry_telefono.register(self.validar_telefono), "%P"))

        boton_crear = tk.Button(ventana_actualizar, text="Crear", command=self.crear_contacto)
        boton_crear.pack(pady=10)

    def validar_nombre(self, entrada):
        if len(entrada) <= 12:
            return True
        else:
            return False

    def validar_telefono(self, entrada):
        if len(entrada) <= 10 and entrada.isdigit():
            return True
        else:
            return False

    def crear_contacto(self):
        nombre = self.entry_nombre.get()
        telefono = self.entry_telefono.get()

        if nombre and telefono:
            if not self.carpeta_destino:
                messagebox.showinfo("Crear Contacto", "No se ha seleccionado una carpeta")
                return

            archivo = os.path.join(self.carpeta_destino, "contacto_de_amigos.txt")

            with open(archivo, "a") as f:
                f.write(f"{nombre.ljust(20)}{telefono}\n")

            messagebox.showinfo("Crear Contacto", "Contacto creado exitosamente")
        else:
            messagebox.showinfo("Crear Contacto", "Por favor, completa todos los campos")

    def abrir_ventana_borrar(self):
        ventana_borrar = tk.Toplevel(self.ventana)
        ventana_borrar.title("Borrar contacto")

        label_nombre = tk.Label(ventana_borrar, text="Nombre de contacto:")
        label_nombre.pack()
        self.entry_borrar_nombre = tk.Entry(ventana_borrar)
        self.entry_borrar_nombre.pack()

        boton_eliminar = tk.Button(ventana_borrar, text="Eliminar", command=self.eliminar_contacto)
        boton_eliminar.pack(pady=10)

    def eliminar_contacto(self):
        nombre = self.entry_borrar_nombre.get()

        if nombre:
            if not self.carpeta_destino:
                messagebox.showinfo("Borrar Contacto", "No se ha seleccionado una carpeta")
                return

            archivo = os.path.join(self.carpeta_destino, "contacto_de_amigos.txt")
            temp_file = os.path.join(self.carpeta_destino, "temp_contactos.txt")

            with open(archivo, "r") as f, open(temp_file, "w") as temp:
                contactos = f.readlines()
                encontrado = False
                for contacto in contactos:
                    if contacto.startswith(nombre):
                        encontrado = True
                    else:
                        temp.write(contacto)

            if encontrado:
                os.remove(archivo)
                os.rename(temp_file, archivo)
                messagebox.showinfo("Borrar Contacto", "Contacto borrado exitosamente")
            else:
                os.remove(temp_file)
                messagebox.showinfo("Borrar Contacto", "No se encontró el contacto en la agenda")
        else:
            messagebox.showinfo("Borrar Contacto", "Por favor, ingresa el nombre del contacto a borrar")

    def iniciar(self):
        self.ventana.mainloop()

agenda = AgendaAmigos()
agenda.iniciar()
