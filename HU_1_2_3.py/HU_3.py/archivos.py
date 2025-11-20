"""
Módulo para gestión de persistencia en archivos CSV.
Contiene funciones para guardar y cargar el inventario.
"""

import csv
import os


def guardar_csv(inventario, ruta, incluir_header=True):
    """
    Guarda el inventario en un archivo CSV.
    
    Parámetros:
        inventario (list): Lista de diccionarios con los productos
        ruta (str): Ruta del archivo donde guardar
        incluir_header (bool): Si se debe incluir encabezado (por defecto True)
    
    Retorna:
        bool: True si se guardó correctamente, False si hubo error
    """
    # Validar que el inventario no esté vacío
    if not inventario:
        print("\nError: El inventario está vacío. No hay nada que guardar.")
        return False
    
    try:
        # Abrir archivo en modo escritura
        with open(ruta, 'w', newline='', encoding='utf-8') as archivo:
            # Definir los campos del CSV
            campos = ['nombre', 'precio', 'cantidad']
            
            # Crear escritor CSV
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            
            # Escribir encabezado si se solicita
            if incluir_header:
                escritor.writeheader()
            
            # Escribir todos los productos
            escritor.writerows(inventario)
        
        print(f"\nInventario guardado exitosamente en: {ruta}")
        return True
    
    except PermissionError:
        print(f"\nError: No tiene permisos para escribir en '{ruta}'.")
        return False
    
    except IOError as e:
        print(f"\nError de escritura: {e}")
        return False
    
    except Exception as e:
        print(f"\nError inesperado al guardar: {e}")
        return False


def cargar_csv(ruta):
    """
    Carga productos desde un archivo CSV.
    
    Parámetros:
        ruta (str): Ruta del archivo a cargar
    
    Retorna:
        tuple: (lista_productos, filas_invalidas)
            - lista_productos: Lista de diccionarios con productos válidos
            - filas_invalidas: Número de filas que no pudieron cargarse
    """
    productos = []
    filas_invalidas = 0
    
    # Verificar que el archivo existe
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"El archivo '{ruta}' no existe.")
    
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            
            # Leer encabezado
            try:
                encabezado = next(lector)
            except StopIteration:
                print("\nError: El archivo está vacío.")
                return productos, filas_invalidas
            
            # Validar encabezado
            encabezado_esperado = ['nombre', 'precio', 'cantidad']
            if encabezado != encabezado_esperado:
                print(f"\nError: Encabezado inválido. Se esperaba {encabezado_esperado}")
                print(f"Se encontró: {encabezado}")
                return productos, filas_invalidas
            
            # Procesar cada fila
            numero_linea = 1
            for fila in lector:
                numero_linea += 1
                
                # Validar que tenga exactamente 3 columnas
                if len(fila) != 3:
                    print(f"Advertencia: Línea {numero_linea} tiene {len(fila)} columnas (se esperan 3). Omitida.")
                    filas_invalidas += 1
                    continue
                
                try:
                    nombre = fila[0].strip()
                    precio = float(fila[1])
                    cantidad = int(fila[2])
                    
                    # Validar que no sean negativos
                    if precio < 0:
                        print(f"Advertencia: Línea {numero_linea} tiene precio negativo. Omitida.")
                        filas_invalidas += 1
                        continue
                    
                    if cantidad < 0:
                        print(f"Advertencia: Línea {numero_linea} tiene cantidad negativa. Omitida.")
                        filas_invalidas += 1
                        continue
                    
                    # Validar que el nombre no esté vacío
                    if not nombre:
                        print(f"Advertencia: Línea {numero_linea} tiene nombre vacío. Omitida.")
                        filas_invalidas += 1
                        continue
                    
                    # Agregar producto válido
                    producto = {
                        "nombre": nombre,
                        "precio": precio,
                        "cantidad": cantidad
                    }
                    productos.append(producto)
                
                except ValueError as e:
                    print(f"Advertencia: Línea {numero_linea} tiene formato inválido ({e}). Omitida.")
                    filas_invalidas += 1
                    continue
        
        return productos, filas_invalidas
    
    except UnicodeDecodeError:
        print("\nError: El archivo no tiene codificación UTF-8 válida.")
        raise
    
    except Exception as e:
        print(f"\nError inesperado al leer el archivo: {e}")
        raise


def fusionar_inventarios(inventario_actual, productos_nuevos):
    """
    Fusiona productos nuevos con el inventario actual.
    Si un producto ya existe, actualiza precio y suma cantidades.
    
    Parámetros:
        inventario_actual (list): Inventario existente
        productos_nuevos (list): Productos a fusionar
    
    Retorna:
        int: Número de productos agregados (no actualizados)
    """
    from servicios import buscar_producto
    
    productos_agregados = 0
    
    for producto_nuevo in productos_nuevos:
        producto_existente = buscar_producto(inventario_actual, producto_nuevo["nombre"])
        
        if producto_existente is not None:
            # El producto ya existe: actualizar
            producto_existente["precio"] = producto_nuevo["precio"]
            producto_existente["cantidad"] += producto_nuevo["cantidad"]
        else:
            # El producto no existe: agregar
            inventario_actual.append(producto_nuevo)
            productos_agregados += 1
    
    return productos_agregados