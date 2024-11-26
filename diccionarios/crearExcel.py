import json
import os
from openpyxl import Workbook

# Ruta de la carpeta y los archivos
carpeta = "/Volumes/kevin/1/python3/diccionarios"
json_file = os.path.join(carpeta, "marvelianos.json")
excel_file = os.path.join(carpeta, "marvelianos.xlsx")

# Función para convertir JSON a Excel
def json_a_excel(json_path, excel_path):
    try:
        # Leer el archivo JSON
        with open(json_path, "r", encoding="utf-8") as file:
            marvelianos = json.load(file)

        # Crear un nuevo libro de Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Marvelianos"

        # Escribir encabezados
        headers = ["Nickname", "Nombre", "Clase", "Habilidades"]
        ws.append(headers)

        # Escribir datos de personajes
        for key, personaje in marvelianos.items():
            ws.append([
                personaje.get("nickname", ""),
                personaje.get("nombre", ""),
                personaje.get("clase", ""),
                ", ".join(personaje.get("habilidades", []))
            ])

        # Guardar el archivo Excel
        wb.save(excel_path)
        print(f"Archivo Excel creado exitosamente: {excel_path}")
    except Exception as e:
        print(f"Error al convertir JSON a Excel: {e}")

# Ejecutar la conversión
json_a_excel(json_file, excel_file)
