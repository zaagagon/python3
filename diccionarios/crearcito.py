import json
import os

# Ruta del directorio donde se guardará el archivo JSON
directory = "/Volumes/kevin/1/python3/diccionarios"
os.makedirs(directory, exist_ok=True)  # Crear la carpeta si no existe
file_path = os.path.join(directory, "marvelianoski.json")

# Crear un diccionario para personajes de Marvel
marvelianos = {
    "nickname": "mujer maravilla",
    "nombre_real": "brenda",
    "clase": "SuperHumana",
    "habilidades": ["fuerza", "me ama"]
}

# Guardar el diccionario en el archivo JSON
with open(file_path, "w") as file:
    json.dump(marvelianos, file, indent=4)

print(f"El archivo JSON se ha creado en: {file_path}")
