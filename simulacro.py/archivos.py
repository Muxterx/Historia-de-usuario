import csv
import os
from datetime import datetime

# Rutas de archivos
ARCHIVO_PRODUCTOS = "productos.csv"
ARCHIVO_VENTAS = "ventas.csv"

def crear_archivos_si_no_existen():
    """Crear archivos CSV si no existen"""
    if not os.path.exists(ARCHIVO_PRODUCTOS):
        with open(ARCHIVO_PRODUCTOS, 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(['ID', 'Nombre', 'Marca', 'Categoria', 'Precio', 'Stock', 'Garantia'])
    
    if not os.path.exists(ARCHIVO_VENTAS):
        with open(ARCHIVO_VENTAS, 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(['ID_Venta', 'Cliente', 'Tipo_Cliente', 'ID_Producto', 'Nombre_Producto', 
                           'Cantidad', 'Precio_Unitario', 'Descuento', 'Total', 'Fecha'])

def guardar_productos(productos):
    """Guardar todos los productos en el archivo CSV"""
    try:
        with open(ARCHIVO_PRODUCTOS, 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(['ID', 'Nombre', 'Marca', 'Categoria', 'Precio', 'Stock', 'Garantia'])
            
            for id_producto, datos in productos.items():
                writer.writerow([
                    id_producto,
                    datos['nombre'],
                    datos['marca'],
                    datos['categoria'],
                    datos['precio'],
                    datos['stock'],
                    datos['garantia']
                ])
        return True
    except Exception as e:
        print(f"Error al guardar productos: {e}")
        return False

def cargar_productos():
    """Cargar productos desde el archivo CSV"""
    productos = {}
    try:
        if os.path.exists(ARCHIVO_PRODUCTOS):
            with open(ARCHIVO_PRODUCTOS, 'r', encoding='utf-8') as archivo:
                reader = csv.DictReader(archivo)
                for fila in reader:
                    id_producto = fila['ID']
                    productos[id_producto] = {
                        'nombre': fila['Nombre'],
                        'marca': fila['Marca'],
                        'categoria': fila['Categoria'],
                        'precio': float(fila['Precio']),
                        'stock': int(fila['Stock']),
                        'garantia': int(fila['Garantia'])
                    }
    except Exception as e:
        print(f"Error al cargar productos: {e}")
    
    return productos

def guardar_venta(venta):
    """Agregar una nueva venta al archivo CSV"""
    try:
        with open(ARCHIVO_VENTAS, 'a', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow([
                venta['id_venta'],
                venta['cliente'],
                venta['tipo_cliente'],
                venta['id_producto'],
                venta['nombre_producto'],
                venta['cantidad'],
                venta['precio_unitario'],
                venta['descuento'],
                venta['total'],
                venta['fecha']
            ])
        return True
    except Exception as e:
        print(f"Error al guardar venta: {e}")
        return False

def cargar_ventas():
    """Cargar todas las ventas desde el archivo CSV"""
    ventas = []
    try:
        if os.path.exists(ARCHIVO_VENTAS):
            with open(ARCHIVO_VENTAS, 'r', encoding='utf-8') as archivo:
                reader = csv.DictReader(archivo)
                for fila in reader:
                    ventas.append({
                        'id_venta': fila['ID_Venta'],
                        'cliente': fila['Cliente'],
                        'tipo_cliente': fila['Tipo_Cliente'],
                        'id_producto': fila['ID_Producto'],
                        'nombre_producto': fila['Nombre_Producto'],
                        'cantidad': int(fila['Cantidad']),
                        'precio_unitario': float(fila['Precio_Unitario']),
                        'descuento': float(fila['Descuento']),
                        'total': float(fila['Total']),
                        'fecha': fila['Fecha']
                    })
    except Exception as e:
        print(f"Error al cargar ventas: {e}")
    
    return ventas