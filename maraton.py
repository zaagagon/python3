horas, minutos, distancia = 2, 25, 42.195
total_min = horas*60 + minutos
pace = total_min / distancia
mm = int(pace)
ss = int(round((pace - mm)*60))
print(f"Ritmo: {pace:.4f} min/km  (~ {mm:02d}:{ss:02d} /km)")