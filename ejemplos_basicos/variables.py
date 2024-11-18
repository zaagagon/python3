# Variable global
global_variable = "Hola, soy una variable global"

def saludo_usuario():
    # Variable local
    local_variable = input("Por favor, escribe tu nombre: ")
    print(f"Hola, {local_variable}, desde una función.")
    print(global_variable)  # Accediendo a la variable global

saludo_usuario()
