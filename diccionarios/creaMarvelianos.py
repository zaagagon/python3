import json
import os

# Ruta del directorio donde se guardará el archivo JSON
directory = "/Volumes/kevin/1/python3/diccionarios"
os.makedirs(directory, exist_ok=True)  # Crear la carpeta si no existe
file_path = os.path.join(directory, "marvelianos3.json")

# Crear un diccionario vacío para personajes de Marvel
marvelianos = {
    "nickname":"mujer maravilla",
    "nombre_real":"brenda",
    "clase":"SuperHumana",
    "habilidades":["fuerza","me ama"]
    
}

# Función para agregar un personaje al diccionario
def agregar_marveliano(diccionario):
    print("\nAgregar un nuevo personaje de Marvel:")
    nickname = input("Ingrese el nickname del personaje (clave en el diccionario): ").strip()
    nombre_real = input("Ingrese el nombre real del personaje: ").strip()
    clase = input("Ingrese la clase del personaje (mutante, tecnológico, etc.): ").strip()
    habilidades = input("Ingrese las habilidades separadas por comas: ").strip().split(",")
    habilidades = [h.strip() for h in habilidades]  # Limpiar espacios adicionales
    
    # Agregar personaje al diccionario
    diccionario[nickname] = {
        "nickname": nickname,
        "nombre": nombre_real,
        "clase": clase,
        "habilidades": habilidades
    }
    print(f"Personaje {nombre_real} agregado correctamente.")

# Llenar el diccionario con varios personajes
while True:
    agregar_marveliano(marvelianos)
    continuar = input("¿Desea agregar otro personaje? (s/n): ").strip().lower()
    if continuar != 's':
        break

# Guardar el diccionario en un archivo JSON
with open(file_path, "w") as json_file:
    json.dump(marvelianos, json_file, indent=4, ensure_ascii=False)

print(f"\nDiccionario de Marvel guardado en: {file_path}")
