import numpy as np
from scipy import stats

# Arreglo de ejemplo
arreglo = np.array([1, 2, 2, 3, 4, 5, 5, 5, 6])

# Calcular la media
media = np.mean(arreglo)

# Calcular la mediana
mediana = np.median(arreglo)

# Calcular la moda
moda = stats.mode(arreglo)
moda_valor = moda.mode[0]
frecuencia_moda = moda.count[0]

# Imprimir resultados
print("Media:", media)
print("Mediana:", mediana)
print("Moda:", moda_valor)
print("Frecuencia de la moda:", frecuencia_moda)
