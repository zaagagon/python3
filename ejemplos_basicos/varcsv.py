# Recolección de datos
nombre = input("Escribe tu nombre: ")
apellido = input("Escribe tu apellido: ")
edad = input("¿Cuál es tu edad? ")

# Guardar como línea de CSV
linea_csv = f"{nombre},{apellido},{edad}\n"

# Escribir en un archivo CSV
with open("usuarios.csv", "a") as archivo_csv:
    archivo_csv.write(linea_csv)

print("Datos guardados en el archivo 'usuarios.csv'.")
