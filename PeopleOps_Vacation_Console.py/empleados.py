

import csv
import os
from datetime import datetime

def crear_archivo_empleados():
    
    if not os.path.exists("data"):
        os.makedirs("data")
    
    if not os.path.exists("data/empleados.csv"):
        archivo = open("data/empleados.csv", "w", newline="")
        escritor = csv.writer(archivo)
        escritor.writerow(["empleado_id", "nombre_completo", "cargo", "area", "fecha_inicio_contrato"])
        archivo.close()


def registrar_empleado():

    crear_archivo_empleados()
    
    print("\n--- REGISTRAR EMPLEADO ---")
    
    nombre = input("Nombre completo: ")
    if nombre == "":
        print("Error: El nombre no puede estar vacio")
        return
    
    cargo = input("Cargo: ")
    if cargo == "":
        print("Error: El cargo no puede estar vacio")
        return
    
    area = input("Area: ")
    if area == "":
        print("Error: El area no puede estar vacia")
        return
    
    print("Formato de fecha: YYYY-MM-DD (ejemplo: 2024-06-15)")
    fecha = input("Fecha de inicio de contrato: ")
    

    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
        if fecha_obj > datetime.now():
            print("Error: La fecha no puede ser futura")
            return
    except:
        print("Error: Formato de fecha invalido")
        return
    
    
    empleado_id = "EMP" + datetime.now().strftime("%Y%m%d%H%M%S")
    
    
    archivo = open("data/empleados.csv", "a", newline="")
    escritor = csv.writer(archivo)
    escritor.writerow([empleado_id, nombre, cargo, area, fecha])
    archivo.close()
    
    print("\nEmpleado registrado!")
    print("ID asignado: " + empleado_id)


def listar_empleados():
    
    crear_archivo_empleados()
    
    print("\n--- LISTA DE EMPLEADOS ---")
    
    archivo = open("data/empleados.csv", "r")
    lector = csv.DictReader(archivo)
    
    empleados = []
    for fila in lector:
        empleados.append(fila)
    archivo.close()
    
    if len(empleados) == 0:
        print("No hay empleados registrados.")
        return
    
    print("")
    print("ID                   | Nombre                | Cargo              | Area")
    print("-" * 80)
    
    for emp in empleados:
        print(emp["empleado_id"] + " | " + emp["nombre_completo"][:20] + " | " + emp["cargo"][:18] + " | " + emp["area"])
    
    print("-" * 80)
    print("Total: " + str(len(empleados)) + " empleados")


def buscar_empleado(empleado_id):
    
    crear_archivo_empleados()
    
    archivo = open("data/empleados.csv", "r")
    lector = csv.DictReader(archivo)
    
    for fila in lector:
        if fila["empleado_id"] == empleado_id:
            archivo.close()
            return fila
    
    archivo.close()
    return None


def calcular_meses_trabajados(fecha_contrato):
    
    fecha_inicio = datetime.strptime(fecha_contrato, "%Y-%m-%d")
    fecha_actual = datetime.now()
    
    meses = (fecha_actual.year - fecha_inicio.year) * 12
    meses = meses + (fecha_actual.month - fecha_inicio.month)
    
    if fecha_actual.day < fecha_inicio.day:
        meses = meses - 1
    
    if meses < 0:
        meses = 0
    
    return meses


def obtener_dias_usados(empleado_id):
    
    if not os.path.exists("data/vacaciones.csv"):
        return 0
    
    archivo = open("data/vacaciones.csv", "r")
    lector = csv.DictReader(archivo)
    
    dias_usados = 0
    for fila in lector:
        if fila["empleado_id"] == empleado_id and fila["estado"] == "APROBADA":
            dias_usados = dias_usados + int(fila["dias_calculados"])
    
    archivo.close()
    return dias_usados


def calcular_dias_disponibles(empleado_id):
    
    empleado = buscar_empleado(empleado_id)
    
    if empleado == None:
        return 0
    
    meses = calcular_meses_trabajados(empleado["fecha_inicio_contrato"])
    dias_acumulados = meses * 1.5
    dias_usados = obtener_dias_usados(empleado_id)
    
    dias_disponibles = dias_acumulados - dias_usados
    
    if dias_disponibles < 0:
        dias_disponibles = 0
    
    return dias_disponibles


def consultar_empleado():
    
    print("\n--- CONSULTAR EMPLEADO ---")
    
    empleado_id = input("Ingrese el ID del empleado: ")
    
    empleado = buscar_empleado(empleado_id)
    
    if empleado == None:
        print("No se encontro el empleado con ese ID")
        return
    
    meses = calcular_meses_trabajados(empleado["fecha_inicio_contrato"])
    dias_acumulados = meses * 1.5
    dias_usados = obtener_dias_usados(empleado_id)
    dias_disponibles = calcular_dias_disponibles(empleado_id)
    
    print("\n=== DATOS DEL EMPLEADO ===")
    print("ID: " + empleado["empleado_id"])
    print("Nombre: " + empleado["nombre_completo"])
    print("Cargo: " + empleado["cargo"])
    print("Area: " + empleado["area"])
    print("Fecha contrato: " + empleado["fecha_inicio_contrato"])
    
    print("\n=== VACACIONES ===")
    print("Meses trabajados: " + str(meses))
    print("Dias acumulados: " + str(dias_acumulados))
    print("Dias usados: " + str(dias_usados))
    print("Dias disponibles: " + str(dias_disponibles))
    
    if meses >= 6:
        print("\nPuede solicitar vacaciones")
    else:
        print("\nNo puede solicitar vacaciones (minimo 6 meses)")
        print("Faltan " + str(6 - meses) + " meses")


def menu_empleados():
    
    while True:
        print("\n--- GESTION DE EMPLEADOS ---")
        print("1. Registrar empleado")
        print("2. Listar empleados")
        print("3. Consultar empleado")
        print("0. Volver")
        
        opcion = input("\nOpcion: ")
        
        if opcion == "1":
            registrar_empleado()
        elif opcion == "2":
            listar_empleados()
        elif opcion == "3":
            consultar_empleado()
        elif opcion == "0":
            break
        else:
            print("Opcion no valida")
        
        input("\nPresione Enter para continuar...")