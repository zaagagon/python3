import numpy as np

# Crear tabla de multiplicar del 1 al 10
x = np.arange(1, 11)
tabla = np.outer(x, x)

print(tabla)
