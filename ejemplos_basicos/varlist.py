# Recolección de datos
nombre = input("Escribe tu nombre: ")
apellido = input("Escribe tu apellido: ")
edad = input("¿Cuál es tu edad? ")

# Guardar en una lista
datos = [nombre, apellido, edad]

# Concatenar con separador
datos_separados = ", ".join(datos)
print("Datos concatenados:", datos_separados)

# Guardar en un archivo
with open("datos_usuario.txt", "w") as archivo:
    archivo.write(datos_separados)

print("Datos guardados en el archivo 'datos_usuario.txt'.")
