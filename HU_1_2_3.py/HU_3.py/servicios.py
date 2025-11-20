"""
Módulo de servicios para gestión de inventario.
Contiene funciones CRUD y cálculo de estadísticas.
"""

def agregar_producto(inventario, nombre, precio, cantidad):
    """
    Agrega un nuevo producto al inventario.
    
    Parámetros:
        inventario (list): Lista de diccionarios con los productos
        nombre (str): Nombre del producto
        precio (float): Precio unitario del producto
        cantidad (int): Cantidad en stock
    
    Retorna:
        bool: True si se agregó exitosamente, False si ya existe
    """
    # Verificar si el producto ya existe
    if buscar_producto(inventario, nombre) is not None:
        return False
    
    # Crear nuevo producto
    producto = {
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
    }
    
    inventario.append(producto)
    return True


def mostrar_inventario(inventario):
    """
    Muestra todos los productos del inventario en formato tabla.
    
    Parámetros:
        inventario (list): Lista de diccionarios con los productos
    
    Retorna:
        None
    """
    if not inventario:
        print("\nEl inventario está vacío.")
        return
    
    print("\n" + "=" * 70)
    print(f"{'NOMBRE':<30} {'PRECIO':>15} {'CANTIDAD':>15}")
    print("=" * 70)
    
    for producto in inventario:
        print(f"{producto['nombre']:<30} ${producto['precio']:>14.2f} {producto['cantidad']:>15}")
    
    print("=" * 70)


def buscar_producto(inventario, nombre):
    """
    Busca un producto por nombre en el inventario.
    
    Parámetros:
        inventario (list): Lista de diccionarios con los productos
        nombre (str): Nombre del producto a buscar
    
    Retorna:
        dict o None: Diccionario del producto si existe, None si no se encuentra
    """
    nombre_lower = nombre.lower()
    
    for producto in inventario:
        if producto["nombre"].lower() == nombre_lower:
            return producto
    
    return None


def actualizar_producto(inventario, nombre, nuevo_precio=None, nueva_cantidad=None):
    """
    Actualiza el precio y/o cantidad de un producto existente.
    
    Parámetros:
        inventario (list): Lista de diccionarios con los productos
        nombre (str): Nombre del producto a actualizar
        nuevo_precio (float, opcional): Nuevo precio del producto
        nueva_cantidad (int, opcional): Nueva cantidad del producto
    
    Retorna:
        bool: True si se actualizó, False si no se encontró el producto
    """
    producto = buscar_producto(inventario, nombre)
    
    if producto is None:
        return False
    
    # Actualizar solo los campos proporcionados
    if nuevo_precio is not None:
        producto["precio"] = nuevo_precio
    
    if nueva_cantidad is not None:
        producto["cantidad"] = nueva_cantidad
    
    return True


def eliminar_producto(inventario, nombre):
    """
    Elimina un producto del inventario.
    
    Parámetros:
        inventario (list): Lista de diccionarios con los productos
        nombre (str): Nombre del producto a eliminar
    
    Retorna:
        bool: True si se eliminó, False si no se encontró
    """
    producto = buscar_producto(inventario, nombre)
    
    if producto is None:
        return False
    
    inventario.remove(producto)
    return True


def calcular_estadisticas(inventario):
    """
    Calcula estadísticas generales del inventario.
    
    Parámetros:
        inventario (list): Lista de diccionarios con los productos
    
    Retorna:
        dict: Diccionario con las estadísticas calculadas:
            - unidades_totales: Total de unidades en stock
            - valor_total: Valor total del inventario
            - producto_mas_caro: Tupla (nombre, precio)
            - producto_mayor_stock: Tupla (nombre, cantidad)
    """
    if not inventario:
        return None
    
    # Función lambda para calcular subtotal
    subtotal = lambda p: p["precio"] * p["cantidad"]
    
    # Calcular unidades totales
    unidades_totales = sum(p["cantidad"] for p in inventario)
    
    # Calcular valor total del inventario
    valor_total = sum(subtotal(p) for p in inventario)
    
    # Encontrar producto más caro
    producto_caro = max(inventario, key=lambda p: p["precio"])
    producto_mas_caro = (producto_caro["nombre"], producto_caro["precio"])
    
    # Encontrar producto con mayor stock
    producto_stock = max(inventario, key=lambda p: p["cantidad"])
    producto_mayor_stock = (producto_stock["nombre"], producto_stock["cantidad"])
    
    estadisticas = {
        "unidades_totales": unidades_totales,
        "valor_total": valor_total,
        "producto_mas_caro": producto_mas_caro,
        "producto_mayor_stock": producto_mayor_stock
    }
    
    return estadisticas


def mostrar_estadisticas(inventario):
    """
    Calcula y muestra las estadísticas del inventario en formato legible.
    
    Parámetros:
        inventario (list): Lista de diccionarios con los productos
    
    Retorna:
        None
    """
    estadisticas = calcular_estadisticas(inventario)
    
    if estadisticas is None:
        print("\nNo hay datos para calcular estadísticas.")
        return
    
    print("\n" + "=" * 70)
    print("ESTADISTICAS DEL INVENTARIO")
    print("=" * 70)
    print(f"Unidades totales en stock: {estadisticas['unidades_totales']}")
    print(f"Valor total del inventario: ${estadisticas['valor_total']:.2f}")
    print(f"Producto más caro: {estadisticas['producto_mas_caro'][0]} "
          f"(${estadisticas['producto_mas_caro'][1]:.2f})")
    print(f"Producto con mayor stock: {estadisticas['producto_mayor_stock'][0]} "
          f"({estadisticas['producto_mayor_stock'][1]} unidades)")
    print("=" * 70)