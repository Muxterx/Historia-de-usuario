import os 

print("===MODULO OS===\n")
if os.path.exists("archivo.txt"):
    print("el archivo existe")
else:
    print("el archivo no existe")

print("\narchivos en esta carpeta:")
archivos= os.listdir()
for archivo in archivos:
    print(f" - {archivo}")

if not os.path.exists("nuevo.txt"):
    with open("nuevo.txt", "w") as f:
      f.write("nuevo archivo")
      print("\narchivo 'nuevo.txt' creado")