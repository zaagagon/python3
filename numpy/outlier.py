import numpy as np
import matplotlib.pyplot as plt

# Datos con un outlier
datos = [20, 21, 22, 23, 24, 90]

plt.boxplot(datos)
plt.title("Detección de Outliers con Boxplot")
plt.ylabel("Valores")
plt.show()
