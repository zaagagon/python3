# filepath: /python-sequences/python-sequences/src/sequences_examples.py
# Este archivo demuestra el uso de listas y tuplas en Python

# Las listas son secuencias mutables (se pueden modificar)
frutas_lista = ['manzana', 'banana', 'naranja', 'uva']
print("Ejemplo de lista:", frutas_lista)
print("Tamaño de la lista:", len(frutas_lista))

# Agregando y eliminando elementos de la lista
frutas_lista.append('mango')
frutas_lista.remove('banana')
print("Lista modificada:", frutas_lista)

# Las tuplas son secuencias inmutables (no se pueden modificar)
frutas_tupla = ('manzana', 'banana', 'naranja', 'uva')
print("\nEjemplo de tupla:", frutas_tupla)
print("Tamaño de la tupla:", len(frutas_tupla))

# Intentar modificar la tupla generará un error
try:
    frutas_tupla[0] = 'mango'
except TypeError as e:
    print("No se puede modificar la tupla:", str(e))

# Comparando tamaños
print("\nLongitud de la lista:", len(frutas_lista))
print("Longitud de la tupla:", len(frutas_tupla))