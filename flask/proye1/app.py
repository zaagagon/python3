from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        datos = {'nombre': nombre, 'edad': edad}
        with open('datos.json', 'w') as file:
            json.dump(datos, file)
        return jsonify({'mensaje': 'Datos guardados correctamente'})
    return render_template('./form.html')

if __name__ == '__main__':
    port=5009
    app.run(port=port,debug=True)