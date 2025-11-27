# archivos.py
# ===========
# Este módulo maneja la lectura y escritura de archivos CSV
# CSV = Comma Separated Values (Valores Separados por Comas)

"""
Módulo de manejo de archivos CSV para el sistema de inventario.
Permite guardar y cargar el inventario desde archivos.
"""


def guardar_csv(inventario, ruta, incluir_header=True):
    """
    Guarda el inventario en un archivo CSV.
    
    ¿POR QUÉ EXISTE?
    - Persistencia: los datos sobreviven al cerrar el programa
    - Portabilidad: CSV se puede abrir en Excel, Google Sheets, etc.
    - Respaldo: protege contra pérdida de datos
    
    ¿QUÉ ES UN ARCHIVO CSV?
    nombre,precio,cantidad
    Manzana,1.50,100
    Banana,0.75,150
    
    Args:
        inventario (list): Lista de diccionarios con productos
        ruta (str): Ruta del archivo donde guardar (ej: "inventario.csv")
        incluir_header (bool): Si incluir encabezados. Default True.
    
    Returns:
        tuple: (éxito: bool, mensaje: str)
    """
    # Validar que el inventario no esté vacío
    if not inventario:
        return (False, "❌ El inventario está vacío. No hay nada que guardar.")
    
    try:
        # Abrir archivo en modo escritura ('w')
        # encoding='utf-8' para soportar caracteres especiales (ñ, tildes)
        # ¿Qué es 'with'? Abre el archivo y lo cierra automáticamente al terminar
        with open(ruta, 'w', encoding='utf-8') as archivo:
            
            # Escribir encabezado si se solicita
            if incluir_header:
                archivo.write("nombre,precio,cantidad\n")
            
            # Escribir cada producto como una línea
            for producto in inventario:
                # Crear línea CSV: nombre,precio,cantidad
                linea = f"{producto['nombre']},{producto['precio']},{producto['cantidad']}\n"
                archivo.write(linea)
        
        # Si llegamos aquí, todo salió bien
        return (True, f"✅ Inventario guardado exitosamente en: {ruta}")
    
    except PermissionError:
        # Error: no tenemos permiso para escribir en esa ubicación
        return (False, f"❌ Error de permisos: No se puede escribir en '{ruta}'")
    
    except OSError as e:
        # Error del sistema operativo (disco lleno, ruta inválida, etc.)
        return (False, f"❌ Error del sistema: {e}")
    
    except Exception as e:
        # Cualquier otro error inesperado
        return (False, f"❌ Error inesperado al guardar: {e}")


def cargar_csv(ruta):
    """
    Carga productos desde un archivo CSV.
    
    ¿POR QUÉ EXISTE?
    - Recuperar datos guardados anteriormente
    - Importar datos de otros sistemas (Excel, etc.)
    - Continuar trabajando donde lo dejamos
    
    VALIDACIONES QUE HACE:
    1. ¿El archivo existe?
    2. ¿Tiene el encabezado correcto?
    3. ¿Cada fila tiene 3 columnas?
    4. ¿El precio es un número válido?
    5. ¿La cantidad es un número entero?
    6. ¿No hay valores negativos?
    
    Args:
        ruta (str): Ruta del archivo CSV a cargar
    
    Returns:
        tuple: (productos: list, errores: int, mensaje: str)
               productos = lista de diccionarios cargados
               errores = cantidad de filas inválidas omitidas
               mensaje = descripción del resultado
    """
    productos_cargados = []  # Lista para almacenar productos válidos
    filas_invalidas = 0      # Contador de filas con errores
    
    try:
        # Abrir archivo en modo lectura ('r')
        with open(ruta, 'r', encoding='utf-8') as archivo:
            
            # Leer todas las líneas del archivo
            lineas = archivo.readlines()
            
            # Verificar que el archivo no esté vacío
            if not lineas:
                return ([], 0, "⚠️ El archivo está vacío.")
            
            # Verificar encabezado (primera línea)
            # strip() elimina espacios y saltos de línea
            # lower() convierte a minúsculas para comparar
            encabezado = lineas[0].strip().lower()
            
            if encabezado != "nombre,precio,cantidad":
                return ([], 0, "❌ Encabezado inválido. Se esperaba: nombre,precio,cantidad")
            
            # Procesar cada línea de datos (desde la línea 1, después del encabezado)
            for numero_linea, linea in enumerate(lineas[1:], start=2):
                # enumerate da el índice, start=2 porque línea 1 es encabezado
                
                # Ignorar líneas vacías
                if not linea.strip():
                    continue
                
                try:
                    # Separar la línea por comas
                    partes = linea.strip().split(',')
                    
                    # Validar que tenga exactamente 3 columnas
                    if len(partes) != 3:
                        filas_invalidas += 1
                        continue  # Saltar esta fila
                    
                    # Extraer y convertir valores
                    nombre = partes[0].strip()
                    precio = float(partes[1].strip())
                    cantidad = int(partes[2].strip())
                    
                    # Validar que no sean negativos
                    if precio < 0 or cantidad < 0:
                        filas_invalidas += 1
                        continue
                    
                    # Validar que el nombre no esté vacío
                    if not nombre:
                        filas_invalidas += 1
                        continue
                    
                    # Todo válido, agregar a la lista
                    productos_cargados.append({
                        "nombre": nombre,
                        "precio": precio,
                        "cantidad": cantidad
                    })
                    
                except ValueError:
                    # Error al convertir precio a float o cantidad a int
                    filas_invalidas += 1
                    continue
            
            # Preparar mensaje de resultado
            if productos_cargados:
                mensaje = f"✅ Se cargaron {len(productos_cargados)} productos."
                if filas_invalidas > 0:
                    mensaje += f" ({filas_invalidas} filas inválidas omitidas)"
            else:
                mensaje = "⚠️ No se pudo cargar ningún producto válido."
            
            return (productos_cargados, filas_invalidas, mensaje)
    
    except FileNotFoundError:
        # El archivo no existe
        return ([], 0, f"❌ Archivo no encontrado: '{ruta}'")
    
    except UnicodeDecodeError:
        # Error de codificación (archivo en formato incorrecto)
        return ([], 0, "❌ Error de codificación. El archivo no está en formato UTF-8.")
    
    except PermissionError:
        # No tenemos permiso para leer el archivo
        return ([], 0, f"❌ Sin permiso para leer: '{ruta}'")
    
    except Exception as e:
        # Cualquier otro error
        return ([], 0, f"❌ Error al cargar archivo: {e}")


def fusionar_inventarios(inventario_actual, productos_nuevos):
    """
    Fusiona productos nuevos con el inventario actual.
    
    ¿POR QUÉ EXISTE?
    - Al cargar un CSV, el usuario puede elegir fusionar en vez de sobrescribir
    - Permite combinar datos de múltiples fuentes
    
    POLÍTICA DE FUSIÓN:
    - Si el producto ya existe: suma las cantidades y actualiza el precio
    - Si es nuevo: lo agrega
    
    Args:
        inventario_actual (list): Inventario existente en memoria
        productos_nuevos (list): Productos cargados del CSV
    
    Returns:
        dict: Resumen de la fusión (agregados, actualizados)
    """
    agregados = 0
    actualizados = 0
    
    for producto_nuevo in productos_nuevos:
        # Buscar si ya existe en el inventario actual
        existente = None
        for producto in inventario_actual:
            if producto["nombre"].lower() == producto_nuevo["nombre"].lower():
                existente = producto
                break
        
        if existente:
            # Actualizar: sumar cantidades, actualizar precio al nuevo
            existente["cantidad"] += producto_nuevo["cantidad"]
            existente["precio"] = producto_nuevo["precio"]
            actualizados += 1
        else:
            # Agregar como nuevo
            inventario_actual.append(producto_nuevo)
            agregados += 1
    
    return {
        "agregados": agregados,
        "actualizados": actualizados
    }