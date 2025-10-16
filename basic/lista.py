# Crear la lista inicial
numeros = [10, 20, 30, 40, 50]

# Añadir el número 60 al final
numeros.append(60)

# Insertar el número 15 entre el 10 y el 20 (posición 1)
numeros.insert(1, 15)

# Eliminar el número 30 de la lista
numeros.remove(30)

# Calcular la suma de todos los números
suma = sum(numeros)

# Calcular el promedio
promedio = suma / len(numeros)

# Imprimir los resultados
print("Lista resultante:", numeros)
print("Suma:", suma)
print("Promedio:", promedio)
