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
