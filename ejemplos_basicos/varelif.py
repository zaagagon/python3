nota = float(input("Ingresa la calificación del estudiante: "))

if nota >= 90:
    print("Excelente, tienes una A.")
elif nota >= 80:
    print("Muy bien, tienes una B.")
elif nota >= 70:
    print("Bien, tienes una C.")
elif nota >= 60:
    print("Aprobado, tienes una D.")
else:
    print("Reprobado, tienes una F.")
