from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
import re
import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Preprocesamiento del texto
def preprocesar(texto):
    # Normalización
    texto = texto.lower()
    texto = re.sub(r'[^\w\s]', '', texto)
    
    # Tokenización
    tokens = word_tokenize(texto)
    
    # Eliminación de stopwords
    stop_words = set(stopwords.words('spanish'))
    tokens_filtrados = [word for word in tokens if word not in stop_words]
    
    # Lematización
    lemmatizer = WordNetLemmatizer()
    lematizados = [lemmatizer.lemmatize(word) for word in tokens_filtrados]
    
    # Stemming
    stemmer = SnowballStemmer('spanish')
    stemmed = [stemmer.stem(word) for word in lematizados]
    
    return stemmed

# Respuestas predefinidas
respuestas = {
    "hola": "¡Hola! ¿Cómo puedo ayudarte?",
    "estas": "Estoy bien, gracias por preguntar.",
    "adios": "¡Adiós! Que tengas un buen día."
}

# Función del chatbot
def chatbot():
    print("Chatbot: ¡Hola! Escribe algo para comenzar (o escribe 'salir' para terminar).")
    while True:
        entrada = input("Tú: ")
        if entrada.lower() == 'salir':
            print("Chatbot: ¡Adiós!")
            break
        tokens = preprocesar(entrada)
        print("Tokens procesados:", tokens)
        for token in tokens:
            if token in respuestas:
                print("Chatbot:", respuestas[token])
                break
        else:
            print("Chatbot: Lo siento, no entiendo eso.")

# Ejecutar el chatbot
chatbot()
