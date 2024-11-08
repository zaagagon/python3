import numpy as np
import matplotlib.pyplot as plt

# Crear dos arreglos de ejemplo
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 6, 8, 10])

# Graficar
plt.plot(x, y, marker='o', linestyle='-', color='b', label='Arreglo Y vs X')
plt.xlabel('Valores de X')
plt.ylabel('Valores de Y')
plt.title('Gráfico de dos arreglos')
plt.legend()
plt.grid(True)

# Mostrar el gráfico
plt.show()
