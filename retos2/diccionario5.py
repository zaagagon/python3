# Crear un diccionario de una persona (Peter Parker)
persona = {
    "nombre": "Peter Parker",
    "edad": 18,
    "ciudad": "Nueva York"
}

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
