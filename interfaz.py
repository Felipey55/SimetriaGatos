import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from procesamiento_imagenes import ProcesadorImagenes

class InterfazSimetriaGatos:
    """
    Interfaz gráfica para el análisis de simetría en gatos.
    Permite seleccionar imágenes, visualizar el proceso de tratamiento y mostrar resultados.
    Incluye un menú navegable para facilitar el acceso a las diferentes secciones.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Simetría en Gatos")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        # Hacer que la ventana sea maximizada por defecto
        self.root.state('zoomed')
        
        # Inicializar el procesador de imágenes
        self.procesador = ProcesadorImagenes()
        
        # Directorio de imágenes
        self.dir_imagenes = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
        
        # Variables para almacenar imágenes y resultados
        self.imagen_seleccionada = None
        self.resultados_procesamiento = None
        self.miniaturas = []
        
        # Crear la interfaz
        self.crear_interfaz()
        
        # Crear encabezado
        self.crear_encabezado()
        
        # Cargar miniaturas de imágenes
        self.cargar_miniaturas()
    
    def crear_interfaz(self):
        """
        Crea la estructura de la interfaz gráfica con menú navegable.
        """
        # Configurar estilos
        self.configurar_estilos()
        
        # Crear menú de navegación
        self.crear_menu_navegacion()
        
        # Crear contenedor principal para las pestañas
        self.contenedor_principal = ttk.Frame(self.root)
        self.contenedor_principal.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        # Configurar el contenedor principal para que se expanda
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.contenedor_principal.grid_rowconfigure(0, weight=1)
        self.contenedor_principal.grid_columnconfigure(0, weight=1)
        
        # Crear frames para cada sección
        self.crear_seccion_repositorio()
        self.crear_seccion_imagen_seleccionada()
        self.crear_seccion_proceso()
        self.crear_seccion_analisis()
        
        # Mostrar la sección de repositorio por defecto
        self.mostrar_seccion("repositorio")
    
    def configurar_estilos(self):
        """
        Configura los estilos para la interfaz.
        """
        estilo = ttk.Style()
        estilo.configure("TFrame", background="#f0f0f0")
        estilo.configure("Card.TFrame", background="#ffffff", relief="raised")
        estilo.configure("TNotebook", background="#f0f0f0")
        estilo.configure("TNotebook.Tab", background="#e0e0e0", padding=[10, 5], font=("Arial", 10))
        estilo.map("TNotebook.Tab", background=[('selected', '#ffffff')])
        estilo.configure("Boton.TButton", font=("Arial", 10), padding=5)
        
    def crear_menu_navegacion(self):
        """
        Crea el menú de navegación con pestañas.
        """
        # Frame para el menú de navegación
        menu_frame = ttk.Frame(self.root)
        menu_frame.pack(fill=tk.X, padx=0, pady=0)
        
        # Botones de navegación
        self.botones_menu = {}
        
        # Definir secciones del menú
        secciones = [
            ("repositorio", "Repositorio de Imágenes"),
            ("imagen", "Imagen Seleccionada"),
            ("proceso", "Proceso de Tratamiento"),
            ("analisis", "Análisis de Simetría")
        ]
        
        # Crear botones para cada sección
        for i, (seccion_id, texto) in enumerate(secciones):
            btn = ttk.Button(menu_frame, text=texto, style="Boton.TButton",
                           command=lambda s=seccion_id: self.mostrar_seccion(s))
            btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.botones_menu[seccion_id] = btn
    
    def mostrar_seccion(self, seccion):
        """
        Muestra la sección seleccionada y oculta las demás.
        
        Args:
            seccion (str): Identificador de la sección a mostrar.
        """
        # Ocultar todas las secciones
        self.frame_repositorio.pack_forget()
        self.frame_imagen_seleccionada.pack_forget()
        self.frame_proceso.pack_forget()
        self.frame_analisis.pack_forget()
        
        # Mostrar la sección seleccionada y ajustarla para ocupar todo el espacio
        if seccion == "repositorio":
            self.frame_repositorio.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        elif seccion == "imagen":
            self.frame_imagen_seleccionada.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        elif seccion == "proceso":
            self.frame_proceso.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        elif seccion == "analisis":
            self.frame_analisis.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
    
    def crear_encabezado(self):
        """
        Crea un encabezado con título y botones de acción.
        """
        header_frame = ttk.Frame(self.root, style="TFrame")
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        # Título principal
        ttk.Label(header_frame, text="Análisis de Simetría en Gatos", 
                 font=("Arial", 18, "bold"), background="#f0f0f0").pack(side=tk.LEFT, pady=5)
        
        # Botones de acción
        btn_frame = ttk.Frame(header_frame, style="TFrame")
        btn_frame.pack(side=tk.RIGHT, pady=5)
        
        # Botón para recargar imágenes
        ttk.Button(btn_frame, text="Recargar Imágenes", style="Boton.TButton",
                  command=self.recargar_imagenes).pack(side=tk.RIGHT, padx=5)
    
    def recargar_imagenes(self):
        """
        Recarga las imágenes del repositorio.
        """
        self.cargar_miniaturas()
        self.mostrar_seccion("repositorio")
        
    def crear_seccion_repositorio(self):
        """
        Crea la sección del repositorio de imágenes.
        """
        self.frame_repositorio = ttk.Frame(self.contenedor_principal, style="Card.TFrame")
        
        # Título de la sección
        titulo_frame = ttk.Frame(self.frame_repositorio, style="Card.TFrame")
        titulo_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(titulo_frame, text="Repositorio de Imágenes", 
                 font=("Arial", 16, "bold"), background="#ffffff").pack(side=tk.LEFT, padx=10)
        
        # Canvas para mostrar miniaturas con scrollbar
        self.canvas_frame = ttk.Frame(self.frame_repositorio)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Configurar el canvas_frame para que se expanda
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Configurar el canvas para que ocupe todo el espacio
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.canvas.winfo_width())
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Hacer que el canvas se expanda con la ventana
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Actualizar el ancho del scrollable_frame cuando cambie el tamaño del canvas
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(
            self.canvas.find_withtag('all')[0], width=e.width))
    
    def crear_seccion_imagen_seleccionada(self):
        """
        Crea la sección de la imagen seleccionada.
        """
        self.frame_imagen_seleccionada = ttk.Frame(self.contenedor_principal, style="Card.TFrame")
        
        # Título de la sección
        titulo_frame = ttk.Frame(self.frame_imagen_seleccionada, style="Card.TFrame")
        titulo_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(titulo_frame, text="Imagen Seleccionada", 
                 font=("Arial", 16, "bold"), background="#ffffff").pack(side=tk.LEFT, padx=10)
        
        # Botones de navegación
        botones_frame = ttk.Frame(titulo_frame, style="Card.TFrame")
        botones_frame.pack(side=tk.RIGHT, padx=10)
        
        ttk.Button(botones_frame, text="Ver Repositorio", style="Boton.TButton",
                  command=lambda: self.mostrar_seccion("repositorio")).pack(side=tk.LEFT, padx=5)
        
        # Frame para mostrar la imagen seleccionada
        self.imagen_frame = ttk.Frame(self.frame_imagen_seleccionada)
        self.imagen_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Configurar el frame para que se expanda
        self.frame_imagen_seleccionada.grid_rowconfigure(0, weight=1)
        self.frame_imagen_seleccionada.grid_columnconfigure(0, weight=1)
        self.imagen_frame.grid_rowconfigure(0, weight=1)
        self.imagen_frame.grid_columnconfigure(0, weight=1)
        
        # Mensaje inicial
        ttk.Label(self.imagen_frame, text="No hay imagen seleccionada", 
                 font=("Arial", 12), foreground="#888888").pack(pady=50)
    
    def crear_seccion_proceso(self):
        """
        Crea la sección del proceso de tratamiento.
        """
        self.frame_proceso = ttk.Frame(self.contenedor_principal, style="Card.TFrame")
        
        # Título de la sección
        titulo_frame = ttk.Frame(self.frame_proceso, style="Card.TFrame")
        titulo_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(titulo_frame, text="Proceso de Tratamiento", 
                 font=("Arial", 16, "bold"), background="#ffffff").pack(side=tk.LEFT, padx=10)
        
        # Botones de navegación
        botones_frame = ttk.Frame(titulo_frame, style="Card.TFrame")
        botones_frame.pack(side=tk.RIGHT, padx=10)
        
        ttk.Button(botones_frame, text="Ver Imagen", style="Boton.TButton",
                  command=lambda: self.mostrar_seccion("imagen")).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Ver Análisis", style="Boton.TButton",
                  command=lambda: self.mostrar_seccion("analisis")).pack(side=tk.LEFT, padx=5)
        
        # Frame para mostrar las imágenes del proceso
        self.proceso_frame = ttk.Frame(self.frame_proceso)
        self.proceso_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Configurar el frame para que se expanda
        self.frame_proceso.grid_rowconfigure(0, weight=1)
        self.frame_proceso.grid_columnconfigure(0, weight=1)
        self.proceso_frame.grid_rowconfigure(0, weight=1)
        self.proceso_frame.grid_columnconfigure(0, weight=1)
        
        # Mensaje inicial
        ttk.Label(self.proceso_frame, text="No hay imagen procesada", 
                 font=("Arial", 12), foreground="#888888").pack(pady=50)
    
    def crear_seccion_analisis(self):
        """
        Crea la sección del análisis de simetría.
        """
        self.frame_analisis = ttk.Frame(self.contenedor_principal, style="Card.TFrame")
        
        # Título de la sección
        titulo_frame = ttk.Frame(self.frame_analisis, style="Card.TFrame")
        titulo_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(titulo_frame, text="Análisis de Simetría", 
                 font=("Arial", 16, "bold"), background="#ffffff").pack(side=tk.LEFT, padx=10)
        
        # Botones de navegación
        botones_frame = ttk.Frame(titulo_frame, style="Card.TFrame")
        botones_frame.pack(side=tk.RIGHT, padx=10)
        
        ttk.Button(botones_frame, text="Ver Imagen", style="Boton.TButton",
                  command=lambda: self.mostrar_seccion("imagen")).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Ver Proceso", style="Boton.TButton",
                  command=lambda: self.mostrar_seccion("proceso")).pack(side=tk.LEFT, padx=5)
        
        # Frame para mostrar el resultado de simetría
        self.resultado_frame = ttk.Frame(self.frame_analisis)
        self.resultado_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Configurar el frame para que se expanda
        self.frame_analisis.grid_rowconfigure(0, weight=1)
        self.frame_analisis.grid_columnconfigure(0, weight=1)
        self.resultado_frame.grid_rowconfigure(0, weight=1)
        self.resultado_frame.grid_columnconfigure(0, weight=1)
        
        # Mensaje inicial
        ttk.Label(self.resultado_frame, text="No hay análisis de simetría", 
                 font=("Arial", 12), foreground="#888888").pack(pady=50)
    
    def cargar_miniaturas(self):
        """
        Carga las miniaturas de todas las imágenes en la carpeta img.
        """
        # Limpiar miniaturas anteriores
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.miniaturas = []
        
        # Verificar si el directorio existe
        if not os.path.exists(self.dir_imagenes):
            ttk.Label(self.scrollable_frame, text="Carpeta 'img' no encontrada", foreground="red").pack(pady=10)
            return
        
        # Obtener lista de archivos de imagen
        archivos_imagen = [f for f in os.listdir(self.dir_imagenes) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        
        if not archivos_imagen:
            ttk.Label(self.scrollable_frame, text="No se encontraron imágenes", foreground="red").pack(pady=10)
            return
        
        # Título informativo
        ttk.Label(self.scrollable_frame, text=f"Se encontraron {len(archivos_imagen)} imágenes", 
                 font=("Arial", 10), background="#f0f0f0").pack(pady=(0, 10))
        
        # Crear un contenedor grid para las miniaturas
        grid_frame = ttk.Frame(self.scrollable_frame)
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        grid_frame.grid_columnconfigure(tuple(range(4)), weight=1)  # 4 columnas con peso igual
        
        # Cargar y mostrar miniaturas en grid
        row = 0
        col = 0
        for archivo in archivos_imagen:
            # Frame para cada miniatura
            thumb_frame = ttk.Frame(grid_frame, style="Card.TFrame")
            thumb_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            # Configurar el thumb_frame para expandirse
            thumb_frame.grid_columnconfigure(0, weight=1)
            thumb_frame.grid_rowconfigure(0, weight=1)
            
            # Actualizar índices de grid
            col += 1
            if col >= 4:  # 4 miniaturas por fila
                col = 0
                row += 1
            
            # Cargar imagen y crear miniatura
            ruta_completa = os.path.join(self.dir_imagenes, archivo)
            try:
                # Usar PIL para crear miniatura
                img = Image.open(ruta_completa)
                img.thumbnail((300, 300))  # Redimensionar a 300x300 para miniaturas más grandes
                img_tk = ImageTk.PhotoImage(img)
                
                # Guardar referencia para evitar que sea eliminada por el recolector de basura
                self.miniaturas.append(img_tk)
                
                # Crear botón con la miniatura
                btn = tk.Button(thumb_frame, image=img_tk, bd=0,
                               command=lambda ruta=ruta_completa: self.seleccionar_imagen(ruta))
                btn.pack(padx=5, pady=5)
                
                # Etiqueta con el nombre del archivo
                nombre_corto = archivo if len(archivo) < 15 else archivo[:12] + "..."
                ttk.Label(thumb_frame, text=nombre_corto, background="#ffffff").pack(pady=(0, 5))
                
            except Exception as e:
                print(f"Error al cargar {archivo}: {e}")
        
        # Añadir instrucciones al final
        instrucciones_frame = ttk.Frame(self.scrollable_frame)
        instrucciones_frame.pack(fill=tk.X, padx=5, pady=15)
        
        ttk.Label(instrucciones_frame, text="Haga clic en una imagen para analizarla", 
                 font=("Arial", 10, "italic"), foreground="#555555").pack(pady=5)
    
    def seleccionar_imagen(self, ruta_imagen):
        """
        Maneja la selección de una imagen y procesa la imagen seleccionada.
        
        Args:
            ruta_imagen (str): Ruta de la imagen seleccionada.
        """
        self.imagen_seleccionada = ruta_imagen
        
        # Limpiar secciones anteriores
        for widget in self.imagen_frame.winfo_children():
            widget.destroy()
        
        # Mostrar la imagen seleccionada en la sección correspondiente
        try:
            # Cargar y mostrar la imagen seleccionada
            img = Image.open(ruta_imagen)
            img.thumbnail((1200, 1200))  # Redimensionar para una visualización más grande
            img_tk = ImageTk.PhotoImage(img)
            
            # Guardar referencia para evitar que sea eliminada por el recolector de basura
            self.imagen_actual = img_tk
            
            # Mostrar imagen
            lbl_img = ttk.Label(self.imagen_frame, image=img_tk, background="#ffffff")
            lbl_img.pack(pady=10)
            
            # Mostrar información de la imagen
            nombre_archivo = os.path.basename(ruta_imagen)
            ttk.Label(self.imagen_frame, text=f"Archivo: {nombre_archivo}", 
                     font=("Arial", 12), background="#ffffff").pack(pady=5)
            
            # Procesar la imagen
            self.resultados_procesamiento = self.procesador.procesar_imagen_completa(ruta_imagen)
            
            # Mostrar resultados del proceso
            self.mostrar_proceso()
            
            # Mostrar resultados de simetría
            self.mostrar_resultado_simetria()
            
            # Cambiar a la sección de imagen seleccionada
            self.mostrar_seccion("imagen")
            
        except Exception as e:
            # Mostrar mensaje de error
            ttk.Label(self.imagen_frame, text=f"Error al procesar la imagen: {str(e)}", 
                     foreground="red").pack(pady=20)
            
            # Limpiar otras secciones
            for widget in self.proceso_frame.winfo_children():
                widget.destroy()
            for widget in self.resultado_frame.winfo_children():
                widget.destroy()
                
            ttk.Label(self.proceso_frame, text=f"Error al procesar la imagen: {str(e)}", 
                     foreground="red").pack(pady=20)
            ttk.Label(self.resultado_frame, text=f"Error al procesar la imagen: {str(e)}", 
                     foreground="red").pack(pady=20)
    
    def mostrar_proceso(self):
        """
        Muestra las imágenes del proceso de tratamiento.
        """
        # Limpiar frame anterior
        for widget in self.proceso_frame.winfo_children():
            widget.destroy()
        
        if not self.resultados_procesamiento:
            ttk.Label(self.proceso_frame, text="No hay imagen procesada", 
                     font=("Arial", 12), foreground="#888888").pack(pady=50)
            return
        
        # Configurar el frame principal para ser responsive
        self.proceso_frame.grid_columnconfigure(0, weight=1)
        self.proceso_frame.grid_rowconfigure(0, weight=1)
        
        # Crear canvas con scrollbar para el contenido
        canvas = tk.Canvas(self.proceso_frame, bg="#ffffff")
        scrollbar = ttk.Scrollbar(self.proceso_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # Configurar el scrollable frame
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Configurar grid del canvas y scrollbar
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Crear ventana en el canvas
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Configurar el grid del scrollable frame para 3 columnas
        for i in range(3):
            scrollable_frame.grid_columnconfigure(i, weight=1)
        
        # Definir las imágenes a mostrar en el proceso
        imagenes_proceso = [
            ('Original', 'cara_gato'),
            ('Filtro Gaussiano', 'filtro_gaussiano'),
            ('Detección de Contornos', 'contornos_laplaciano'),
            ('Análisis de Gradiente', 'magnitud_gradiente'),
            ('Filtro Bilateral', 'filtro_bilateral'),
            ('Filtro de Orden Estático', 'filtro_mediana'),
            ('Filtro High Boost', 'filtro_highboost')
        ]
        
        # Crear grid de imágenes
        for i, (titulo, clave) in enumerate(imagenes_proceso):
            # Calcular posición en el grid (3 columnas)
            fila = i // 3
            columna = i % 3
            
            # Frame para cada imagen
            imagen_frame = ttk.Frame(scrollable_frame, style="Card.TFrame")
            imagen_frame.grid(row=fila, column=columna, padx=5, pady=5, sticky="nsew")
            
            # Título de la imagen
            ttk.Label(imagen_frame, text=titulo, 
                     font=("Arial", 11, "bold"), background="#ffffff").pack(pady=3)
            
            # Convertir y redimensionar imagen
            img = cv2.cvtColor(self.resultados_procesamiento[clave], cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img)
            
            # Calcular tamaño manteniendo proporción
            ancho_deseado = 400  # Reducir el ancho para que quepan 3 imágenes
            ratio = ancho_deseado / img.shape[1]
            nuevo_alto = int(img.shape[0] * ratio)
            
            img_pil = img_pil.resize((ancho_deseado, nuevo_alto), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_pil)
            
            # Guardar referencia para evitar que el recolector de basura la elimine
            imagen_frame.image = img_tk
            
            # Mostrar imagen
            label_imagen = ttk.Label(imagen_frame, image=img_tk)
            label_imagen.pack(pady=5)
        
        # Botones de navegación en la parte inferior
        botones_frame = ttk.Frame(self.proceso_frame)
        botones_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(botones_frame, text="Ver Imagen", style="Boton.TButton",
                  command=lambda: self.mostrar_seccion("imagen")).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Ver Análisis", style="Boton.TButton",
                  command=lambda: self.mostrar_seccion("analisis")).pack(side=tk.LEFT, padx=5)
        
        # Ajustar el ancho del canvas window cuando se redimensiona
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind('<Configure>', on_canvas_configure)
    
    def mostrar_resultado_simetria(self):
        """
        Muestra el resultado del análisis de simetría con una imagen que ocupa el máximo espacio posible
        y un scrollbar para poder desplazarse verticalmente.
        """
        # Limpiar frame anterior
        for widget in self.resultado_frame.winfo_children():
            widget.destroy()
        
        if not self.resultados_procesamiento:
            ttk.Label(self.resultado_frame, text="No hay análisis de simetría", 
                     font=("Arial", 12), foreground="#888888").pack(pady=50)
            return
            
        # Crear un canvas con scrollbar para contener todo el contenido
        main_canvas = tk.Canvas(self.resultado_frame)
        scrollbar = ttk.Scrollbar(self.resultado_frame, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)
        
        # Configurar el canvas para que se pueda hacer scroll
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(
                scrollregion=main_canvas.bbox("all")
            )
        )
        
        # Crear ventana dentro del canvas
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar el canvas y scrollbar
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Crear figura para mostrar el resultado de simetría que ocupe el máximo espacio disponible
        fig = plt.Figure(figsize=(16, 12), dpi=100)  # Ajustar dimensiones para maximizar visualización
        fig.subplots_adjust(hspace=0.1, wspace=0.05, left=0.01, right=0.99, top=0.95, bottom=0.05)  # Usar todo el espacio disponible
        
        # Imagen con línea de simetría ocupando el máximo espacio horizontal disponible
        fig = plt.figure(figsize=(15, 8))  # Ajustar tamaño de la figura
        ax1 = fig.add_subplot(1, 1, 1)  # Cambiar a un solo gráfico que ocupe todo el espacio
        img_simetria = cv2.cvtColor(self.resultados_procesamiento['imagen_simetria'], cv2.COLOR_BGR2RGB)
        ax1.imshow(img_simetria)  # Quitar aspect='equal' para permitir estirar la imagen
        ax1.set_title('Línea de Simetría', pad=20, fontsize=14, fontweight='bold')
        ax1.axis('off')
        
        # Mostrar las mitades en una ventana separada o pestaña para que no afecten al tamaño 
        # de la imagen principal y se puedan mostrar independientemente
        
        # Guardar las mitades para mostrarlas cuando se solicite
        self.mitad_izquierda = cv2.cvtColor(self.resultados_procesamiento['mitad_izquierda'], cv2.COLOR_BGR2RGB)
        self.mitad_derecha = cv2.cvtColor(self.resultados_procesamiento['mitad_derecha'], cv2.COLOR_BGR2RGB)
        
        # Puntuación de simetría
        puntuacion = self.resultados_procesamiento['puntuacion_simetria']
        
        # Determinar color y mensaje según puntuación
        if puntuacion >= 80:
            color = '#28a745'  # Verde más suave
            mensaje = 'Alta simetría'
        elif puntuacion >= 60:
            color = '#ffc107'  # Amarillo más suave
            mensaje = 'Simetría media'
        else:
            color = '#dc3545'  # Rojo más suave
            mensaje = 'Baja simetría'
        
        # Crear un frame para la puntuación con estilo
        puntuacion_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        puntuacion_frame.pack(fill=tk.X, padx=5, pady=(5, 5))
        
        # Mostrar puntuación con estilo mejorado
        ttk.Label(puntuacion_frame, 
                 text=f"Puntuación de Simetría: {puntuacion:.1f}%",
                 font=("Arial", 14), 
                 foreground=color,
                 background='#ffffff').pack(pady=(5, 0))
        
        ttk.Label(puntuacion_frame,
                 text=mensaje,
                 font=("Arial", 16, "bold"),
                 foreground=color,
                 background='#ffffff').pack(pady=(0, 5))
        
        # Mostrar la figura en el frame con mejor ajuste y ocupando todo el espacio disponible
        canvas = FigureCanvasTkAgg(fig, master=scrollable_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Añadir función para mostrar las mitades en una ventana separada
        def mostrar_mitades():
            ventana_mitades = tk.Toplevel(self.resultado_frame)
            ventana_mitades.title("Comparación de Mitades")
            ventana_mitades.geometry("800x400")  # Tamaño adecuado para las mitades
            
            # Crear figura para las mitades
            fig_mitades = plt.Figure(figsize=(12, 6), dpi=100)
            fig_mitades.subplots_adjust(wspace=0.05, left=0.01, right=0.99, top=0.9, bottom=0.1)
            
            # Mitad izquierda
            ax_izq = fig_mitades.add_subplot(1, 2, 1)
            ax_izq.imshow(self.mitad_izquierda)
            ax_izq.set_title('Mitad Izquierda', fontsize=14)
            ax_izq.axis('off')
            
            # Mitad derecha
            ax_der = fig_mitades.add_subplot(1, 2, 2)
            ax_der.imshow(self.mitad_derecha)
            ax_der.set_title('Mitad Derecha', fontsize=14)
            ax_der.axis('off')
            
            # Mostrar la figura en la ventana
            canvas_mitades = FigureCanvasTkAgg(fig_mitades, master=ventana_mitades)
            canvas_mitades.draw()
            canvas_mitades.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botones de navegación con estilo mejorado
        botones_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        botones_frame.pack(pady=10)
        
        ttk.Button(botones_frame, text="Ver Imagen Original", style="Boton.TButton",
                  command=lambda: self.mostrar_seccion("imagen")).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Ver Mitades", style="Boton.TButton",
                  command=mostrar_mitades).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Ver Proceso", style="Boton.TButton",
                  command=lambda: self.mostrar_seccion("proceso")).pack(side=tk.LEFT, padx=5)
                  
        # Asegurar que el scrollbar funciona correctamente
        scrollable_frame.update_idletasks()
        main_canvas.config(scrollregion=main_canvas.bbox("all"))
        
        # Vincular la rueda del ratón al scroll
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Para Windows/MacOS
        main_canvas.bind_all("<Button-4>", lambda e: main_canvas.yview_scroll(-1, "units"))  # Para Linux
        main_canvas.bind_all("<Button-5>", lambda e: main_canvas.yview_scroll(1, "units"))  # Para Linux

# Función principal para iniciar la aplicación
def main():
    root = tk.Tk()
    app = InterfazSimetriaGatos(root)
    root.mainloop()

if __name__ == "__main__":
    main()