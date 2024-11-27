from flask import Flask

app=Flask(__name__)
@app.route("/")
def home():
    return "Hola, corriendo flask en otro puerto"

if __name__=="__main__":
    port=5003
    print(f"servidor corriendo en yolis{port}")
    app.run(port=port)
    