# Importar las librerías necesarias
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

# Descargar los recursos necesarios de NLTK
nltk.download('punkt')  # Tokenización
nltk.download('stopwords')  # Stopwords
nltk.download('wordnet')  # Lematización
nltk.download('omw-1.4')  # Diccionario adicional para lematización

# Paso 1: Función para normalización, tokenización, eliminación de stopwords y lematización
def preprocesar(texto):
    """
    Normaliza y procesa el texto de entrada:
    - Convierte a minúsculas.
    - Elimina puntuación.
    - Tokeniza el texto.
    - Filtra stopwords.
    - Aplica lematización a las palabras.
    """
    # Normalización: convertir a minúsculas y eliminar puntuación
    texto = texto.lower()
    texto = re.sub(r'[^\w\s]', '', texto)  # Eliminar signos de puntuación
    
    # Tokenización: dividir el texto en palabras individuales
    tokens = word_tokenize(texto)
    
    # Eliminación de stopwords: palabras comunes como 'el', 'la', 'de'
    stop_words = set(stopwords.words('spanish'))
    tokens_filtrados = [word for word in tokens if word not in stop_words]
    
    # Lematización: convertir las palabras a su forma base
    lemmatizer = WordNetLemmatizer()
    lematizados = [lemmatizer.lemmatize(word) for word in tokens_filtrados]
    
    return lematizados

# Paso 2: Respuestas predefinidas
respuestas = {
    "hola": "¡Hola! ¿Cómo puedo ayudarte?",
    "estas": "Estoy bien, gracias por preguntar.",
    "adios": "¡Adiós! Que tengas un buen día.",
    "gracias": "¡De nada! Estoy aquí para ayudarte.",
    "nombre": "Soy un chatbot simple, pero puedes llamarme ChatBot."
}

# Paso 3: Función del chatbot
def chatbot():
    """
    Función principal del chatbot.
    - Procesa la entrada del usuario.
    - Busca palabras clave en las respuestas predefinidas.
    - Responde según corresponda o indica que no entiende.
    """
    print("Chatbot: ¡Hola! Escribe algo para comenzar (o escribe 'salir' para terminar).")
    while True:
        # Entrada del usuario
        entrada = input("Tú: ")
        
        # Opción para salir del chatbot
        if entrada.lower() == 'salir':
            print("Chatbot: ¡Adiós! Que tengas un excelente día.")
            break
        
        # Preprocesar la entrada del usuario
        tokens = preprocesar(entrada)
        print("Tokens procesados:", tokens)  # Mostrar tokens para depuración
        
        # Buscar respuestas
        for token in tokens:
            if token in respuestas:
                print("Chatbot:", respuestas[token])
                break
        else:
            print("Chatbot: Lo siento, no entiendo eso.")

# Ejecutar el chatbot
# Chatbot funcionando
chatbot()
