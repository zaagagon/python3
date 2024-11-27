import pandas as pd
import matplotlib.pyplot as plt

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

# Convertir a DataFrame
df = pd.DataFrame.from_dict(datos_marvel, orient='index')

# Graficar ambas variables
df.plot(kind='bar', figsize=(10, 6), color=['blue', 'green'])

# Personalizar la gráfica
plt.title('Poder y Velocidad de los Personajes de Marvel')
plt.xlabel('Personajes')
plt.ylabel('Valores')
plt.xticks(rotation=45)
plt.legend(title='Atributos')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Mostrar la gráfica
plt.tight_layout()
plt.show()
