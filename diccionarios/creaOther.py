import json
import os

# Ruta del directorio donde se guardarán los archivos JSON
directory = "/Volumes/kevin/1/python3/diccionarios"
os.makedirs(directory, exist_ok=True)  # Crear la carpeta si no existe

# Crear un diccionario con el nuevo personaje de Marvel
nuevo_personaje = {
    "nickname": "mujer maravilla",
    "nombre_real": "brenda",
    "clase": "SuperHumana",
    "habilidades": ["fuerza", "me ama"]
}

# Función para encontrar un nombre de archivo disponible
def obtener_nombre_archivo(base_name, directory, extension=".json"):
    count = 0
    while True:
        filename = f"{base_name}{count if count > 0 else ''}{extension}"
        file_path = os.path.join(directory, filename)
        if not os.path.exists(file_path):
            return file_path
        count += 1

# Generar el nombre de archivo disponible
file_path = obtener_nombre_archivo("marvelianoss", directory)

# Guardar el nuevo personaje en el archivo JSON
with open(file_path, "w") as file:
    json.dump([nuevo_personaje], file, indent=4)

print(f"El personaje {nuevo_personaje['nickname']} se ha guardado en el archivo {os.path.basename(file_path)}.")
