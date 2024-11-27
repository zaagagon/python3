import json
import os

# Ruta del directorio donde se guardará el archivo JSON
directory = "/Volumes/kevin/1/python3/diccionarios"
os.makedirs(directory, exist_ok=True)  # Crear la carpeta si no existe
file_path = os.path.join(directory, "marvelianoss.json")

# Crear un diccionario con el nuevo personaje de Marvel
nuevo_personaje = {
    "nickname": "mujer maravilla",
    "nombre_real": "brenda",
    "clase": "SuperHumana",
    "habilidades": ["fuerza", "me ama"]
}

# Leer el archivo existente si existe
if os.path.exists(file_path):
    with open(file_path, "r") as file:
        try:
            marvelianos = json.load(file)  # Cargar datos existentes
        except json.JSONDecodeError:
            marvelianos = []  # Crear lista vacía si el archivo está vacío o tiene un formato incorrecto
else:
    marvelianos = []  # Crear lista vacía si el archivo no existe

# Agregar el nuevo personaje a la lista
marvelianos.append(nuevo_personaje)

# Guardar la lista actualizada en el archivo JSON
with open(file_path, "w") as file:
    json.dump(marvelianos, file, indent=4)

print(f"El personaje {nuevo_personaje['nickname']} se ha añadido al archivo JSON.")
