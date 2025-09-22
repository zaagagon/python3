import seaborn as sns
import matplotlib.pyplot as plt

# Datos de ejemplo
tips = sns.load_dataset("tips")

# Crear gráfico de dispersión
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="sex")

plt.title("Relación entre cuenta total y propina")
plt.show()
