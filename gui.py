import os
import sys
import tkinter as tk
import customtkinter as ctk
import threading
import backend
import baseDatos
from customtkinter import filedialog, CTkButton

CAPACIDADES_BD = {
    "BD-R SL (25GB)": 25_025_314_816,
    "BD-R DL (50GB)": 50_050_629_632,
    "BD-R TL (100GB)": 100_103_356_416,
    "BD-R XL (128GB)": 128_001_769_472
}

def resolver_ruta(ruta_relativa):
    """Devuelve la ruta absoluta al recurso, ya sea en desarrollo o en el .exe compilado"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.abspath("."), ruta_relativa)

class GestorPreservacion(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestor Preservación Digital")
        self.geometry("950x750")
        self.iconbitmap(resolver_ruta("favicon.ico"))
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)
        self.tab_rar = self.tabs.add("Generar RARs")
        self.tab_grabar = self.tabs.add("Preparar buffer y grabar disco")
        self.tab_bbdd = self.tabs.add("Gestión de base de datos")

        self.construir_pestana_grabar()
        self.construir_pestana_bbdd()
        self.construir_pestana_rar()

    def construir_pestana_rar(self):
        self.ruta_origen = ctk.StringVar(value="")
        self.ruta_destino = ctk.StringVar(value="no olvides poner archivo.rar al final de la ruta")

        ctk.CTkLabel(self.tab_rar, text="Empaquetado y compresión",
                     font=("Arial", 20, "bold")).pack(pady=20)
        frame_inputs = ctk.CTkFrame(self.tab_rar, fg_color="transparent")
        frame_inputs.pack(pady=10)

        #Origen
        ctk.CTkLabel(frame_inputs, text="Carpeta a comprimir").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ctk.CTkEntry(frame_inputs, textvariable=self.ruta_origen, width=450).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(frame_inputs, text="Explorar", command=self.seleccionar_origen).grid(row=0, column=2, padx=10, pady=10)

        #Destino
        ctk.CTkLabel(frame_inputs, text="Carpeta de destino").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        ctk.CTkEntry(frame_inputs, textvariable=self.ruta_destino, width=450).grid(row=1, column=1, padx=10, pady=10)
        ctk.CTkButton(frame_inputs, text="Explorar", command=self.seleccionar_destino).grid(row=1, column=2, padx=10,
                                                                                               pady=10)
        self.btn_comprimir = ctk.CTkButton(self.tab_rar, text="Comprimir RAR", height=40,
                                           font=("Arial", 14, "bold"), command=self.iniciar_compresion)
        self.btn_comprimir.pack(pady=30)

        self.label_estado_rar = ctk.CTkLabel(self.tab_rar, text="Esperando...", text_color="gray")
        self.label_estado_rar.pack()

    def construir_pestana_grabar(self):
        self.plan_origen = ctk.StringVar(value="")
        self.plan_destino = ctk.StringVar(value="")
        self.capacidad_seleccionada = ctk.StringVar(value="BD-R SL (25GB)")

        frame_rutas = ctk.CTkFrame(self.tab_grabar)
        frame_rutas.pack(padx=10 ,pady=10, fill="x")

        #Ruta de origen
        ctk.CTkLabel(frame_rutas, text="Carpeta origen:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkEntry(frame_rutas, textvariable=self.plan_origen, width=350).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(frame_rutas, text="Explorar", command=self.seleccionar_prebuffer).grid(row=0, column=2,
                                                                                          padx=5, pady=5)
        #Ruta de buffer
        ctk.CTkLabel(frame_rutas, text="Carpeta Buffer (Grabación)").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkEntry(frame_rutas, textvariable=self.plan_destino, width=350).grid(row=1, column=1, padx=5, pady=5)
        ctk.CTkButton(frame_rutas, text="Explorar",command=self.seleccionar_buffer).grid(row=1, column=2,
                                                                                                     padx=5, pady=5)
        ctk.CTkOptionMenu(frame_rutas, values=list(CAPACIDADES_BD.keys()), variable=self.capacidad_seleccionada,
                          command=lambda x: self.actualizar_listas()).grid(row=2, column=1, padx=5,
                                                                           pady=10, sticky="w")
        ctk.CTkButton(frame_rutas, text="Cargar Carpetas", fg_color="green",
                      command=self.actualizar_listas).grid(row=2, column=2, padx=5, pady=10)

        self.label_tamano = ctk.CTkLabel(self.tab_grabar, text="0.00 GB / 23.30 GB", font=("Arial", 20, "bold"))
        self.label_tamano.pack(pady=5)
        self.barra_progreso = ctk.CTkProgressBar(self.tab_grabar, width=700)
        self.barra_progreso.pack(pady=5)
        self.barra_progreso.set(0)

        #zona de listas de archivos
        frame_listas = ctk.CTkFrame(self.tab_grabar, fg_color="transparent")
        frame_listas.pack(pady=10, padx=10, fill="both", expand=True)

        #lista de origen
        frame_izq = ctk.CTkFrame(frame_listas, fg_color="transparent")
        frame_izq.pack(side="left", fill="both", expand=True, padx=5)
        ctk.CTkLabel(frame_izq, text="Archivos de origen").pack()
        self.lista_origen = tk.Listbox(frame_izq, bg="#2b2b2b", fg="white",
                                       selectbackground="#1f538d", highlightthickness=0)
        self.lista_origen.pack(fill="both", expand=True, padx=5, pady=5)

        frame_centro = ctk.CTkFrame(frame_listas, fg_color="transparent")
        frame_centro.pack(side="left", padx=10)
        ctk.CTkButton(frame_centro, text="Mover al Buffer >>", command=self.mover_a_buffer).pack(pady=10)
        ctk.CTkButton(frame_centro, text="<< Devolver", command=self.mover_a_origen).pack(pady=10)

        #lista del buffer de grabacion
        frame_der = ctk.CTkFrame(frame_listas)
        frame_der.pack(side="left", padx=5, fill="both", expand=True)
        ctk.CTkLabel(frame_der, text="Archivos del buffer").pack()
        self.lista_buffer = tk.Listbox(frame_der, bg="#2b2b2b", fg="white",
                                       selectbackground="#1f538d", highlightthickness=0)
        self.lista_buffer.pack(fill="both", expand=True, padx=5, pady=5)

        #Boton imgburn
        self.btn_imgburn = ctk.CTkButton(self.tab_grabar, text="Abrir ImgBurn💿", font=("Arial", 16, "bold"),
                                         fg_color="#8B0000", hover_color="#A52A2A", command=self.lanzar_imgburn)
        self.btn_imgburn.pack(pady=10)

    def actualizar_listas(self):
        origen = self.plan_origen.get()
        destino = self.plan_destino.get()

        self.lista_origen.delete(0, tk.END)
        self.lista_buffer.delete(0, tk.END)

        lista_origen = backend.leer_archivos(origen)
        if lista_origen:
            for item in lista_origen:
                self.lista_origen.insert(tk.END, item)
        lista_destino = backend.leer_archivos(destino)
        if lista_destino:
            for item in lista_destino:
                self.lista_buffer.insert(tk.END, item)

        tamano_bytes = backend.calcular_capacidad_usada(destino)
        capacidad_max = CAPACIDADES_BD[self.capacidad_seleccionada.get()]

        self.label_tamano.configure(text=f"{(tamano_bytes / 1024**3):.2f} GB / {(capacidad_max / 1024**3):.2f} GB")
        porcentaje = tamano_bytes / capacidad_max
        if porcentaje > 1.0:
            self.barra_progreso.set(1.0)
            self.barra_progreso.configure(progress_color="red")
            self.label_tamano.configure(text_color="red")
        else:
            self.barra_progreso.set(porcentaje)
            self.barra_progreso.configure(progress_color="#1f538d")
            self.label_tamano.configure(text_color="white")

    def ejecutar_movimiento(self, lista_origen, ruta_origen_base, ruta_destino_base):
        seleccion = lista_origen.curselection()
        if not seleccion: return

        nombre_item = lista_origen.get(seleccion[0])
        ruta_origen = os.path.join(ruta_origen_base, nombre_item)
        ruta_destino = os.path.join(ruta_destino_base, nombre_item)

        exito = backend.mover_archivos(ruta_origen, ruta_destino)
        if exito:
            self.actualizar_listas()


    def mover_a_buffer(self):
        self.ejecutar_movimiento(self.lista_origen, self.plan_origen.get(), self.plan_destino.get())

    def mover_a_origen(self):
        self.ejecutar_movimiento(self.lista_buffer, self.plan_destino.get(), self.plan_origen.get())

    def lanzar_imgburn(self):
        backend.lanzar_img_burn()

    def construir_pestana_bbdd(self):
        frame_izq = ctk.CTkFrame(self.tab_bbdd)
        frame_izq.pack(fill="both", expand=True, padx=10, pady=10, side="left")

        frame_der =ctk.CTkScrollableFrame(self.tab_bbdd)
        frame_der.pack(fill="both", expand=True, padx=10, pady=10, side="right")
        #Busqueda
        ctk.CTkLabel(frame_izq, text="Buscador", font=("Arial", 18, "bold")).pack(pady=15)
        self.tipo_busqueda = ctk.StringVar(value="Archivos")
        ctk.CTkSegmentedButton(frame_izq, values=["Archivos", "RARs", "Discos"], variable=self.tipo_busqueda).pack(pady=5)
        self.entry_busqueda = ctk.CTkEntry(frame_izq, width=300, placeholder_text="Nombre a buscar...")
        self.entry_busqueda.pack(pady=10)

        ctk.CTkButton(frame_izq, text="Buscar", command=self.buscar_elemento_ui).pack(pady=5)

        self.caja_resultados = ctk.CTkTextbox(frame_izq, width=400, height=400)
        self.caja_resultados.pack(pady=10, padx=10, fill="both", expand=True)

        #Guardar disco bbdd
        ctk.CTkLabel(frame_der, text="Registrar nuevo disco💿", font=("Arial", 16, "bold")).pack(pady=(15, 5))

        self.bd_id = ctk.StringVar(value="BD-000")
        self.fecha_bd = ctk.StringVar(value="DD-MM-YYYY")
        self.bd_capacidad = ctk.StringVar(value="BD-R SL (25GB)")

        ctk.CTkEntry(frame_der, textvariable=self.bd_id, width=250, placeholder_text="BD-000").pack(pady=2)
        ctk.CTkEntry(frame_der, textvariable=self.fecha_bd, width=250, placeholder_text="DD-MM-YYYY").pack(pady=2)
        ctk.CTkOptionMenu(frame_der, values=list(CAPACIDADES_BD.keys()), variable=self.bd_capacidad).pack(pady=2)
        ctk.CTkButton(frame_der, text="Guardar disco", fg_color="green", command=self.guardar_disco).pack(pady=10)

        #Guardar directorios y rars
        ctk.CTkLabel(frame_der, text="Escanear carpeta📁", font=("Arial", 16, "bold")).pack(pady=25)
        self.ruta_escaneo = ctk.StringVar()
        self.id_bd_destino = ctk.StringVar()
        self.nombre_rar_destino = ctk.StringVar()

        frame_ruta = ctk.CTkFrame(frame_der, fg_color="transparent")
        frame_ruta.pack(pady=5)
        ctk.CTkEntry(frame_ruta, textvariable=self.ruta_escaneo, width=180).pack(padx=5, side="left")
        ctk.CTkButton(frame_ruta, text="Explorar", command=self.seleccionar_carpeta_escaneo).pack(side="left")

        ctk.CTkLabel(frame_der, text="¿A qué BD?").pack(pady=(5,0))
        ctk.CTkEntry(frame_der, textvariable=self.id_bd_destino, width=250, placeholder_text="BD-000").pack(pady=2)

        ctk.CTkLabel(frame_der, text="¿En qué RAR? (si aplica)").pack(pady=(5,0))
        ctk.CTkEntry(frame_der, textvariable=self.nombre_rar_destino, width=250,
                     placeholder_text="anything.rar").pack(pady=2)

        self.btn_archivos = ctk.CTkButton(frame_der, text="Registrar archivos originales", command=self.escanear_originales)
        self.btn_archivos.pack(pady=10)
        self.btn_rars = ctk.CTkButton(frame_der, text="Registrar RARs", command=self.escanear_rars, fg_color="#8B4513")
        self.btn_rars.pack(pady=5)

        self.label_estado_bd = ctk.CTkLabel(frame_der, text="")
        self.label_estado_bd.pack(pady=10)


    def buscar_elemento_ui(self):
        termino = self.entry_busqueda.get()
        tipo = self.tipo_busqueda.get()
        self.caja_resultados.delete("1.0", tk.END)
        if not termino:
            if tipo == "Discos":
                resultados = baseDatos.buscar_discos()
                if resultados:
                    self.caja_resultados.insert(tk.END, "--- INVENTARIO DE TODOS LOS DISCOS ---\n")
                    for fila in resultados:
                        self.caja_resultados.insert(tk.END, f"💿 {fila[0]} | 📅 {fila[1]} | 💾 {fila[2]}\n")
                    self.caja_resultados.insert(tk.END, "-" * 40 + "\n")
                else:
                    self.caja_resultados.insert(tk.END, "La base de datos de discos está vacía.")
            else:
                self.caja_resultados.insert(tk.END, "Escribe algo para buscar brotha")
                return
        if tipo == "Archivos":
            resultados = baseDatos.buscar_archivo(termino)
            resultados_disco = baseDatos.buscar_archivos_disco(termino)
            if resultados:
                for fila in resultados:
                    texto = f"📄 Archivo: {fila[1]}\n📦 Contenedor RAR: {fila[2]}\n💿 Disco: {fila[3]}\n{'-' * 40}\n"
                    self.caja_resultados.insert(tk.END, texto)
            elif resultados_disco:
                self.caja_resultados.insert(tk.END, f"--- Listado completo de archivos en '{termino}' ---\n")
                self.caja_resultados.insert(tk.END, f"Total: {len(resultados_disco)} archivos.\n\n")
                for fila in resultados_disco:
                    contenedor = f"(En RAR: {fila[2]})" if fila[2] else "(Suelto o en carpeta)"
                    self.caja_resultados.insert(tk.END, f"📄 {fila[1]} {contenedor}\n")
                self.caja_resultados.insert(tk.END, f"\n{'-' * 40}\n")
            else:
                self.caja_resultados.insert(tk.END, f"No se encontró el archivo '{termino}'.")
        elif tipo == "RARs":
            resultados = baseDatos.buscar_rar(termino)
            resultados_disco = baseDatos.buscar_rars_disco(termino)
            if resultados:
                for fila in resultados:
                    texto = f"📦 RAR: {fila[1]}\n💿 Disco: {fila[3]}\n🔐 Hash: {fila[2]}\n{'-' * 40}\n"
                    self.caja_resultados.insert(tk.END, texto)
            elif resultados_disco:
                self.caja_resultados.insert(tk.END, f"--- Listado completo de RARs en '{termino}' ---\n")
                self.caja_resultados.insert(tk.END, f"Total: {len(resultados_disco)} RARs.\n\n")
                for fila in resultados_disco:
                    self.caja_resultados.insert(tk.END, f"📦 {fila[1]}\n   🔐 Hash: {fila[2]}\n")
                self.caja_resultados.insert(tk.END, f"\n{'-' * 40}\n")
            else:
                self.caja_resultados.insert(tk.END, f"No se encontró el RAR '{termino}'.")
        elif tipo == "Discos":
            resultados = baseDatos.buscar_disco(termino)
            if resultados:
                for fila in resultados:
                    id_disco = fila[0]
                    texto = f"💿 ID Disco: {fila[0]}\n📅 Fecha de Grabación: {fila[1]}\n💾 Capacidad: {fila[2]}\n{'-' * 40}\n"
                    rars_en_disco = baseDatos.buscar_rars_disco(id_disco)
                    archivos_en_disco = baseDatos.buscar_archivos_disco(id_disco)
                    texto += f"📊 RESUMEN DE CONTENIDO:\n"
                    texto += f"Contiene {len(rars_en_disco)} archivos RAR y {len(archivos_en_disco)} archivos sueltos.\n\n"
                    if rars_en_disco:
                        texto += "📦 ARCHIVOS RAR:\n"
                        for r in rars_en_disco:
                            texto += f"  - {r[1]}\n"

                    if archivos_en_disco:
                        texto += "\n📄 ARCHIVOS INDEXADOS (Muestra):\n"
                        # Si hay 10.000 fotos, mostramos solo las 15 primeras para no colgar la interfaz
                        for a in archivos_en_disco[:15]:
                            contenedor = f"(En RAR: {a[2]})" if a[2] else "(Suelto o en carpeta)"
                            texto += f"  - {a[1]} {contenedor}\n"

                        if len(archivos_en_disco) > 15:
                            texto += f"  ... y {len(archivos_en_disco) - 15} archivos más.\n"

                    texto += f"\n{'-' * 40}\n"
                    self.caja_resultados.insert(tk.END, texto)
            else:
                self.caja_resultados.insert(tk.END, f"No se encontró ningún disco con el ID '{termino}'.")

    def guardar_disco(self):
        id_disco = self.bd_id.get()
        if id_disco:
            try:
                baseDatos.crear_disco(id_disco, self.bd_capacidad.get(), self.fecha_bd.get())
                self.label_estado_bd.configure(text=f"Disco {id_disco} registrado.", text_color="green")
            except Exception as e:
                self.label_estado_bd.configure(text=f"Error BBDD: {e}", text_color="red")
        else:
            self.label_estado_bd.configure(text="Falta el ID del disco.", text_color="orange")

    def escanear_originales(self):
        ruta = self.ruta_escaneo.get()
        id_disco = self.id_bd_destino.get()
        nombre_rar = self.nombre_rar_destino.get()
        if not ruta or not id_disco:
            self.label_estado_bd.configure(text="Selecciona ruta y un ID de Disco destino.", text_color="red")
            return

        archivos_enc = backend.escanear_para_archivo(ruta)

        try:
            for archivo in archivos_enc:
                if not archivo.lower().endswith(".rar"):
                    baseDatos.crear_archivo_disco(archivo, id_disco)

                    if nombre_rar:
                        baseDatos.adjuntar_nombre_rar_a_archivo(nombre_rar, archivo)

                    self.label_estado_bd.configure(text=f"{len(archivos_enc)} archivos indexados con éxito.",
                                           text_color="green")

        except Exception as e:
            self.label_estado_bd.configure(text=f"Error BBDD: {e}", text_color="red")


    def escanear_rars(self):
        ruta = self.ruta_escaneo.get()
        id_disco = self.id_bd_destino.get()

        if not ruta or not id_disco:
            self.label_estado_bd.configure(text="Selecciona ruta y un ID de Disco destino.", text_color="red")
            return

        self.btn_archivos.configure(state="disabled")
        self.btn_rars.configure(state="disabled")
        self.label_estado_bd.configure(text="Procesando RARs... (La interfaz podría pausarse por el cálculo de Hashes)",
                                       text_color="orange")

        hilo = threading.Thread(target=self.hilo_hash_rars, args=(ruta, id_disco))
        hilo.start()


    def hilo_hash_rars(self, ruta, id_disco):
        archivos_encontrados = backend.escanear_para_archivo(ruta)
        rars_procesados = 0
        try:
            for archivo in archivos_encontrados:
                if archivo.lower().endswith(".rar"):
                    baseDatos.crear_rar_disco(archivo, id_disco)
                    ruta_completa = os.path.join(ruta, archivo)

                    hash_calculado = backend.calcular_hash_rar(ruta_completa)

                    baseDatos.adjuntar_hash_a_rar(hash_calculado, archivo)
                    rars_procesados += 1
                    self.label_estado_bd.configure(text=f"¡Éxito! {rars_procesados} RARs registrados.",
                                                   text_color="green")
        except Exception as e:
            self.label_estado_bd.configure(text=f"Error BBDD: {e}", text_color="red")
        finally:
            self.btn_archivos.configure(state="normal")
            self.btn_rars.configure(state="normal")


    def seleccionar_buffer(self):
        ruta = filedialog.askdirectory(title="Selecciona la carpeta de buffer")
        if ruta: self.plan_destino.set(ruta)
    def seleccionar_prebuffer(self):
        ruta = filedialog.askdirectory(title="Selecciona la carpeta de prebuffer")
        if ruta: self.plan_origen.set(ruta)

    def seleccionar_carpeta_escaneo(self):
        ruta = filedialog.askdirectory(title="Selecciona la carpeta a escanear")
        if ruta: self.ruta_escaneo.set(ruta)

    def seleccionar_origen(self):
        ruta = filedialog.askdirectory(title="Selecciona la carpeta de origen")
        if ruta: self.ruta_origen.set(ruta)

    def seleccionar_destino(self):
        ruta = filedialog.asksaveasfilename(title="Guardar RAR como",
                                            defaultextension=".rar",
                                            filetypes=[("RAR files", ".rar")])
        if ruta: self.ruta_destino.set(ruta)

    def iniciar_compresion(self):
        self.btn_comprimir.configure(state="disabled")
        self.label_estado_rar.configure(text="Comprimiendo de fondo... Puedes ir a la otra pestaña.",
                                        text_color="orange")
        origen = self.ruta_origen.get()
        destino = self.ruta_destino.get()

        hilo = threading.Thread(target=self.hilo_comprimir, args=(origen, destino))
        hilo.start()

    def hilo_comprimir(self, origen, destino):
        try:
            backend.generar_rar(origen, destino)
            self.label_estado_rar.configure(text="Compresion finalizada.")
        except Exception as e:
            self.label_estado_rar.configure(text=f"Error: {e}", text_color="red")
        finally:
            self.btn_comprimir.configure(state="normal")

if __name__ == '__main__':
    baseDatos.inicializar()
    app = GestorPreservacion()
    app.mainloop()