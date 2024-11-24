# Recorrer una lista con for
nombres = ["Alice", "Bob", "Charlie"]

for nombre in nombres:
    print(nombre)
#muestra el contenido de nombre es decir h porque es posicio 1
print(nombre[1])
#muestra indice valor de la lista
for indice,elem in enumerate(nombres):
    print(indice,elem)