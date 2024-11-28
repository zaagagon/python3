# Importar la biblioteca nltk
import nltk
nltk.download('punkt_tab') 
from nltk.tokenize import word_tokenize

# Texto a tokenizar
texto = "Hola, ¿cómo estás?"

# Tokenización en palabras
tokens = word_tokenize(texto)

# Imprimir los tokens
print("Tokens generados:")
print(tokens)
