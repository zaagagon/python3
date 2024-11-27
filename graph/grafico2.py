import pandas as pd
import matplotlib.pyplot as plt


# Diccionario con los poderes de personajes de Marvel
poderes_marvel = {
    'Iron Man': 85,
    'Thor': 95,
    'Hulk': 90,
    'Captain America': 80,
    'Black Widow': 70,
    'Hawkeye': 65,
    'Scarlet Witch': 95,
    'Doctor Strange': 92
}

# Convertir el diccionario en un DataFrame
df = pd.DataFrame(list(poderes_marvel.items()), columns=['Personaje', 'Poder'])

# Graficar los datos
df.plot(x='Personaje', y='Poder', kind='bar', color='blue', legend=False)

# Personalizar la gráfica
plt.title('Poder de los personajes de Marvel')
plt.xlabel('Personajes')
plt.ylabel('Poder')
plt.xticks(rotation=45)  # Rotar nombres para mejor visibilidad
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Mostrar la gráfica
plt.tight_layout()  # Ajusta el diseño para que no se corte el texto
plt.show()
