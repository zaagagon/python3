def calcular_pares():
    """
    Calcula y retorna los primeros 10 números pares
    
    Returns:
        list: Lista con los primeros 10 números pares
    """
    pares = []
    numero = 0
    
    # Bucle para encontrar los 10 primeros pares
    while len(pares) < 10:
        if numero % 2 == 0:
            pares.append(numero)
        numero += 1
        
    return pares

# Llamar a la función y mostrar resultados
numeros_pares = calcular_pares()
print("Los primeros 10 números pares son:")
for indice, numero in enumerate(numeros_pares, 1):
    print(f"{indice}. {numero}")