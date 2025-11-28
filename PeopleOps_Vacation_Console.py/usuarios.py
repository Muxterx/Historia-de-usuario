

import csv
import os

def verificar_login():
    
    intentos = 0
    max_intentos = 3
    
    while intentos < max_intentos:
        print("\n--- INICIO DE SESION ---")
        usuario = input("Usuario: ")
        contrasena = input("Contrasena: ")
        
    
        if os.path.exists("data/usuarios.csv"):
            archivo = open("data/usuarios.csv", "r")
            lector = csv.DictReader(archivo)
            
            for fila in lector:
                if fila["usuario"] == usuario and fila["contrasena"] == contrasena:
                    archivo.close()
                    print("\nLogin exitoso! Bienvenido " + usuario)
                    return True
            
            archivo.close()
        
        intentos = intentos + 1
        print("Usuario o contrasena incorrectos.")
        print("Intentos restantes: " + str(max_intentos - intentos))
    
    print("Demasiados intentos fallidos.")
    return False