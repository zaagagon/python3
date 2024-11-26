from flask import Flask, request, jsonify
import os
import json
from flask import  render_template


app = Flask(__name__)


# Ruta del archivo JSON
JSON_PATH = "/Volumes/kevin/1/python3/diccionarios/marvelianos.json"

# Función para cargar datos del archivo JSON
def cargar_datos():
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, "r") as file:
            return json.load(file)
    return {}

# Ruta para la página principal
@app.route("/")
def home():
    return render_template("index.html")

# Función para guardar datos en el archivo JSON
def guardar_datos(data):
    with open(JSON_PATH, "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Ruta para obtener todos los personajes
@app.route("/personajes", methods=["GET"])
def obtener_personajes():
    datos = cargar_datos()
    return jsonify(datos)

# Ruta para agregar o actualizar un personaje
@app.route("/personajes", methods=["POST"])
def agregar_actualizar_personaje():
    datos = cargar_datos()
    personaje = request.json
    nickname = personaje.get("nickname")

    if not nickname:
        return jsonify({"error": "El nickname es obligatorio"}), 400

    datos[nickname] = personaje
    guardar_datos(datos)
    return jsonify({"message": "Personaje agregado o actualizado correctamente"})

# Ruta para eliminar un personaje
@app.route("/personajes/<nickname>", methods=["DELETE"])
def eliminar_personaje(nickname):
    datos = cargar_datos()
    if nickname in datos:
        del datos[nickname]
        guardar_datos(datos)
        return jsonify({"message": f"Personaje {nickname} eliminado correctamente"})
    return jsonify({"error": "Personaje no encontrado"}), 404

if __name__ == "__main__":
    app.run(debug=True)
