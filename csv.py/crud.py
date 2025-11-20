import csv
import os

class CRUD:
    def crear_archivo(self,archivo):
        if not os.path.exists(archivo):
            with open(archivo, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "nombre", "edad"])
    
    def obtener_nuevo_id(self,archivo):
        with open(archivo, "r")as f:
            filas = list(csv.reader(f))
            if len(filas) <= 1:
                return 1
            ultimo_id=int(filas[-1][0])
            return ultimo_id + 1
    
    def crear(self,archivo,nombre,edad):
        id_nuevo= self.obtener_nuevo_id(archivo)
        with open(archivo,"a", newline="") as f:
            writer= csv.writer(f)
            writer.writerow([id_nuevo,nombre,edad]) 
            return id_nuevo
        
    def listar(self,archivo):      
        with open(archivo,"r")as f:
            reader= csv.reader(f)
            next (reader)
            return list(reader)