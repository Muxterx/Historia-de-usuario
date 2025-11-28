

import os
from usuarios import verificar_login
from empleados import menu_empleados
from vacaciones import menu_vacaciones
"""from reportes import menu_reportes"""

def crear_archivo_usuarios():
   
    if not os.path.exists("data"):
        os.makedirs("data")
    
    if not os.path.exists("data/usuarios.csv"):
        archivo = open("data/usuarios.csv", "w", newline="")
        archivo.write("usuario,contrasena,rol\n")
        archivo.write("santi,mux,administrador\n")
        archivo.close()
        print("Archivo de usuarios creado")


def menu_principal():
    
    while True:
        print("\n========================================")
        print("   PEOPLEOPS VACATION CONSOLE - RIWI")
        print("========================================")
        print("")
        print("1. Gestion de Empleados")
        print("2. Gestion de Vacaciones")
        print("3. Reportes")
        print("0. Salir")
        
        opcion = input("\nSeleccione una opcion: ")
        
        if opcion == "1":
            menu_empleados()
        elif opcion == "2":
            menu_vacaciones()
        elif opcion == "3":
            menu_reportes()
        elif opcion == "0":
            confirmar = input("Seguro que desea salir? (S/N): ")
            if confirmar.upper() == "S":
                print("\nHasta pronto!")
                break
        else:
            print("Opcion no valida")



print("========================================")
print("   PEOPLEOPS VACATION CONSOLE")
print("   Sistema de Gestion de Vacaciones")
print("========================================")


crear_archivo_usuarios()


if verificar_login():
    input("\nPresione Enter para continuar...")
    menu_principal()
else:
    print("\nNo se pudo iniciar sesion")

print("\nPrograma terminado")