import numpy as np

arr = np.array([1, 2, 3, 4, 5])

print(arr + 10)   # Suma 10 a cada elemento
print(arr * 2)    # Multiplica cada elemento por 2

mat = np.ones((3, 3))
print(mat + arr[:3])  # Broadcasting: suma vector a cada fila
bro