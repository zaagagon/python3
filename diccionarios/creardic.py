import json
import os

# Ruta del directorio donde se guardará el archivo JSON
directory = "/Volumes/kevin/1/python3/diccionarios"

# Crear la carpeta si no existe
os.makedirs(directory, exist_ok=True)

# Ruta completa del archivo JSON
file_path = os.path.join(directory, "personajes.json")

# Diccionario con la información de los personajes
personajes = {
    "Trinity": {
        "nombre": "Trinity",
        "edad": 28,
        "profesión": "Hacker",
        "habilidades": ["artes marciales", "hackeo avanzado"]
    },
    "Hulk": {
        "nombre": "Hulk",
        "edad": 45,
        "profesión": "Científico",
        "habilidades": ["superfuerza", "resistencia extrema", "curación rápida"]
    },
    "Wolverine": {
        "nombre": "Wolverine",
        "edad": 137,
        "profesión": "Mutante",
        "habilidades": ["regeneración", "garras de adamantium", "sentidos agudos"]
    }
}

# Guardar el diccionario en un archivo JSON
with open(file_path, "w") as json_file:
    json.dump(personajes, json_file, indent=4, ensure_ascii=False)

print(f"Archivo JSON creado exitosamente en: {file_path}")
