# Recorrer una lista con for
nombres = ["Alice", "Bob", "Charlie"]

for nombre in nombres:
    print(nombre)
print(nombre[1])

for indice,elem in enumerate(nombres):
    print(indice,elem)