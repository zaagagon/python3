import numpy as np

# Diccionario con poderes y velocidades de personajes de Marvel
datos_marvel = {
    'Iron Man': {'Poder': 85, 'Velocidad': 70},
    'Thor': {'Poder': 95, 'Velocidad': 65},
    'Hulk': {'Poder': 90, 'Velocidad': 40},
    'Captain America': {'Poder': 80, 'Velocidad': 75},
    'Black Widow': {'Poder': 70, 'Velocidad': 85},
    'Hawkeye': {'Poder': 65, 'Velocidad': 80},
    'Scarlet Witch': {'Poder': 95, 'Velocidad': 50},
    'Doctor Strange': {'Poder': 92, 'Velocidad': 60}
}

# Extraer los valores de poder y velocidad
poderes = np.array([personaje['Poder'] for personaje in datos_marvel.values()])
velocidades = np.array([personaje['Velocidad'] for personaje in datos_marvel.values()])

# Operaciones con NumPy

# 1. Máximo y Mínimo
print(poderes)
print(velocidades)
print(f"Máximo poder: {np.max(poderes)}")  # Poder máximo
print(f"Mínimo poder: {np.min(poderes)}")  # Poder mínimo

# 2. Promedio
print(f"Promedio de poder: {np.mean(poderes):.2f}")  # Promedio de poder

# 3. Mediana
print(f"Mediana de poder: {np.median(poderes)}")  # Mediana del poder

# 4. Desviación estándar
print(f"Desviación estándar de poder: {np.std(poderes):.2f}")  # Desviación estándar

# 5. Varianza
print(f"Varianza de poder: {np.var(poderes):.2f}")  # Varianza

# 6. Suma total
print(f"Suma total de poder: {np.sum(poderes)}")  # Suma de todos los poderes

# 7. Percentiles
print(f"Percentil 25 de poder: {np.percentile(poderes, 25)}")  # Percentil 25
print(f"Percentil 75 de poder: {np.percentile(poderes, 75)}")  # Percentil 75

# 8. Rango (máximo - mínimo)
print(f"Rango de poder (max - min): {np.ptp(poderes)}")  # Diferencia entre max y min

# 9. Producto de todos los valores
print(f"Producto de todos los poderes: {np.prod(poderes)}")  # Producto de todos los valores

# 10. Comparación de máximos entre poderes y velocidades
print(f"Mayor entre máximos (Poder vs Velocidad): {max(np.max(poderes), np.max(velocidades))}")

# 11. Relación entre poder y velocidad (promedio)
relacion_poder_velocidad = np.mean(poderes / velocidades)
print(f"Relación promedio (Poder/Velocidad): {relacion_poder_velocidad:.2f}")

# 12. Normalización de los poderes (escalar entre 0 y 1)
poder_normalizado = (poderes - np.min(poderes)) / (np.max(poderes) - np.min(poderes))
print(f"Poderes normalizados: {poder_normalizado}")

# 13. Diferencia absoluta entre poder y velocidad
diferencia_poder_velocidad = np.abs(poderes - velocidades)
print(f"Diferencia absoluta entre poder y velocidad: {diferencia_poder_velocidad}")

# 14. Indices del máximo y mínimo poder
indice_max_poder = np.argmax(poderes)
indice_min_poder = np.argmin(poderes)
print(f"Índice del máximo poder: {indice_max_poder} (Personaje: {list(datos_marvel.keys())[indice_max_poder]})")
print(f"Índice del mínimo poder: {indice_min_poder} (Personaje: {list(datos_marvel.keys())[indice_min_poder]})")
