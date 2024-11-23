# secuencia variable
#bloque

personajes=["wolverine","logan","deadpool"]
for personajes in personajes:
    print(f"contenido lista : {personajes}")

#prueba con lista personajes
for personajes in personajes:
    print(personajes)
    
print("hola master solucionando ")
#git push no funciona pero git push origin head si

#Cuando usas git push y no funciona, pero git push origin HEAD sí lo hace, la razón está en cómo Git maneja las ramas locales y remotas, y si están correctamente configuradas para rastrearse mutuamente.
"""
Explicación del Comportamiento
1. Qué hace git push:
Por defecto, git push intenta empujar la rama actual al upstream (rama remota rastreada).
Si la rama local no tiene configurada una relación de seguimiento con una rama remota (upstream), Git no sabe dónde empujar los cambios, y el comando falla.
2. Qué hace git push origin HEAD:
Este comando fuerza a Git a empujar la rama actual (representada por HEAD) al repositorio remoto (origin) y la asocia manualmente con la rama remota del mismo nombre.
No depende de que exista una configuración previa de upstream, por lo que funciona incluso si no has configurado la rama correctamente."""