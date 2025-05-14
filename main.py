import tkinter as tk
from interfaz import InterfazSimetriaGatos

def main():
    """
    Función principal para iniciar la aplicación de análisis de simetría en gatos.
    """
    root = tk.Tk()
    app = InterfazSimetriaGatos(root)
    root.mainloop()

if __name__ == "__main__":
    main()