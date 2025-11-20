from crud import CRUD

crud =CRUD()
archivo = "datos.csv"

crud.crear_archivo(archivo)
while True:
    print("\n--- menu ---")
    print("1. crear persona ")
    print("2. listar personas")
    print("3.actualizar persona")
    print("4. salir")

    opcion= input("elijas una opcion: ")
    if opcion=="1":
        nombre= input("ingresa el nombre: ")
        edad= input("ingresa la edad: ")
        id_creado= crud.crear(archivo,nombre,edad)
        print(f"persona craeda con id: {id_creado}")
    elif opcion=="2":
        datos= crud.listar(archivo)
        print("\n---LISTADO---")
        for fila in datos:
            print(f"ID: {fila[0]} | Nombre: {fila[1]} | Edad: {fila[2]}")
    elif opcion=="3":
        print(f"\n--- actualizar persona ---")
        id_actualizar= input("ingresa el id de la persona a actualizar: ")
        nombre_nuevo= input("ingresa el nuevo nombre: ")
        edad_nueva= input("ingresa la nueva edad: ")
        if id_actualizar in datos:
          datos[id_actualizar]['nombre']= nombre_nuevo
          datos[id_actualizar]['edad']= edad_nueva
        print("actualizando..")
        print("persona actualizada")
    elif opcion =="4":
        print("saliendo")
        break
    else:
        print("opcion no valida")

