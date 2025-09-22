import matplotlib.pyplot as plt

# Diccionario con notas anidadas
notas = {
    "Alicia": {"notas": [4.5, 6, 8, 10]},
    "Ramon": {"notas": [6.5, 7, 9, 10]},
    "Felipe": {"notas": [5.5, 9, 8.4, 10]}
}

# Seleccionar un estudiante
estudiante = "Alicia"
valores = notas[estudiante]["notas"]   # 👈 importante: acceder a la lista dentro del diccionario

# Graficar
plt.bar(range(1, len(valores)+1), valores, color="skyblue")
#plt.title(f"Notas de {estudiante}")
#plt.xlabel("Evaluaciones")
#plt.ylabel("Nota")
#plt.ylim(0, 10)
plt.show()
