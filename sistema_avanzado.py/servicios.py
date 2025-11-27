# servicios.py
# ============
# Este módulo contiene todas las funciones para manejar el inventario
# CRUD = Create (Crear), Read (Leer), Update (Actualizar), Delete (Eliminar)

"""
Módulo de servicios para el sistema de inventario.
Contiene funciones CRUD y cálculo de estadísticas.
"""


def agregar_producto(inventario, nombre, precio, cantidad):
    """
    Agrega un nuevo producto al inventario.
    
    ¿POR QUÉ EXISTE?
    - Necesitamos una forma de añadir productos nuevos
    - Centraliza la lógica de creación en un solo lugar
    - Valida que no existan duplicados
    
    Args:
        inventario (list): Lista de diccionarios con productos
        nombre (str): Nombre del producto a agregar
        precio (float): Precio unitario del producto
        cantidad (int): Cantidad en stock
    
    Returns:
        bool: True si se agregó exitosamente, False si ya existe
    """
    # Verificar si el producto ya existe (búsqueda insensible a mayúsculas)
    # ¿Por qué lower()? Para que "Manzana" y "manzana" se consideren iguales
    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            return False  # Ya existe, no agregar duplicado
    
    # Crear el diccionario del nuevo producto
    # ¿Por qué diccionario? Permite acceder por nombre de campo: producto["precio"]
    nuevo_producto = {
        "nombre": nombre,
        "precio": float(precio),  # Asegurar que sea float
        "cantidad": int(cantidad)  # Asegurar que sea int
    }
    
    # Agregar a la lista
    inventario.append(nuevo_producto)
    return True


def mostrar_inventario(inventario):
    """
    Muestra todos los productos del inventario de forma formateada.
    
    ¿POR QUÉ EXISTE?
    - El usuario necesita ver qué productos hay
    - Presenta la información de forma legible y profesional
    
    Args:
        inventario (list): Lista de diccionarios con productos
    
    Returns:
        str: Mensaje con el inventario formateado o mensaje de vacío
    """
    # Verificar si está vacío
    if not inventario:  # Lista vacía = False en Python
        return "📦 El inventario está vacío."
    
    # Construir la salida formateada
    # ¿Por qué usar f-strings? Facilitan formatear texto con variables
    lineas = []
    lineas.append("\n" + "=" * 70)
    lineas.append(f"{'INVENTARIO ACTUAL':^70}")  # ^70 = centrado en 70 caracteres
    lineas.append("=" * 70)
    
    # Encabezados de columna
    # :<20 = alineado izquierda, 20 caracteres
    # :>12 = alineado derecha, 12 caracteres
    lineas.append(f"{'Nombre':<25} {'Precio':>12} {'Cantidad':>12} {'Subtotal':>15}")
    lineas.append("-" * 70)
    
    # Mostrar cada producto
    for producto in inventario:
        nombre = producto["nombre"]
        precio = producto["precio"]
        cantidad = producto["cantidad"]
        subtotal = precio * cantidad  # Valor total de ese producto
        
        # :.2f = 2 decimales para números flotantes
        lineas.append(f"{nombre:<25} ${precio:>11.2f} {cantidad:>12} ${subtotal:>14.2f}")
    
    lineas.append("=" * 70)
    
    return "\n".join(lineas)  # Unir todas las líneas con saltos de línea


def buscar_producto(inventario, nombre):
    """
    Busca un producto por nombre en el inventario.
    
    ¿POR QUÉ EXISTE?
    - Necesitamos encontrar productos específicos
    - Usado internamente por actualizar y eliminar
    - El usuario puede buscar para ver detalles
    
    Args:
        inventario (list): Lista de diccionarios con productos
        nombre (str): Nombre del producto a buscar
    
    Returns:
        dict or None: El diccionario del producto si existe, None si no
    """
    # Recorrer la lista buscando coincidencia
    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            return producto  # Retorna el diccionario completo
    
    return None  # No encontrado


def actualizar_producto(inventario, nombre, nuevo_precio=None, nueva_cantidad=None):
    """
    Actualiza el precio y/o cantidad de un producto existente.
    
    ¿POR QUÉ EXISTE?
    - Los precios cambian con el tiempo
    - El stock aumenta o disminuye
    - Permite modificar sin eliminar y recrear
    
    ¿QUÉ SON nuevo_precio=None?
    - Parámetros opcionales: si no se pasan, quedan en None
    - Permite actualizar solo lo que necesitamos
    
    Args:
        inventario (list): Lista de diccionarios con productos
        nombre (str): Nombre del producto a actualizar
        nuevo_precio (float, optional): Nuevo precio. Default None.
        nueva_cantidad (int, optional): Nueva cantidad. Default None.
    
    Returns:
        bool: True si se actualizó, False si no se encontró el producto
    """
    # Primero buscar el producto
    producto = buscar_producto(inventario, nombre)
    
    if producto is None:
        return False  # No existe, no se puede actualizar
    
    # Actualizar solo los campos que se proporcionaron
    # ¿Por qué "is not None"? Porque el precio podría ser 0 (válido pero False en if)
    if nuevo_precio is not None:
        producto["precio"] = float(nuevo_precio)
    
    if nueva_cantidad is not None:
        producto["cantidad"] = int(nueva_cantidad)
    
    return True


def eliminar_producto(inventario, nombre):
    """
    Elimina un producto del inventario por nombre.
    
    ¿POR QUÉ EXISTE?
    - Productos descontinuados deben removerse
    - Errores al agregar deben poder corregirse
    
    Args:
        inventario (list): Lista de diccionarios con productos
        nombre (str): Nombre del producto a eliminar
    
    Returns:
        bool: True si se eliminó, False si no se encontró
    """
    # Buscar el producto
    producto = buscar_producto(inventario, nombre)
    
    if producto is None:
        return False
    
    # Eliminar de la lista
    # ¿Por qué remove()? Elimina el primer elemento que coincida
    inventario.remove(producto)
    return True


def calcular_estadisticas(inventario):
    """
    Calcula estadísticas del inventario.
    
    ¿POR QUÉ EXISTE?
    - El negocio necesita conocer el valor de su inventario
    - Identificar productos clave (más caro, mayor stock)
    - Tomar decisiones informadas
    
    Args:
        inventario (list): Lista de diccionarios con productos
    
    Returns:
        dict or None: Diccionario con estadísticas, None si inventario vacío
    """
    if not inventario:
        return None
    
    # Calcular unidades totales
    # sum() suma todos los elementos de una lista/generador
    unidades_totales = sum(p["cantidad"] for p in inventario)
    
    # Calcular valor total del inventario
    # Usando lambda (función anónima de una línea)
    # ¿Qué es lambda? Una forma corta de escribir funciones simples
    calcular_subtotal = lambda p: p["precio"] * p["cantidad"]
    valor_total = sum(calcular_subtotal(p) for p in inventario)
    
    # Encontrar producto más caro
    # max() con key= encuentra el máximo según un criterio
    producto_mas_caro = max(inventario, key=lambda p: p["precio"])
    
    # Encontrar producto con mayor stock
    producto_mayor_stock = max(inventario, key=lambda p: p["cantidad"])
    
    # Retornar como diccionario para fácil acceso
    return {
        "unidades_totales": unidades_totales,
        "valor_total": valor_total,
        "producto_mas_caro": {
            "nombre": producto_mas_caro["nombre"],
            "precio": producto_mas_caro["precio"]
        },
        "producto_mayor_stock": {
            "nombre": producto_mayor_stock["nombre"],
            "cantidad": producto_mayor_stock["cantidad"]
        },
        "total_productos": len(inventario)  # Cantidad de productos diferentes
    }


def mostrar_estadisticas(inventario):
    """
    Muestra las estadísticas de forma formateada.
    
    Args:
        inventario (list): Lista de diccionarios con productos
    
    Returns:
        str: Estadísticas formateadas
    """
    stats = calcular_estadisticas(inventario)
    
    if stats is None:
        return "📊 No hay estadísticas disponibles. El inventario está vacío."
    
    lineas = []
    lineas.append("\n" + "=" * 50)
    lineas.append(f"{'📊 ESTADÍSTICAS DEL INVENTARIO':^50}")
    lineas.append("=" * 50)
    lineas.append(f"Total de productos diferentes: {stats['total_productos']}")
    lineas.append(f"Unidades totales en stock:     {stats['unidades_totales']}")
    lineas.append(f"Valor total del inventario:    ${stats['valor_total']:,.2f}")
    lineas.append("-" * 50)
    lineas.append(f"💰 Producto más caro:")
    lineas.append(f"   {stats['producto_mas_caro']['nombre']} - ${stats['producto_mas_caro']['precio']:.2f}")
    lineas.append(f"📦 Producto con mayor stock:")
    lineas.append(f"   {stats['producto_mayor_stock']['nombre']} - {stats['producto_mayor_stock']['cantidad']} unidades")
    lineas.append("=" * 50)
    
    return "\n".join(lineas)