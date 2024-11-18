# Solicitar al usuario un número
numero = int(input("Introduce un número para generar su tabla de multiplicar: "))

# Usar for para generar la tabla
for i in range(1, 11):  # Itera del 1 al 10
    print(f"{numero} x {i} = {numero * i}")
