from flask import Flask, request, jsonify, render_template
import json

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
        
        # Crear un diccionario con los datos
        datos = {'nombre': nombre, 'edad': edad}
        
        # Guardar los datos en un archivo JSON
        with open('datos.json', 'w') as file:
            json.dump(datos, file)
        
        return jsonify({'mensaje': 'Datos guardados correctamente', 'datos': datos})
    
    # Renderizar el formulario (busca en la carpeta 'templates')
    return render_template('form.html')

if __name__ == '__main__':
    port = 5012
    print(f"Servidor corriendo en el puerto {port}")
    app.run(port=port, debug=True)
