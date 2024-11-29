from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Validar si los campos existen en el formulario
        if 'nombre' not in request.form or 'edad' not in request.form:
            return jsonify({'error': 'Faltan campos en el formulario'}), 400
        
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        edad = request.form['edad']
        
        # Crear un diccionario con los nuevos datos
        nuevo_dato = {'nombre': nombre, 'edad': edad}
        
        # Verificar si el archivo JSON existe
        if os.path.exists('datos.json'):
            with open('datos.json', 'r') as file:
                try:
                    datos_existentes = json.load(file)
                except json.JSONDecodeError:
                    datos_existentes = []  # Si el archivo está corrupto, inicializamos como lista
            
            # Si los datos existentes no son una lista, conviértelos en una lista
            if isinstance(datos_existentes, dict):
                datos_existentes = [datos_existentes]
        else:
            datos_existentes = []  # Crear una lista vacía si no hay archivo
        
        # Agregar el nuevo dato a la lista
        datos_existentes.append(nuevo_dato)
        
        # Guardar los datos actualizados en el archivo JSON
        with open('datos.json', 'w') as file:
            json.dump(datos_existentes, file, indent=4)
        
        return jsonify({'mensaje': 'Datos guardados correctamente', 'datos': nuevo_dato})
    
    # Renderizar el formulario (busca en la carpeta 'templates')
    return render_template('form.html')

if __name__ == '__main__':
    port = 5217
    print(f"Servidor escuchando en el puerto {port}")
    app.run(port=port, debug=True)
