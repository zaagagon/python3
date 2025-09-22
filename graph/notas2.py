import pandas as pd
import matplotlib.pyplot as plt

# Diccionario de estudiantes con sus notas
notas = {
    "Alicia": {"notas": [4.5, 6, 8, 10]},
    "Ramon": {"notas": [6.5, 7, 9, 10]},
    "Felipe": {"notas": [5.5, 9, 8.4, 10]}
}

# Convertir a DataFrame (serie por fila)
df = pd.DataFrame({nombre: datos["notas"] for nombre, datos in notas.items()})

# Transponer: cada estudiante como columna
df = df.T
df.columns = [f"Eval {i+1}" for i in range(df.shape[1])]

print("📊 DataFrame de notas:")
print(df)

# Calcular promedio por estudiante
df["Promedio"] = df.mean(axis=1)

# --- Graficar series ---
df.drop(columns=["Promedio"]).T.plot(marker="o")
plt.title("Evolución de notas por estudiante")
plt.xlabel("Evaluaciones")
plt.ylabel("Nota")
plt.ylim(0, 10)
plt.legend(title="Estudiantes")
plt.show()

# --- Graficar promedios ---
df["Promedio"].plot(kind="bar", color="skyblue")
plt.title("Promedio de notas por estudiante")
plt.ylabel("Promedio")
plt.ylim(0, 10)
plt.show()
