import json
import os

# Ruta del directorio donde se guardará el archivo JSON
directory = "/Volumes/kevin/1/python3/diccionarios"
os.makedirs(directory, exist_ok=True)  # Crear la carpeta si no existe
file_path = os.path.join(directory, "marvelianoss.json")

# Crear un diccionario vacío para personajes de Marvel
marvelianos = {
    "nickname":"mujer maravilla",
    "nombre_real":"brenda",
    "clase":"SuperHumana",
    "habilidades":["fuerza","me ama"]
    
}