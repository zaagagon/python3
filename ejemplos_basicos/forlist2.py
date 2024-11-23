# Simular un bucle basado en índices
nombres = ["Alice", "Bob", "Charlie",9,7]
numeros=[45,6,78,8,7,3,67,999]
print(len(nombres))
print(numeros.pop())
print(numeros)
numeros.insert(5,909)
#numeros=123
print(numeros)
numeros.append(10)
print("appe",numeros)
#print(nombres(2))
print(nombres[2])

for i in range(len(nombres)):
    print(f"Índice {i}: {nombres[i]}")
