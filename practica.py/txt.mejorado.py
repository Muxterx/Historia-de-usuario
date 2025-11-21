print("====FORMA PROFESIONAL====")

with open ("archivo_mejorado.txt", "w") as file:
    file.write("\nesta forma es mejor y simplificada")
    file.write("\nmucho mejor")
with open("archivo_mejorado.txt", "r") as file:
    contenido= file.read()
print ( contenido)