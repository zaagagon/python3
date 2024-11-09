# Número secreto
numero_secreto = 7

# Pedir al usuario que adivine el número
intento = int(input("Adivina el número entre 1 y 10: "))

# Comprobar si adivinó
if intento == numero_secreto:
    print("¡Felicidades! Adivinaste el número.")
else:
    print("Lo siento, intenta de nuevo.")
