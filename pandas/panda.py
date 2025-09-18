import pandas as pd

# 1) DataFrame pequeño de Marvel
data = [
    {"heroe": "Iron Man",     "nombre": "Tony Stark",     "equipo": "Avengers",  "fuerza": 70, "inteligencia": 98},
    {"heroe": "Captain America","nombre": "Steve Rogers", "equipo": "Avengers",  "fuerza": 78, "inteligencia": 75},
    {"heroe": "Thor",         "nombre": "Thor Odinson",   "equipo": "Avengers",  "fuerza": 95, "inteligencia": 65},
    {"heroe": "Hulk",         "nombre": "Bruce Banner",   "equipo": "Avengers",  "fuerza": 99, "inteligencia": 95},
    {"heroe": "Spider-Man",   "nombre": "Peter Parker",   "equipo": "Avengers",  "fuerza": 74, "inteligencia": 90},
    {"heroe": "Wolverine",    "nombre": "Logan",          "equipo": "X-Men",     "fuerza": 85, "inteligencia": 60},
    {"heroe": "Storm",        "nombre": "Ororo Munroe",   "equipo": "X-Men",     "fuerza": 80, "inteligencia": 70},
    {"heroe": "Star-Lord",    "nombre": "Peter Quill",    "equipo": "Guardians", "fuerza": 60, "inteligencia": 65},
]
df = pd.DataFrame(data)

print(df.head(0))
print(df.dtypes)
df.info()
print("columa heroes")
print(df.heroe)
# 2) Nueva columna simple (índice de poder: promedio de fuerza e inteligencia)
df["indice_poder"] = (df["fuerza"] + df["inteligencia"]) / 2

# 3) Filtros básicos
avengers = df[df["equipo"] == "Avengers"]
xmen_fuertes = df[(df["equipo"] == "X-Men") & (df["fuerza"] >= 80)]

# 4) Ordenar por fuerza (desc) y tomar top 3
top_fuerza = df.sort_values("fuerza", ascending=False).head(3)

# 5) Agrupar por equipo (promedio de fuerza e inteligencia)
promedios_equipo = df.groupby("equipo")[["fuerza", "inteligencia", "indice_poder"]].mean().round(1)

# 6) Búsqueda por patrón (héroes que contienen 'man', sin distinguir mayúsculas)
contienen_man = df[df["heroe"].str.contains("man", case=False)]

fuerza70=df.loc[df["fuerza"] > 70, "heroe"].tolist()
print("DataFrame base:\n", df, "\n")
print("Solo Avengers:\n", avengers, "\n")
print("X-Men con fuerza >= 80:\n", xmen_fuertes, "\n")
print("Top 3 por fuerza:\n", top_fuerza, "\n")
print("Promedios por equipo:\n", promedios_equipo, "\n")
print("Héroes que contienen 'man':\n", contienen_man, "\n")
print("heroes con fuerz mayor a 70:\n",fuerza70,"\n")

# 7) Guardar a CSV (opcional)
# df.to_csv("marvel_heroes.csv", index=False)

df = pd.DataFrame(data)
#revisar