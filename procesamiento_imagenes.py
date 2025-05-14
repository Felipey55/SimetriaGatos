import cv2
import numpy as np
import matplotlib.pyplot as plt

class ProcesadorImagenes:
    """
    Clase para el procesamiento de imágenes de gatos y análisis de simetría.
    Implementa varios filtros y técnicas de procesamiento de imágenes.
    """
    
    def __init__(self):
        # Cargar el clasificador para detección de caras de gatos
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalcatface.xml')
    
    def cargar_imagen(self, ruta_imagen):
        """
        Carga una imagen desde la ruta especificada.
        
        Args:
            ruta_imagen (str): Ruta de la imagen a cargar.
            
        Returns:
            numpy.ndarray: Imagen cargada en formato BGR.
        """
        imagen = cv2.imread(ruta_imagen)
        if imagen is None:
            raise ValueError(f"No se pudo cargar la imagen desde {ruta_imagen}")
        return imagen
    
    def detectar_cara_gato(self, imagen):
        """
        Detecta la cara del gato en la imagen, la centra y la acerca.
        
        Args:
            imagen (numpy.ndarray): Imagen en formato BGR.
            
        Returns:
            tuple: (imagen_procesada, imagen_original_con_rectangulo)
        """
        # Convertir a escala de grises para la detección
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        
        # Detectar caras de gatos
        caras = self.face_cascade.detectMultiScale(gris, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Crear una copia de la imagen original para dibujar el rectángulo
        imagen_con_rectangulo = imagen.copy()
        
        if len(caras) > 0:
            # Tomar la primera cara detectada
            x, y, w, h = caras[0]
            
            # Dibujar un rectángulo alrededor de la cara en la imagen original
            cv2.rectangle(imagen_con_rectangulo, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Extraer y agrandar la región de la cara (con un margen adicional)
            margen = int(0.2 * max(w, h))  # 20% de margen
            x_start = max(0, x - margen)
            y_start = max(0, y - margen)
            x_end = min(imagen.shape[1], x + w + margen)
            y_end = min(imagen.shape[0], y + h + margen)
            
            cara_recortada = imagen[y_start:y_end, x_start:x_end]
            
            # Redimensionar la cara para que sea más grande
            altura, ancho = cara_recortada.shape[:2]
            factor_escala = 2.0  # Hacer la cara 2 veces más grande
            cara_agrandada = cv2.resize(cara_recortada, (int(ancho * factor_escala), int(altura * factor_escala)))
            
            return cara_agrandada, imagen_con_rectangulo
        else:
            # Si no se detecta ninguna cara, devolver la imagen original
            print("No se detectó ninguna cara de gato en la imagen.")
            return imagen, imagen_con_rectangulo
    
    def aplicar_filtro_gaussiano(self, imagen, tamano_kernel=5, sigma=0):
        """
        Aplica un filtro gaussiano para suavizar la imagen.
        
        Args:
            imagen (numpy.ndarray): Imagen en formato BGR.
            tamano_kernel (int): Tamaño del kernel gaussiano (debe ser impar).
            sigma (float): Desviación estándar del kernel gaussiano.
            
        Returns:
            numpy.ndarray: Imagen con filtro gaussiano aplicado.
        """
        return cv2.GaussianBlur(imagen, (tamano_kernel, tamano_kernel), sigma)
    
    def detectar_contornos_laplaciano(self, imagen, tamano_kernel=3):
        """
        Detecta contornos usando el operador Laplaciano.
        
        Args:
            imagen (numpy.ndarray): Imagen en formato BGR.
            tamano_kernel (int): Tamaño del kernel para el Laplaciano.
            
        Returns:
            numpy.ndarray: Imagen con contornos detectados.
        """
        # Convertir a escala de grises si es necesario
        if len(imagen.shape) == 3:
            gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        else:
            gris = imagen
        
        # Aplicar filtro gaussiano para reducir ruido
        gris = cv2.GaussianBlur(gris, (3, 3), 0)
        
        # Aplicar operador Laplaciano
        laplaciano = cv2.Laplacian(gris, cv2.CV_64F, ksize=tamano_kernel)
        
        # Convertir a un rango adecuado para visualización
        laplaciano = np.uint8(np.absolute(laplaciano))
        
        # Normalizar para mejor visualización
        laplaciano_normalizado = cv2.normalize(laplaciano, None, 0, 255, cv2.NORM_MINMAX)
        
        return laplaciano_normalizado
    
    def analisis_gradiente(self, imagen):
        """
        Realiza análisis de gradiente usando los operadores Sobel.
        
        Args:
            imagen (numpy.ndarray): Imagen en formato BGR.
            
        Returns:
            tuple: (magnitud_gradiente, direccion_gradiente)
        """
        # Convertir a escala de grises si es necesario
        if len(imagen.shape) == 3:
            gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        else:
            gris = imagen
        
        # Calcular gradientes en x e y usando Sobel
        grad_x = cv2.Sobel(gris, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gris, cv2.CV_64F, 0, 1, ksize=3)
        
        # Calcular magnitud y dirección del gradiente
        magnitud = cv2.magnitude(grad_x, grad_y)
        direccion = cv2.phase(grad_x, grad_y, angleInDegrees=True)
        
        # Normalizar magnitud para visualización
        magnitud_norm = cv2.normalize(magnitud, None, 0, 255, cv2.NORM_MINMAX)
        magnitud_norm = np.uint8(magnitud_norm)
        
        return magnitud_norm, direccion
    
    def aplicar_filtro_bilateral(self, imagen, d=9, sigma_color=75, sigma_space=75):
        """
        Aplica un filtro bilateral para suavizar la imagen preservando bordes.
        
        Args:
            imagen (numpy.ndarray): Imagen en formato BGR.
            d (int): Diámetro de cada vecindad de píxeles.
            sigma_color (float): Sigma en el espacio de color.
            sigma_space (float): Sigma en el espacio de coordenadas.
            
        Returns:
            numpy.ndarray: Imagen con filtro bilateral aplicado.
        """
        return cv2.bilateralFilter(imagen, d, sigma_color, sigma_space)
    
    def aplicar_filtro_orden_estatico(self, imagen, tamano_kernel=3, tipo='mediana'):
        """
        Aplica un filtro de orden estático (mediana, mínimo o máximo).
        
        Args:
            imagen (numpy.ndarray): Imagen en formato BGR.
            tamano_kernel (int): Tamaño del kernel para el filtro.
            tipo (str): Tipo de filtro ('mediana', 'minimo', 'maximo').
            
        Returns:
            numpy.ndarray: Imagen con filtro de orden estático aplicado.
        """
        if tipo == 'mediana':
            return cv2.medianBlur(imagen, tamano_kernel)
        elif tipo == 'minimo':
            kernel = np.ones((tamano_kernel, tamano_kernel), np.uint8)
            return cv2.erode(imagen, kernel)
        elif tipo == 'maximo':
            kernel = np.ones((tamano_kernel, tamano_kernel), np.uint8)
            return cv2.dilate(imagen, kernel)
        else:
            raise ValueError("Tipo de filtro no válido. Opciones: 'mediana', 'minimo', 'maximo'")
    
    def aplicar_filtro_highboost(self, imagen, k=1.5):
        """
        Aplica un filtro de realce (High Boost) para mejorar detalles.
        
        Args:
            imagen (numpy.ndarray): Imagen en formato BGR.
            k (float): Factor de realce (k > 1).
            
        Returns:
            numpy.ndarray: Imagen con filtro high boost aplicado.
        """
        # Convertir a escala de grises si es necesario
        if len(imagen.shape) == 3:
            gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        else:
            gris = imagen
            imagen = cv2.cvtColor(gris, cv2.COLOR_GRAY2BGR)
        
        # Aplicar filtro gaussiano
        imagen_suavizada = cv2.GaussianBlur(gris, (5, 5), 0)
        
        # Calcular máscara de nitidez (imagen original - imagen suavizada)
        mascara = cv2.subtract(gris, imagen_suavizada)
        
        # Aplicar high boost: imagen original + k * máscara
        imagen_realzada = cv2.add(gris, cv2.multiply(mascara, k))
        
        # Normalizar resultado
        imagen_realzada = cv2.normalize(imagen_realzada, None, 0, 255, cv2.NORM_MINMAX)
        imagen_realzada = np.uint8(imagen_realzada)
        
        # Si la imagen original era a color, convertir el resultado a color
        if len(imagen.shape) == 3:
            imagen_realzada = cv2.cvtColor(imagen_realzada, cv2.COLOR_GRAY2BGR)
        
        return imagen_realzada
    
    def analizar_simetria(self, imagen):
        """
        Analiza la simetría vertical de la imagen del gato.
        
        Args:
            imagen (numpy.ndarray): Imagen en formato BGR.
            
        Returns:
            tuple: (imagen_con_linea_simetria, puntuacion_simetria, mitad_izquierda, mitad_derecha)
        """
        # Convertir a escala de grises si es necesario
        if len(imagen.shape) == 3:
            gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        else:
            gris = imagen
            imagen = cv2.cvtColor(gris, cv2.COLOR_GRAY2BGR)
        
        # Obtener dimensiones
        altura, ancho = gris.shape
        
        # Encontrar la línea central
        linea_central = ancho // 2
        
        # Dividir la imagen en mitad izquierda y derecha
        mitad_izquierda = gris[:, :linea_central]
        mitad_derecha = gris[:, linea_central:]
        
        # Voltear horizontalmente la mitad derecha para comparar con la izquierda
        mitad_derecha_volteada = cv2.flip(mitad_derecha, 1)
        
        # Redimensionar si las mitades tienen diferentes tamaños
        if mitad_izquierda.shape[1] != mitad_derecha_volteada.shape[1]:
            min_ancho = min(mitad_izquierda.shape[1], mitad_derecha_volteada.shape[1])
            mitad_izquierda = mitad_izquierda[:, :min_ancho]
            mitad_derecha_volteada = mitad_derecha_volteada[:, :min_ancho]
        
        # Calcular la diferencia absoluta entre las dos mitades
        diferencia = cv2.absdiff(mitad_izquierda, mitad_derecha_volteada)
        
        # Calcular puntuación de simetría (0 = perfectamente simétrico, valores mayores = menos simétrico)
        puntuacion_simetria = np.mean(diferencia)
        
        # Normalizar puntuación a un porcentaje (100% = perfectamente simétrico)
        puntuacion_simetria_porcentaje = max(0, 100 - (puntuacion_simetria / 2.55))
        
        # Crear imagen con línea de simetría
        imagen_con_linea = imagen.copy()
        cv2.line(imagen_con_linea, (linea_central, 0), (linea_central, altura), (0, 255, 0), 2)
        
        # Añadir texto con la puntuación de simetría
        texto = f"Simetria: {puntuacion_simetria_porcentaje:.1f}%"
        cv2.putText(imagen_con_linea, texto, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Crear imágenes a color para las mitades
        mitad_izquierda_color = cv2.cvtColor(mitad_izquierda, cv2.COLOR_GRAY2BGR)
        mitad_derecha_color = cv2.cvtColor(mitad_derecha, cv2.COLOR_GRAY2BGR)
        
        return imagen_con_linea, puntuacion_simetria_porcentaje, mitad_izquierda_color, mitad_derecha_color
    
    def procesar_imagen_completa(self, ruta_imagen):
        """
        Procesa una imagen aplicando todos los filtros y análisis.
        
        Args:
            ruta_imagen (str): Ruta de la imagen a procesar.
            
        Returns:
            dict: Diccionario con todas las imágenes procesadas.
        """
        # Cargar imagen
        imagen_original = self.cargar_imagen(ruta_imagen)
        
        # Detectar y centrar cara de gato
        cara_gato, imagen_con_rectangulo = self.detectar_cara_gato(imagen_original)
        
        # Aplicar todos los filtros a la cara del gato
        filtro_gaussiano = self.aplicar_filtro_gaussiano(cara_gato)
        contornos_laplaciano = self.detectar_contornos_laplaciano(cara_gato)
        magnitud_gradiente, _ = self.analisis_gradiente(cara_gato)
        filtro_bilateral = self.aplicar_filtro_bilateral(cara_gato)
        filtro_mediana = self.aplicar_filtro_orden_estatico(cara_gato, tipo='mediana')
        filtro_highboost = self.aplicar_filtro_highboost(cara_gato)
        
        # Analizar simetría
        imagen_simetria, puntuacion_simetria, mitad_izq, mitad_der = self.analizar_simetria(cara_gato)
        
        # Crear un diccionario con todas las imágenes procesadas
        resultados = {
            'original': imagen_original,
            'deteccion_cara': imagen_con_rectangulo,
            'cara_gato': cara_gato,
            'filtro_gaussiano': filtro_gaussiano,
            'contornos_laplaciano': cv2.cvtColor(contornos_laplaciano, cv2.COLOR_GRAY2BGR) if len(contornos_laplaciano.shape) == 2 else contornos_laplaciano,
            'magnitud_gradiente': cv2.cvtColor(magnitud_gradiente, cv2.COLOR_GRAY2BGR) if len(magnitud_gradiente.shape) == 2 else magnitud_gradiente,
            'filtro_bilateral': filtro_bilateral,
            'filtro_mediana': filtro_mediana,
            'filtro_highboost': filtro_highboost,
            'imagen_simetria': imagen_simetria,
            'mitad_izquierda': mitad_izq,
            'mitad_derecha': mitad_der,
            'puntuacion_simetria': puntuacion_simetria
        }
        
        return resultados