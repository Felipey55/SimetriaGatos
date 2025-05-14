# Análisis de Simetría en Gatos 🐱

## Descripción
Este proyecto implementa un sistema avanzado de análisis de simetría facial en imágenes de gatos utilizando técnicas de procesamiento de imágenes. La aplicación ofrece una interfaz gráfica intuitiva que permite a los usuarios seleccionar, procesar y analizar imágenes de gatos para determinar su nivel de simetría facial.

## ✨ Características Principales

- 🔍 **Detección Facial Automática**
  - Identificación precisa de la cara del gato
  - Enfoque automático en la región facial

- 🖼️ **Procesamiento Avanzado de Imágenes**
  - Filtro Gaussiano para reducción de ruido
  - Detección de contornos mediante operador Laplaciano
  - Análisis de gradiente con operador Sobel
  - Filtro bilateral para preservación de bordes
  - Filtros de orden estático (mediana, mínimo, máximo)
  - Realce de detalles con filtro highBoost

- 📊 **Análisis de Simetría**
  - Comparación precisa de mitades faciales
  - Puntuación de simetría porcentual
  - Visualización de resultados

- 🎯 **Interfaz Moderna**
  - Diseño intuitivo de tres paneles
  - Visualización en tiempo real del procesamiento
  - Navegación fluida entre secciones

## 🛠️ Requisitos Técnicos

- Python 3.6 o superior
- Bibliotecas principales:
  ```
  numpy==1.21.0
  opencv-python==4.5.3.56
  matplotlib==3.4.3
  pillow==8.3.2
  ```
- Tkinter (incluido en la mayoría de instalaciones de Python)

## 🚀 Instalación

1. Clone el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/simetria_gatos.git
   cd simetria_gatos
   ```

2. Instale las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Uso

1. Inicie la aplicación:
   ```bash
   python main.py
   ```

2. Navegue por la interfaz:
   - **Panel Izquierdo**: Explore y seleccione imágenes de gatos
   - **Panel Central**: Visualice el proceso de tratamiento paso a paso
   - **Panel Derecho**: Examine el análisis de simetría y resultados

3. Interactúe con la aplicación:
   - Seleccione una imagen haciendo clic en su miniatura
   - Observe el proceso de análisis en tiempo real
   - Revise los resultados de simetría facial

## 📁 Estructura del Proyecto

```
simetria_gatos/
├── main.py              # Punto de entrada de la aplicación
├── interfaz.py          # Implementación de la interfaz gráfica
├── procesamiento_imagenes.py  # Funciones de procesamiento
├── requirements.txt     # Dependencias del proyecto
├── img/                 # Directorio de imágenes
└── README.md           # Documentación
```

## 📝 Notas Importantes

- Formatos de imagen soportados: JPG, PNG, BMP
- Para resultados óptimos, use imágenes donde la cara del gato sea claramente visible
- La puntuación de simetría se presenta en porcentaje (100% = simetría perfecta)

## 🤝 Contribución

Las contribuciones son bienvenidas. Para contribuir:

1. Haga fork del proyecto
2. Cree una rama para su característica (`git checkout -b feature/NuevaCaracteristica`)
3. Realice sus cambios y haga commit (`git commit -am 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abra un Pull Request

## 👥 Autores
- Anderson Francisco Diaz Ciro
- Karen Eliana Muñoz Maya
- Carlos Felipe Suarez Rodriguez

## 🙏 Agradecimientos

- A la comunidad de procesamiento de imágenes
- A todos los contribuidores del proyecto
- A los gatos que prestaron sus rostros para el desarrollo
- Al Profesor Jhon Erick por su guía y apoyo y su 5.0.