import tkinter as tk

def sumar():
    try:
        n1 = int(entry1.get())
        n2 = int(entry2.get())
        resultado = n1 + n2
        label_result.config(text=f"Resultado: {resultado}")
    except ValueError:
        label_result.config(text="Ingrese solo números")

# Crear ventana
ventana = tk.Tk()
ventana.title("Suma con Tkinter")

# Entradas
tk.Label(ventana, text="Número 1:").pack()
entry1 = tk.Entry(ventana)
entry1.pack()

tk.Label(ventana, text="Número 2:").pack()
entry2 = tk.Entry(ventana)
entry2.pack()

# Botón
btn = tk.Button(ventana, text="Sumar", command=sumar)
btn.pack()

# Etiqueta de resultado
label_result = tk.Label(ventana, text="Resultado: ")
label_result.pack()

# Iniciar app
ventana.mainloop()
