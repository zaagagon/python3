import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Diccionario de estudiantes y sus notas
notas = {
    "Alicia": {"notas": [4.5, 6, 8, 10]},
    "Ramon": {"notas": [6.5, 7, 9, 10]},
    "Felipe": {"notas": [5.5, 9, 8.4, 10]}
}

# Crear DataFrame
df = pd.DataFrame({nombre: datos["notas"] for nombre, datos in notas.items()})
df = df.T
df.columns = [f"Eval {i+1}" for i in range(df.shape[1])]
df["Promedio"] = df.mean(axis=1)

print("📊 Tabla de notas con promedio:\n")
print(df)

# ---- Gráfico de barras agrupadas ----
df_long = df.drop(columns=["Promedio"]).reset_index().melt(id_vars="index", var_name="Evaluación", value_name="Nota")
df_long.rename(columns={"index": "Estudiante"}, inplace=True)

plt.figure(figsize=(8,5))
sns.barplot(data=df_long, x="Estudiante", y="Nota", hue="Evaluación", palette="Set2")
plt.title("Notas por evaluación y estudiante")
plt.ylim(0, 10)
plt.show()

# ---- Gráfico de promedios ----
plt.figure(figsize=(6,4))
sns.barplot(x=df.index, y=df["Promedio"], palette="coolwarm")
plt.title("Promedio de notas por estudiante")
plt.ylim(0, 10)
plt.show()
