# colores.py

def texto_colorido(texto, color):
    colores = {
        "rojo": "\033[91m",
        "verde": "\033[92m",
        "amarillo": "\033[93m",
        "azul": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "blanco": "\033[97m",
        "reset": "\033[0m"
    }
    # Devuelve el texto con el color elegido y resetea el color
    return f"{colores.get(color, colores['reset'])}{texto}{colores['reset']}"
