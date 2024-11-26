import json
import csv
import os

# Ruta de la carpeta y los archivos
carpeta = "/Volumes/kevin/1/python3/diccionarios"
json_file = os.path.join(carpeta, "marvelianos.json")
csv_file = os.path.join(carpeta, "marvelianos.csv")

# Función para convertir JSON a CSV
def json_a_csv(json_path, csv_path):
    try:
        # Leer el archivo JSON
        with open(json_path, "r", encoding="utf-8") as file:
            marvelianos = json.load(file)
        
        # Crear el archivo CSV
        with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            
            # Escribir encabezados
            writer.writerow(["Nickname", "Nombre", "Clase", "Habilidades"])
            
            # Escribir datos
            for key, personaje in marvelianos.items():
                writer.writerow([
                    personaje.get("nickname", ""),
                    personaje.get("nombre", ""),
                    personaje.get("clase", ""),
                    ", ".join(personaje.get("habilidades", []))
                ])
        
        print(f"Archivo CSV creado exitosamente: {csv_path}")
    except Exception as e:
        print(f"Error al convertir JSON a CSV: {e}")

# Ejecutar la conversión
json_a_csv(json_file, csv_file)
