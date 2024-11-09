# Pedir al usuario un número
numero = int(input("Ingresa un número para ver su tabla de multiplicar: "))

# Generar la tabla de multiplicar
#f-string(formatted)
print(f"Tabla de multiplicar del {numero}:")
for i in range(1, 11):
    resultado = numero * i
    print(f"{numero} x {i} = {resultado}")
