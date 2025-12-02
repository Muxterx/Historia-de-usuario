

import csv
import os
from datetime import datetime, timedelta
from empleados import buscar_empleado, calcular_meses_trabajados, calcular_dias_disponibles

def crear_archivo_vacaciones():
    
    if not os.path.exists("data"):
        os.makedirs("data")
    
    if not os.path.exists("data/vacaciones.csv"):
        with open("data/vacaciones.csv", "w", newline="") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["empleado_id", "nombre_empleado", "fecha_inicio_vacaciones", 
                                "fecha_fin_vacaciones", "dias_calculados", "estado", "mes", "anio"])
            


def contar_dias_sin_domingos(fecha_inicio, fecha_fin):
   
    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
    
    dias = 0
    fecha_actual = inicio
    
    while fecha_actual <= fin:
        
        if fecha_actual.weekday() != 6:
            dias = dias + 1
        fecha_actual = fecha_actual + timedelta(days=1)
    
    return dias


def registrar_solicitud():
    
    crear_archivo_vacaciones()
    
    print("\n--- NUEVA SOLICITUD DE VACACIONES ---")
    
    empleado_id = input("ID del empleado: ")
    
   
    empleado = buscar_empleado(empleado_id)
    if empleado == None:
        print("Error: No se encontro el empleado")
        return
    
    print("Empleado: " + empleado["nombre_completo"])
    
   
    meses = calcular_meses_trabajados(empleado["fecha_inicio_contrato"])
    if meses < 6:
        print("Error: El empleado no puede solicitar vacaciones")
        print("Meses trabajados: " + str(meses))
        print("Minimo requerido: 6 meses")
        return
    
   
    dias_disponibles = calcular_dias_disponibles(empleado_id)
    print("Dias disponibles: " + str(dias_disponibles))
    
    if dias_disponibles <= 0:
        print("Error: No tiene dias disponibles")
        return
    
   
    print("\nFormato: YYYY-MM-DD")
    fecha_inicio = input("Fecha inicio vacaciones: ")
    fecha_fin = input("Fecha fin vacaciones: ")
    
   
    try:
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
    except:
        print("Error: Formato de fecha invalido")
        return
    
    if fin < inicio:
        print("Error: La fecha fin debe ser posterior a la fecha inicio")
        return
    
    
    dias_solicitados = contar_dias_sin_domingos(fecha_inicio, fecha_fin)
    print("Dias solicitados (sin domingos): " + str(dias_solicitados))
    
    if dias_solicitados > dias_disponibles:
        print("Error: No tiene suficientes dias")
        print("Solicitados: " + str(dias_solicitados))
        print("Disponibles: " + str(dias_disponibles))
        return
    
    
    confirmar = input("\nConfirmar solicitud? (S/N): ")
    if confirmar.upper() != "S":
        print("Solicitud cancelada")
        return
    
   
    archivo = open("data/vacaciones.csv", "a", newline="")
    escritor = csv.writer(archivo)
    escritor.writerow([
        empleado_id,
        empleado["nombre_completo"],
        fecha_inicio,
        fecha_fin,
        dias_solicitados,
        "PENDIENTE",
        inicio.month,
        inicio.year
    ])
    archivo.close()
    
    print("\nSolicitud registrada!")
    print("Estado: PENDIENTE")


def cargar_vacaciones():
    
    crear_archivo_vacaciones()
    
    archivo = open("data/vacaciones.csv", "r")
    lector = csv.DictReader(archivo)
    
    vacaciones = []
    for fila in lector:
        vacaciones.append(fila)
    
    archivo.close()
    return vacaciones


def guardar_vacaciones(vacaciones):
    
    archivo = open("data/vacaciones.csv", "w", newline="")
    escritor = csv.writer(archivo)
    escritor.writerow(["empleado_id", "nombre_empleado", "fecha_inicio_vacaciones", 
                      "fecha_fin_vacaciones", "dias_calculados", "estado", "mes", "anio"])
    
    for v in vacaciones:
        escritor.writerow([
            v["empleado_id"],
            v["nombre_empleado"],
            v["fecha_inicio_vacaciones"],
            v["fecha_fin_vacaciones"],
            v["dias_calculados"],
            v["estado"],
            v["mes"],
            v["anio"]
        ])
    
    archivo.close()


def aprobar_rechazar():
   
    print("\n--- APROBAR/RECHAZAR SOLICITUDES ---")
    
    vacaciones = cargar_vacaciones()
    
    
    pendientes = []
    for v in vacaciones:
        if v["estado"] == "PENDIENTE":
            pendientes.append(v)
    
    if len(pendientes) == 0:
        print("No hay solicitudes pendientes")
        return
    
   
    print("\nSolicitudes pendientes:")
    print("")
    
    numero = 1
    for p in pendientes:
        print(str(numero) + ". " + p["nombre_empleado"] + " - " + p["fecha_inicio_vacaciones"] + " a " + p["fecha_fin_vacaciones"] + " (" + p["dias_calculados"] + " dias)")
        numero = numero + 1
    
    
    try:
        seleccion = int(input("\nNumero de solicitud (0 para cancelar): "))
    except:
        print("Debe ingresar un numero")
        return
    
    if seleccion == 0:
        return
    
    if seleccion < 1 or seleccion > len(pendientes):
        print("Numero invalido")
        return
    
    solicitud = pendientes[seleccion - 1]
    
    print("\nSolicitud seleccionada:")
    print("Empleado: " + solicitud["nombre_empleado"])
    print("Periodo: " + solicitud["fecha_inicio_vacaciones"] + " a " + solicitud["fecha_fin_vacaciones"])
    print("Dias: " + solicitud["dias_calculados"])
    
    print("\n1. Aprobar")
    print("2. Rechazar")
    print("0. Cancelar")
    
    accion = input("\nOpcion: ")
    
    if accion == "1":
        nuevo_estado = "APROBADA"
    elif accion == "2":
        nuevo_estado = "RECHAZADA"
    else:
        return
    
 
    for v in vacaciones:
        if (v["empleado_id"] == solicitud["empleado_id"] and 
            v["fecha_inicio_vacaciones"] == solicitud["fecha_inicio_vacaciones"] and
            v["estado"] == "PENDIENTE"):
            v["estado"] = nuevo_estado
    
    guardar_vacaciones(vacaciones)
    
    print("\nSolicitud " + nuevo_estado)


def ver_historial():
   
    print("\n--- HISTORIAL DE VACACIONES ---")
    
    empleado_id = input("ID del empleado: ")
    
    empleado = buscar_empleado(empleado_id)
    if empleado == None:
        print("No se encontro el empleado")
        return
    
    print("\nHistorial de: " + empleado["nombre_completo"])
    
    vacaciones = cargar_vacaciones()
    
    
    historial = []
    for v in vacaciones:
        if v["empleado_id"] == empleado_id:
            historial.append(v)
    
    if len(historial) == 0:
        print("No tiene solicitudes registradas")
        return
    
    print("")
    print("Inicio      | Fin         | Dias | Estado")
    print("-" * 50)
    
    total_aprobados = 0
    for h in historial:
        print(h["fecha_inicio_vacaciones"] + " | " + h["fecha_fin_vacaciones"] + " | " + h["dias_calculados"] + "    | " + h["estado"])
        if h["estado"] == "APROBADA":
            total_aprobados = total_aprobados + int(h["dias_calculados"])
    
    print("-" * 50)
    print("Total dias aprobados: " + str(total_aprobados))
    print("Dias disponibles: " + str(calcular_dias_disponibles(empleado_id)))


def menu_vacaciones():
   
    while True:
        print("\n--- GESTION DE VACACIONES ---")
        print("1. Registrar solicitud")
        print("2. Aprobar/Rechazar solicitudes")
        print("3. Ver historial de empleado")
        print("0. Volver")
        
        opcion = input("\nOpcion: ")
        
        if opcion == "1":
            registrar_solicitud()
        elif opcion == "2":
            aprobar_rechazar()
        elif opcion == "3":
            ver_historial()
        elif opcion == "0":
            break
        else:
            print("Opcion no valida")
        
        input("\nPresione Enter para continuar...")