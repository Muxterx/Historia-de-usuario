# app.py
# ======
# Archivo principal que ejecuta el programa
# Contiene el menú y la interacción con el usuario

"""
Sistema de Inventario Avanzado
Archivo principal con menú interactivo.

Ejecutar: python app.py
"""

# Importar nuestros módulos personalizados
# ¿Por qué importar? Para usar las funciones que creamos en otros archivos
import servicios
import archivos


def mostrar_menu():
    """Muestra el menú principal del sistema."""
    print("\n" + "=" * 50)
    print(" SISTEMA DE INVENTARIO AVANZADO")
    print("=" * 50)
    print("1.  Agregar producto")
    print("2.  Mostrar inventario")
    print("3.  Buscar producto")
    print("4.   Actualizar producto")
    print("5.   Eliminar producto")
    print("6.  Ver estadísticas")
    print("7.  Guardar en CSV")
    print("8.  Cargar desde CSV")
    print("9.  Salir")
    print("-" * 50)


def obtener_numero(mensaje, tipo="float", permitir_cero=True):
    """
    Solicita un número al usuario con validación.
    
    ¿POR QUÉ EXISTE?
    - Evita que el programa falle con entradas inválidas
    - Reutilizable para precio y cantidad
    
    Args:
        mensaje (str): Texto a mostrar al usuario
        tipo (str): "float" o "int"
        permitir_cero (bool): Si se permite el valor 0
    
    Returns:
        float o int: El número validado
    """
    while True:  # Repetir hasta obtener valor válido
        try:
            entrada = input(mensaje)
            
            if tipo == "int":
                valor = int(entrada)
            else:
                valor = float(entrada)
            
            # Validar que no sea negativo
            if valor < 0:
                print("❌ El valor no puede ser negativo.")
                continue
            
            # Validar cero si no está permitido
            if not permitir_cero and valor == 0:
                print("❌ El valor no puede ser cero.")
                continue
            
            return valor
            
        except ValueError:
            print("❌ Por favor ingresa un número válido.")


def opcion_agregar(inventario):
    """Maneja la opción de agregar producto."""
    print("\n--- AGREGAR PRODUCTO ---")
    
    nombre = input("Nombre del producto: ").strip()
    if not nombre:
        print("❌ El nombre no puede estar vacío.")
        return
    
    precio = obtener_numero("Precio: $", tipo="float", permitir_cero=False)
    cantidad = obtener_numero("Cantidad: ", tipo="int")
    
    # Intentar agregar
    if servicios.agregar_producto(inventario, nombre, precio, cantidad):
        print(f"✅ Producto '{nombre}' agregado exitosamente.")
    else:
        print(f"⚠️ El producto '{nombre}' ya existe en el inventario.")


def opcion_mostrar(inventario):
    """Maneja la opción de mostrar inventario."""
    print(servicios.mostrar_inventario(inventario))


def opcion_buscar(inventario):
    """Maneja la opción de buscar producto."""
    print("\n--- BUSCAR PRODUCTO ---")
    
    nombre = input("Nombre a buscar: ").strip()
    if not nombre:
        print("❌ Debes ingresar un nombre.")
        return
    
    producto = servicios.buscar_producto(inventario, nombre)
    
    if producto:
        print("\n✅ Producto encontrado:")
        print(f"   Nombre:   {producto['nombre']}")
        print(f"   Precio:   ${producto['precio']:.2f}")
        print(f"   Cantidad: {producto['cantidad']}")
        print(f"   Subtotal: ${producto['precio'] * producto['cantidad']:.2f}")
    else:
        print(f"❌ Producto '{nombre}' no encontrado.")


def opcion_actualizar(inventario):
    """Maneja la opción de actualizar producto."""
    print("\n--- ACTUALIZAR PRODUCTO ---")
    
    nombre = input("Nombre del producto a actualizar: ").strip()
    if not nombre:
        print("❌ Debes ingresar un nombre.")
        return
    
    # Verificar que existe
    if not servicios.buscar_producto(inventario, nombre):
        print(f"❌ Producto '{nombre}' no encontrado.")
        return
    
    print("\n¿Qué deseas actualizar?")
    print("1. Solo precio")
    print("2. Solo cantidad")
    print("3. Ambos")
    
    opcion = input("Opción: ").strip()
    
    nuevo_precio = None
    nueva_cantidad = None
    
    if opcion in ["1", "3"]:
        nuevo_precio = obtener_numero("Nuevo precio: $", tipo="float", permitir_cero=False)
    
    if opcion in ["2", "3"]:
        nueva_cantidad = obtener_numero("Nueva cantidad: ", tipo="int")
    
    if opcion not in ["1", "2", "3"]:
        print("❌ Opción no válida.")
        return
    
    if servicios.actualizar_producto(inventario, nombre, nuevo_precio, nueva_cantidad):
        print(f"✅ Producto '{nombre}' actualizado exitosamente.")
    else:
        print("❌ Error al actualizar.")


def opcion_eliminar(inventario):
    """Maneja la opción de eliminar producto."""
    print("\n--- ELIMINAR PRODUCTO ---")
    
    nombre = input("Nombre del producto a eliminar: ").strip()
    if not nombre:
        print("❌ Debes ingresar un nombre.")
        return
    
    # Confirmar eliminación
    confirmacion = input(f"¿Seguro que deseas eliminar '{nombre}'? (S/N): ").strip().upper()
    
    if confirmacion != "S":
        print("Operación cancelada.")
        return
    
    if servicios.eliminar_producto(inventario, nombre):
        print(f"✅ Producto '{nombre}' eliminado exitosamente.")
    else:
        print(f"❌ Producto '{nombre}' no encontrado.")


def opcion_estadisticas(inventario):
    """Maneja la opción de ver estadísticas."""
    print(servicios.mostrar_estadisticas(inventario))


def opcion_guardar(inventario):
    """Maneja la opción de guardar en CSV."""
    print("\n--- GUARDAR EN CSV ---")
    
    ruta = input("Nombre del archivo (ejemplo: inventario.csv): ").strip()
    if not ruta:
        ruta = "inventario.csv"  # Valor por defecto
    
    # Asegurar extensión .csv
    if not ruta.endswith(".csv"):
        ruta += ".csv"
    
    exito, mensaje = archivos.guardar_csv(inventario, ruta)
    print(mensaje)


def opcion_cargar(inventario):
    """Maneja la opción de cargar desde CSV."""
    print("\n--- CARGAR DESDE CSV ---")
    
    ruta = input("Ruta del archivo a cargar: ").strip()
    if not ruta:
        print("❌ Debes ingresar una ruta.")
        return
    
    # Intentar cargar
    productos, errores, mensaje = archivos.cargar_csv(ruta)
    print(mensaje)
    
    # Si no se cargó nada, terminar
    if not productos:
        return
    
    # Preguntar qué hacer con los datos
    print(f"\nSe encontraron {len(productos)} productos válidos.")
    
    if inventario:  # Si ya hay productos en el inventario
        print("\n¿Qué deseas hacer?")
        print("S - Sobrescribir inventario actual (perder datos actuales)")
        print("F - Fusionar con inventario actual (combinar datos)")
        print("C - Cancelar")
        
        opcion = input("Opción: ").strip().upper()
        
        if opcion == "S":
            # Sobrescribir: vaciar y agregar nuevos
            inventario.clear()
            inventario.extend(productos)
            print(f"✅ Inventario reemplazado. {len(productos)} productos cargados.")
            
        elif opcion == "F":
            # Fusionar
            resultado = archivos.fusionar_inventarios(inventario, productos)
            print(f"✅ Fusión completada:")
            print(f"   - Productos nuevos agregados: {resultado['agregados']}")
            print(f"   - Productos existentes actualizados: {resultado['actualizados']}")
            
        else:
            print("Operación cancelada.")
    else:
        # Inventario vacío, solo agregar
        inventario.extend(productos)
        print(f"✅ {len(productos)} productos cargados al inventario.")


def main():
    """
    Función principal del programa.
    
    ¿POR QUÉ EXISTE main()?
    - Organiza el punto de entrada del programa
    - Permite importar el módulo sin ejecutar el menú
    - Práctica estándar en Python
    """
    # Inicializar inventario como lista vacía
    # Esta es la "base de datos" en memoria
    inventario = []
    
    print("\n" + "🌟" * 25)
    print("  ¡Bienvenido al Sistema de Inventario!")
    print("🌟" * 25)
    
    # Bucle principal del programa
    # ¿Por qué while True? El programa sigue corriendo hasta que el usuario elija salir
    while True:
        try:
            # Mostrar menú
            mostrar_menu()
            
            # Obtener opción del usuario
            opcion = input("Selecciona una opción (1-9): ").strip()
            
            # Procesar opción con estructura match-case (Python 3.10+)
            # Si tienes Python < 3.10, usa if-elif-else
            if opcion == "1":
                opcion_agregar(inventario)
            elif opcion == "2":
                opcion_mostrar(inventario)
            elif opcion == "3":
                opcion_buscar(inventario)
            elif opcion == "4":
                opcion_actualizar(inventario)
            elif opcion == "5":
                opcion_eliminar(inventario)
            elif opcion == "6":
                opcion_estadisticas(inventario)
            elif opcion == "7":
                opcion_guardar(inventario)
            elif opcion == "8":
                opcion_cargar(inventario)
            elif opcion == "9":
                # Confirmar salida
                print("\n¿Deseas guardar antes de salir? (S/N): ", end="")
                if input().strip().upper() == "S":
                    opcion_guardar(inventario)
                print("\n👋 ¡Gracias por usar el Sistema de Inventario!")
                print("   Hasta pronto.\n")
                break  # Salir del bucle while
            else:
                print("❌ Opción no válida. Por favor ingresa un número del 1 al 9.")
        
        except KeyboardInterrupt:
            # Si el usuario presiona Ctrl+C
            print("\n\n⚠️ Programa interrumpido por el usuario.")
            break
        
        except Exception as e:
            # Cualquier error inesperado
            print(f"\n❌ Error inesperado: {e}")
            print("   El programa continuará ejecutándose.")


# Esta condición verifica si estamos ejecutando el archivo directamente
# ¿Por qué? Si alguien importa app.py, no queremos que se ejecute el menú automáticamente
if __name__ == "__main__":
    main()