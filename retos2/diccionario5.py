import pandas as pd

# Crear un diccionario de una persona (Peter Parker)
persona = {
    "nombre": "Peter Parker",
    "edad": 18,
    "ciudad": "Nueva York"
}

personas = [
    {"nombre": "Peter Parker", "edad": 18, "ciudad": "Nueva York"},
    {"nombre": "Tony Stark", "edad": 48, "ciudad": "Malibu"},
    {"nombre": "Natasha Romanoff", "edad": 35, "ciudad": "San Petersburgo"},
    {"nombre": "Bruce Banner", "edad": 45, "ciudad": "Dayton"},
    {"nombre": "Steve Rogers", "edad": 102, "ciudad": "Brooklyn"},
    {"nombre": "Diana Prince", "edad": 900, "ciudad": "Themyscira"},
    {"nombre": "Clark Kent", "edad": 36, "ciudad": "Smallville"},
    {"nombre": "Barry Allen", "edad": 30, "ciudad": "Central City"},
    {"nombre": "Arthur Curry", "edad": 34, "ciudad": "Atlantis"},
    {"nombre": "Victor Stone", "edad": 27, "ciudad": "Detroit"}
]

# Crear el DataFrame con pandas
df_personas = pd.DataFrame(personas)
df_personas

# Crear el DataFrame
df_personas = pd.DataFrame(personas)
print(df_personas)

print("primeras cinco filas de dataframe")
print(df_personas.head())  # Muestra las primeras 5 filas


print(df_personas.describe())

df_personas.to_csv("personas.csv", index=False)

df_personas.to_excel("personas_exportado.xlsx", index=False)

print(df_personas.info())

#cambios con nuevos datos al dataframe
import pandas as pd

# Datos iniciales
personas = [
    {"nombre": "Peter Parker", "edad": 18, "ciudad": "Nueva York"},
    {"nombre": "Tony Stark", "edad": 48, "ciudad": "Malibu"},
    {"nombre": "Natasha Romanoff", "edad": 35, "ciudad": "San Petersburgo"},
    {"nombre": "Bruce Banner", "edad": 45, "ciudad": "Dayton"},
    {"nombre": "Steve Rogers", "edad": 102, "ciudad": "Brooklyn"},
    {"nombre": "Diana Prince", "edad": 900, "ciudad": "Themyscira"},
    {"nombre": "Clark Kent", "edad": 36, "ciudad": "Smallville"},
    {"nombre": "Barry Allen", "edad": 30, "ciudad": "Central City"},
    {"nombre": "Arthur Curry", "edad": 34, "ciudad": "Atlantis"},
    {"nombre": "Victor Stone", "edad": 27, "ciudad": "Detroit"}
]

# Crear el DataFrame inicial
df_personas = pd.DataFrame(personas)

# Nuevos datos para anexar
nuevas_personas = [
    {"nombre": "Nick Fury", "edad": 55, "ciudad": "Nueva York"},
    {"nombre": "Maria Hill", "edad": 42, "ciudad": "Nueva York"},
    {"nombre": "Phil Coulson", "edad": 50, "ciudad": "Nueva York"},
    {"nombre": "Gamora", "edad": 30, "ciudad": "Knowhere"},
    {"nombre": "Nebula", "edad": 30, "ciudad": "Knowhere"},
    {"nombre": "Rocket Raccoon", "edad": 10, "ciudad": "Knowhere"},
    {"nombre": "Groot", "edad": 5, "ciudad": "Knowhere"},
    {"nombre": "Thor", "edad": 1500, "ciudad": "Asgard"},
    {"nombre": "Loki", "edad": 1048, "ciudad": "Asgard"},
    {"nombre": "Valkyrie", "edad": 1000, "ciudad": "Asgard"}
]

# Crear DataFrame de las nuevas personas
df_nuevas_personas = pd.DataFrame(nuevas_personas)

# Anexar los nuevos datos
df_personas = pd.concat([df_personas, df_nuevas_personas], ignore_index=True)

df_personas.to_csv("personas_actualizado.csv", index=False)

# Guardar el DataFrame final en un archivo de Excel
df_personas.to_excel("personas_actualizado.xlsx", index=False)

# Mostrar el DataFrame final
print(df_personas)

# Filtrar filas con edades mayores a 100
df_personas = df_personas[df_personas["edad"] <= 100]

#ultima linea de dataframe con cambios

import matplotlib.pyplot as plt

# Histograma de edades
plt.hist(df_personas["edad"], bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], edgecolor='black')
plt.xlabel("Rango de Edad")
plt.ylabel("Número de Personas")
plt.title("Distribución de Edades")
plt.show()


import matplotlib.pyplot as plt
df_personas["edad"].hist()
plt.xlabel("Edad")
plt.ylabel("Frecuencia")
plt.title("Distribución de Edad")
plt.show()

#mejorada con nombres
import matplotlib.pyplot as plt

# Ordenar DataFrame por edades para mayor claridad en el gráfico
df_personas_ordenado = df_personas.sort_values(by="edad")

# Crear gráfico de barras con nombres
plt.figure(figsize=(10, 6))
plt.barh(df_personas_ordenado["nombre"], df_personas_ordenado["edad"], color='skyblue', edgecolor='black')
plt.xlabel("Edad")
plt.ylabel("Nombre")
plt.title("Edad de Cada Persona")
plt.show()

# Crear gráfico de dispersión
plt.figure(figsize=(10, 6))
plt.scatter(df_personas["edad"], df_personas.index, color="purple")
plt.xlabel("Edad")
plt.ylabel("Persona")
plt.title("Distribución de Edad de las Personas")

# Añadir nombres como etiquetas para cada punto
for i, nombre in enumerate(df_personas["nombre"]):
    plt.annotate(nombre, (df_personas["edad"].iloc[i], i), xytext=(5, -5), textcoords="offset points")

plt.show()



# Acceder a valores
print("Nombre:", persona["nombre"])  # Peter Parker
print("Edad:", persona.get("edad"))  # 18

# Modificar el valor de una clave
persona["edad"] = 19
print("Edad modificada:", persona["edad"])  # 19

# Agregar una nueva clave
persona["profesion"] = "Fotógrafo"
print("Profesión:", persona["profesion"])  # Fotógrafo

# Eliminar una clave
del persona["ciudad"]
print(persona)  # {'nombre': 'Peter Parker', 'edad': 19, 'profesion': 'Fotógrafo'}
