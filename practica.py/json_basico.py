import json
import os 

print ("===JSON BASICO===")

Estudiantes = [
    {'id': 1, 'nombre': 'Lucas', 'Edad': 20},
    {'id': 2, 'nombre': 'Santi', 'Edad':19},
    {'id': 3, 'nombre': 'Samu', 'Edad': 22},
]

with open ('Estudiantes.json', 'w') as f:
    json.dump(Estudiantes,f, indent=5)


print("Datos guardados con exito en Json")

with open('Estudiantes.json', 'r')as f:
    Datos= json.load(f)

print("Datos leidos")

for Estudiante in Datos:
    print(f' {Estudiante['nombre']} - {Estudiante['Edad']}años')