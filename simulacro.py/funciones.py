from datetime import datetime
import archivos

# Estructuras de datos globales
productos = {}
ventas = []
contador_ventas = 1

# Descuentos por tipo de cliente
DESCUENTOS_CLIENTE = {
    'regular': 0,
    'miembro': 10,
    'vip': 20,
    'empleado': 30
}

def inicializar_datos():
    """Inicializar el sistema con datos precargados"""
    global productos, ventas, contador_ventas
    
    archivos.crear_archivos_si_no_existen()
    productos = archivos.cargar_productos()
    ventas = archivos.cargar_ventas()
    
    # Configurar contador de ventas
    if ventas:
        ultimo_id = int(ventas[-1]['id_venta'].replace('V', ''))
        contador_ventas = ultimo_id + 1
    
    # Si no hay productos, crear inventario inicial
    if not productos:
        productos = {
            'P001': {
                'nombre': 'iPhone 15 Pro',
                'marca': 'Apple',
                'categoria': 'Smartphone',
                'precio': 999.99,
                'stock': 50,
                'garantia': 12
            },
            'P002': {
                'nombre': 'Samsung Galaxy S24',
                'marca': 'Samsung',
                'categoria': 'Smartphone',
                'precio': 849.99,
                'stock': 45,
                'garantia': 12
            },
            'P003': {
                'nombre': 'MacBook Pro M3',
                'marca': 'Apple',
                'categoria': 'Laptop',
                'precio': 1999.99,
                'stock': 30,
                'garantia': 24
            },
            'P004': {
                'nombre': 'Dell XPS 15',
                'marca': 'Dell',
                'categoria': 'Laptop',
                'precio': 1499.99,
                'stock': 25,
                'garantia': 24
            },
            'P005': {
                'nombre': 'Sony WH-1000XM5',
                'marca': 'Sony',
                'categoria': 'Audífonos',
                'precio': 399.99,
                'stock': 100,
                'garantia': 6
            }
        }
        archivos.guardar_productos(productos)

# ===== CRUD DE PRODUCTOS =====

def agregar_producto():
    """Agregar un nuevo producto al inventario"""
    try:
        print("\n=== AGREGAR NUEVO PRODUCTO ===")
        
        # Generar nuevo ID
        if productos:
            ultimo_id = max([int(pid.replace('P', '')) for pid in productos.keys()])
            nuevo_id = f"P{str(ultimo_id + 1).zfill(3)}"
        else:
            nuevo_id = "P001"
        
        nombre = input("Nombre del producto: ").strip()
        if not nombre:
            print("❌ El nombre no puede estar vacío")
            return
        
        marca = input("Marca: ").strip()
        if not marca:
            print("❌ La marca no puede estar vacía")
            return
        
        categoria = input("Categoría: ").strip()
        if not categoria:
            print("❌ La categoría no puede estar vacía")
            return
        
        precio = float(input("Precio unitario: $"))
        if precio <= 0:
            print("❌ El precio debe ser positivo")
            return
        
        stock = int(input("Stock inicial: "))
        if stock < 0:
            print("❌ El stock no puede ser negativo")
            return
        
        garantia = int(input("Garantía (meses): "))
        if garantia < 0:
            print("❌ La garantía no puede ser negativa")
            return
        
        productos[nuevo_id] = {
            'nombre': nombre,
            'marca': marca,
            'categoria': categoria,
            'precio': precio,
            'stock': stock,
            'garantia': garantia
        }
        
        archivos.guardar_productos(productos)
        print(f"✅ Producto agregado exitosamente con ID: {nuevo_id}")
        
    except ValueError:
        print("❌ Entrada inválida. Por favor ingrese los datos correctos.")
    except Exception as e:
        print(f"❌ Error al agregar producto: {e}")

def ver_productos():
    """Mostrar todos los productos"""
    if not productos:
        print("\n❌ No hay productos en el inventario")
        return
    
    print("\n" + "="*110)
    print(f"{'ID':<8} {'Nombre':<30} {'Marca':<15} {'Categoría':<15} {'Precio':<10} {'Stock':<8} {'Garantía':<8}")
    print("="*110)
    
    for id_producto, datos in productos.items():
        print(f"{id_producto:<8} {datos['nombre']:<30} {datos['marca']:<15} {datos['categoria']:<15} "
              f"${datos['precio']:<9.2f} {datos['stock']:<8} {datos['garantia']:<8}")
    
    print("="*110)

def actualizar_producto():
    """Actualizar un producto existente"""
    try:
        ver_productos()
        id_producto = input("\nIngrese ID del producto a actualizar: ").strip().upper()
        
        if id_producto not in productos:
            print("❌ Producto no encontrado")
            return
        
        print(f"\nActualizando: {productos[id_producto]['nombre']}")
        print("(Presione Enter para mantener el valor actual)")
        
        nombre = input(f"Nombre [{productos[id_producto]['nombre']}]: ").strip()
        marca = input(f"Marca [{productos[id_producto]['marca']}]: ").strip()
        categoria = input(f"Categoría [{productos[id_producto]['categoria']}]: ").strip()
        precio = input(f"Precio [${productos[id_producto]['precio']}]: ").strip()
        stock = input(f"Stock [{productos[id_producto]['stock']}]: ").strip()
        garantia = input(f"Garantía [{productos[id_producto]['garantia']} meses]: ").strip()
        
        if nombre:
            productos[id_producto]['nombre'] = nombre
        if marca:
            productos[id_producto]['marca'] = marca
        if categoria:
            productos[id_producto]['categoria'] = categoria
        if precio:
            productos[id_producto]['precio'] = float(precio)
        if stock:
            productos[id_producto]['stock'] = int(stock)
        if garantia:
            productos[id_producto]['garantia'] = int(garantia)
        
        archivos.guardar_productos(productos)
        print("✅ Producto actualizado exitosamente")
        
    except ValueError:
        print("❌ Entrada inválida")
    except Exception as e:
        print(f"❌ Error al actualizar producto: {e}")

def eliminar_producto():
    """Eliminar un producto del inventario"""
    try:
        ver_productos()
        id_producto = input("\nIngrese ID del producto a eliminar: ").strip().upper()
        
        if id_producto not in productos:
            print("❌ Producto no encontrado")
            return
        
        confirmar = input(f"¿Está seguro de eliminar '{productos[id_producto]['nombre']}'? (si/no): ").lower()
        
        if confirmar == 'si':
            del productos[id_producto]
            archivos.guardar_productos(productos)
            print("✅ Producto eliminado exitosamente")
        else:
            print("❌ Eliminación cancelada")
            
    except Exception as e:
        print(f"❌ Error al eliminar producto: {e}")

# ===== GESTIÓN DE VENTAS =====

def registrar_venta():
    """Registrar una nueva venta"""
    global contador_ventas
    
    try:
        print("\n=== REGISTRAR NUEVA VENTA ===")
        
        ver_productos()
        
        cliente = input("\nNombre del cliente: ").strip()
        if not cliente:
            print("❌ El nombre del cliente no puede estar vacío")
            return
        
        print("\nTipos de cliente:")
        for tipo, descuento in DESCUENTOS_CLIENTE.items():
            print(f"  - {tipo}: {descuento}% de descuento")
        
        tipo_cliente = input("Tipo de cliente: ").strip().lower()
        if tipo_cliente not in DESCUENTOS_CLIENTE:
            print("❌ Tipo de cliente inválido")
            return
        
        id_producto = input("ID del producto: ").strip().upper()
        if id_producto not in productos:
            print("❌ Producto no encontrado")
            return
        
        cantidad = int(input("Cantidad: "))
        if cantidad <= 0:
            print("❌ La cantidad debe ser positiva")
            return
        
        # Validar stock
        if productos[id_producto]['stock'] < cantidad:
            print(f"❌ Stock insuficiente. Disponible: {productos[id_producto]['stock']}")
            return
        
        # Calcular venta
        precio_unitario = productos[id_producto]['precio']
        porcentaje_descuento = DESCUENTOS_CLIENTE[tipo_cliente]
        subtotal = precio_unitario * cantidad
        monto_descuento = subtotal * (porcentaje_descuento / 100)
        total = subtotal - monto_descuento
        
        # Crear registro de venta
        id_venta = f"V{str(contador_ventas).zfill(4)}"
        venta = {
            'id_venta': id_venta,
            'cliente': cliente,
            'tipo_cliente': tipo_cliente,
            'id_producto': id_producto,
            'nombre_producto': productos[id_producto]['nombre'],
            'cantidad': cantidad,
            'precio_unitario': precio_unitario,
            'descuento': porcentaje_descuento,
            'total': total,
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Actualizar stock
        productos[id_producto]['stock'] -= cantidad
        
        # Guardar cambios
        ventas.append(venta)
        archivos.guardar_venta(venta)
        archivos.guardar_productos(productos)
        
        contador_ventas += 1
        
        # Mostrar recibo
        print("\n" + "="*50)
        print("RECIBO DE VENTA")
        print("="*50)
        print(f"ID Venta: {id_venta}")
        print(f"Cliente: {cliente} ({tipo_cliente})")
        print(f"Producto: {productos[id_producto]['nombre']}")
        print(f"Cantidad: {cantidad}")
        print(f"Precio Unitario: ${precio_unitario:.2f}")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Descuento: {porcentaje_descuento}% (-${monto_descuento:.2f})")
        print(f"TOTAL: ${total:.2f}")
        print(f"Fecha: {venta['fecha']}")
        print("="*50)
        print("✅ Venta registrada exitosamente")
        
    except ValueError:
        print("❌ Entrada inválida")
    except Exception as e:
        print(f"❌ Error al registrar venta: {e}")

def ver_ventas():
    """Mostrar todas las ventas"""
    if not ventas:
        print("\n❌ No hay ventas registradas")
        return
    
    print("\n" + "="*130)
    print(f"{'ID Venta':<10} {'Cliente':<20} {'Tipo':<12} {'Producto':<30} {'Cant':<6} {'Precio':<10} {'Desc%':<7} {'Total':<10} {'Fecha':<20}")
    print("="*130)
    
    for venta in ventas:
        print(f"{venta['id_venta']:<10} {venta['cliente']:<20} {venta['tipo_cliente']:<12} "
              f"{venta['nombre_producto']:<30} {venta['cantidad']:<6} ${venta['precio_unitario']:<9.2f} "
              f"{venta['descuento']:<6}% ${venta['total']:<9.2f} {venta['fecha']:<20}")
    
    print("="*130)

# ===== REPORTES =====

def top_3_productos():
    """Mostrar top 3 productos más vendidos"""
    print("\n=== TOP 3 PRODUCTOS MÁS VENDIDOS ===")
    
    if not ventas:
        print("❌ No hay datos de ventas disponibles")
        return
    
    # Contar ventas por producto usando lambda
    ventas_por_producto = {}
    for venta in ventas:
        pid = venta['id_producto']
        if pid in ventas_por_producto:
            ventas_por_producto[pid]['cantidad'] += venta['cantidad']
            ventas_por_producto[pid]['ingresos'] += venta['total']
        else:
            ventas_por_producto[pid] = {
                'nombre': venta['nombre_producto'],
                'cantidad': venta['cantidad'],
                'ingresos': venta['total']
            }
    
    # Ordenar por cantidad vendida
    productos_ordenados = sorted(ventas_por_producto.items(), key=lambda x: x[1]['cantidad'], reverse=True)
    
    print(f"\n{'Posición':<10} {'ID Producto':<12} {'Nombre Producto':<35} {'Unidades':<12} {'Ingresos':<12}")
    print("="*85)
    
    for i, (pid, datos) in enumerate(productos_ordenados[:3], 1):
        print(f"{i:<10} {pid:<12} {datos['nombre']:<35} {datos['cantidad']:<12} ${datos['ingresos']:<11.2f}")

def ventas_por_marca():
    """Mostrar ventas agrupadas por marca"""
    print("\n=== VENTAS POR MARCA ===")
    
    if not ventas:
        print("❌ No hay datos de ventas disponibles")
        return
    
    ventas_marca = {}
    
    for venta in ventas:
        pid = venta['id_producto']
        if pid in productos:
            marca = productos[pid]['marca']
            if marca in ventas_marca:
                ventas_marca[marca]['unidades'] += venta['cantidad']
                ventas_marca[marca]['ingresos'] += venta['total']
            else:
                ventas_marca[marca] = {
                    'unidades': venta['cantidad'],
                    'ingresos': venta['total']
                }
    
    print(f"\n{'Marca':<20} {'Unidades Vendidas':<20} {'Ingresos Totales':<20}")
    print("="*60)
    
    for marca, datos in sorted(ventas_marca.items()):
        print(f"{marca:<20} {datos['unidades']:<20} ${datos['ingresos']:<19.2f}")

def calcular_ingresos():
    """Calcular ingresos brutos y netos"""
    print("\n=== REPORTE DE INGRESOS ===")
    
    if not ventas:
        print("❌ No hay datos de ventas disponibles")
        return
    
    # Usando lambda para cálculos
    ingreso_bruto = sum(map(lambda v: v['precio_unitario'] * v['cantidad'], ventas))
    ingreso_neto = sum(map(lambda v: v['total'], ventas))
    descuento_total = ingreso_bruto - ingreso_neto
    
    print(f"\nIngreso Bruto: ${ingreso_bruto:.2f}")
    print(f"Descuentos Totales: -${descuento_total:.2f}")
    print(f"Ingreso Neto: ${ingreso_neto:.2f}")
    print(f"Descuento Promedio: {(descuento_total/ingreso_bruto*100):.2f}%")

def rendimiento_inventario():
    """Mostrar reporte de rendimiento del inventario"""
    print("\n=== REPORTE DE RENDIMIENTO DEL INVENTARIO ===")
    
    print(f"\n{'ID Producto':<12} {'Nombre Producto':<35} {'Stock':<10} {'Vendido':<10} {'Estado':<20}")
    print("="*90)
    
    for pid, datos in productos.items():
        # Contar unidades vendidas
        vendido = sum([v['cantidad'] for v in ventas if v['id_producto'] == pid])
        
        # Determinar estado
        if datos['stock'] == 0:
            estado = "SIN STOCK"
        elif datos['stock'] < 10:
            estado = "STOCK BAJO"
        elif vendido > datos['stock']:
            estado = "ALTA DEMANDA"
        else:
            estado = "NORMAL"
        
        print(f"{pid:<12} {datos['nombre']:<35} {datos['stock']:<10} {vendido:<10} {estado:<20}")