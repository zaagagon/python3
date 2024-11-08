import numpy as np
import matplotlib.pyplot as plt

# Definir los coeficientes de la parábola
a = 1
b = 0
c = 0

# Crear un rango de valores para x
x = np.linspace(-10, 10, 400)

# Calcular los valores de y usando la fórmula de la parábola
y = a * x**2 + b * x + c

# Graficar
plt.plot(x, y, label=f'y = {a}x² + {b}x + {c}', color='purple')
plt.xlabel('Valores de X')
plt.ylabel('Valores de Y')
plt.title('Gráfico de una parábola')
plt.legend()
plt.grid(True)

# Mostrar el gráfico
plt.show()
