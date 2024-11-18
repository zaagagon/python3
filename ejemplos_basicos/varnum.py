# Variables numéricas
num1 = float(input("Escribe el primer número: "))
num2 = float(input("Escribe el segundo número: "))

# Operaciones básicas
suma = num1 + num2
diferencia = num1 - num2
producto = num1 * num2
cociente = num1 / num2

# Concatenación con resultados
resultado = f"""
Resultados:
Suma: {num1} + {num2} = {suma}
Diferencia: {num1} - {num2} = {diferencia}
Producto: {num1} * {num2} = {producto}
Cociente: {num1} / {num2} = {cociente}
"""
print(resultado)
