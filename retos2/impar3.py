# Este programa le pide al usuario que ingrese un número y luego determina si es par o impar.

# Pedir al usuario que ingrese un número
numero = int(input("Ingresa un número: "))

# Comprobar si el número es par o impar
if numero % 2 == 0:
    print("El número es par.")
else:
    print("El número es impar.")

