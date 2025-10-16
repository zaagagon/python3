#funcion que suma y resta dos numeros
def sumar_restar(a, b):
    suma = a + b
    resta = a - b
    return suma, resta
    
resultado_suma, resultado_resta = sumar_restar(10, 5)
print("Suma:", resultado_suma)
print("Resta:", resultado_resta)
