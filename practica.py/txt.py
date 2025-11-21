print ("----mi primer texto----")

archivo= open('este es mi_primeer_archivo', 'w')
archivo.write('hola, esto es practica\n')
archivo.write('otra linea mas\n')
archivo.close()

print("archivo creado")

print("\n=== ARCHIVO CREADO===")

archivo=open('mi_primeer_archivo.txt', 'r')
contenido= archivo.read()
print(contenido)
archivo.close