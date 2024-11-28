import nltk

try:
    nltk.data.find('tokenizers/punkt')
    print("El recurso 'punkt' está disponible.")
except LookupError:
    print("El recurso 'punkt' no está disponible. Procediendo a descargarlo...")
    nltk.download('punkt')
