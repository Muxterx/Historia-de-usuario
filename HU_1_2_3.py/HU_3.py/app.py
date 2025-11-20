"""
Sistema de Inventario Avanzado - Aplicación Principal
Gestión completa de inventario con persistencia en CSV
"""

import servicios
import archivos


def validar_numero_positivo(mensaje, tipo=float):
    """
    Solicita y valida que el usuario ingrese un número positivo.
    
    Parámetros:
        mensaje (str): Mensaje a mostrar al usuario
        tipo (type): Tipo de dato esperado (float o int)
    
    Retorna:
        float o int: Número válido ingresado
    """
    while True:
        try:
            valor = tipo(input(mensaje))
            if valor < 0:
                print("Error: El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print(f"Error: Debe ingresar un número válido.")


def opcion_agregar(inventario):
    """Maneja la opción de agregar producto."""
    print("\n--- AGREGAR PRODUCTO ---")
    
    nombre = input("Nombre del producto: ").strip()
    
    if not nombre:
        print("Error: El nombre no puede estar vacío.")
        return
    
    precio = validar_numero_positivo("Precio: $", float)
    cantidad = validar_numero_positivo("Cantidad: ", int)
    
    if servicios.agregar_producto(inventario, nombre, precio, cantidad):
        print(f"\nProducto '{nombre}' agregado exitosamente.")
    else:
        print(f"\nError: El producto '{nombre}' ya existe en el inventario.")


def opcion_mostrar(inventario):
    """Maneja la opción de mostrar inventario."""
    print("\n--- INVENTARIO COMPLETO ---")
    servicios.mostrar_inventario(inventario)


def opcion_buscar(inventario):
    """Maneja la opción de buscar producto."""
    print("\n--- BUSCAR PRODUCTO ---")
    
    nombre = input("Nombre del producto a buscar: ").strip()
    producto = servicios.buscar_producto(inventario, nombre)
    
    if producto:
        print("\nProducto encontrado:")
        print(f"  Nombre: {producto['nombre']}")
        print(f"  Precio: ${producto['precio']:.2f}")
        print(f"  Cantidad: {producto['cantidad']}")
    else:
        print(f"\nProducto '{nombre}' no encontrado.")


def opcion_actualizar(inventario):
    """Maneja la opción de actualizar producto."""
    print("\n--- ACTUALIZAR PRODUCTO ---")
    
    nombre = input("Nombre del producto a actualizar: ").strip()
    producto = servicios.buscar_producto(inventario, nombre)
    
    if not producto:
        print(f"\nProducto '{nombre}' no encontrado.")
        return
    
    print(f"\nProducto actual:")
    print(f"  Precio: ${producto['precio']:.2f}")
    print(f"  Cantidad: {producto['cantidad']}")
    
    print("\nDejar en blanco para no modificar.")
    
    # Solicitar nuevo precio
    precio_input = input("Nuevo precio (Enter para mantener): ").strip()
    nuevo_precio = None
    if precio_input:
        try:
            nuevo_precio = float(precio_input)
            if nuevo_precio < 0:
                print("Error: El precio no puede ser negativo. Se mantiene el actual.")
                nuevo_precio = None
        except ValueError:
            print("Error: Precio inválido. Se mantiene el actual.")
            nuevo_precio = None
    
    # Solicitar nueva cantidad
    cantidad_input = input("Nueva cantidad (Enter para mantener): ").strip()
    nueva_cantidad = None
    if cantidad_input:
        try:
            nueva_cantidad = int(cantidad_input)
            if nueva_cantidad < 0:
                print("Error: La cantidad no puede ser negativa. Se mantiene la actual.")
                nueva_cantidad = None
        except ValueError:
            print("Error: Cantidad inválida. Se mantiene la actual.")
            nueva_cantidad = None
    
    if nuevo_precio is None and nueva_cantidad is None:
        print("\nNo se realizaron cambios.")
        return
    
    servicios.actualizar_producto(inventario, nombre, nuevo_precio, nueva_cantidad)
    print(f"\nProducto '{nombre}' actualizado exitosamente.")


def opcion_eliminar(inventario):
    """Maneja la opción de eliminar producto."""
    print("\n--- ELIMINAR PRODUCTO ---")
    
    nombre = input("Nombre del producto a eliminar: ").strip()
    
    confirmacion = input(f"¿Está seguro de eliminar '{nombre}'? (S/N): ").strip().upper()
    
    if confirmacion != 'S':
        print("\nEliminación cancelada.")
        return
    
    if servicios.eliminar_producto(inventario, nombre):
        print(f"\nProducto '{nombre}' eliminado exitosamente.")
    else:
        print(f"\nProducto '{nombre}' no encontrado.")


def opcion_estadisticas(inventario):
    """Maneja la opción de ver estadísticas."""
    print("\n--- ESTADISTICAS ---")
    servicios.mostrar_estadisticas(inventario)


def opcion_guardar_csv(inventario):
    """Maneja la opción de guardar a CSV."""
    print("\n--- GUARDAR INVENTARIO EN CSV ---")
    
    ruta = input("Ruta del archivo (ej: inventario.csv): ").strip()
    
    if not ruta:
        print("Error: Debe especificar una ruta.")
        return
    
    archivos.guardar_csv(inventario, ruta)


def opcion_cargar_csv(inventario):
    """Maneja la opción de cargar desde CSV."""
    print("\n--- CARGAR INVENTARIO DESDE CSV ---")
    
    ruta = input("Ruta del archivo a cargar: ").strip()
    
    if not ruta:
        print("Error: Debe especificar una ruta.")
        return
    
    try:
        productos_cargados, filas_invalidas = archivos.cargar_csv(ruta)
        
        if not productos_cargados:
            print("\nNo se cargaron productos válidos.")
            if filas_invalidas > 0:
                print(f"Filas inválidas omitidas: {filas_invalidas}")
            return
        
        print(f"\nSe encontraron {len(productos_cargados)} productos válidos.")
        if filas_invalidas > 0:
            print(f"Filas inválidas omitidas: {filas_invalidas}")
        
        # Preguntar si sobrescribir o fusionar
        if inventario:
            print(f"\nEl inventario actual tiene {len(inventario)} productos.")
            opcion = input("¿Sobrescribir inventario actual? (S/N): ").strip().upper()
            
            if opcion == 'S':
                inventario.clear()
                inventario.extend(productos_cargados)
                print(f"\nInventario reemplazado. Total de productos: {len(inventario)}")
            else:
                print("\nFusionando inventarios...")
                print("Política: Si el producto existe, se actualiza precio y se suma cantidad.")
                
                productos_agregados = archivos.fusionar_inventarios(inventario, productos_cargados)
                productos_actualizados = len(productos_cargados) - productos_agregados
                
                print(f"\nFusión completada:")
                print(f"  Productos nuevos agregados: {productos_agregados}")
                print(f"  Productos actualizados: {productos_actualizados}")
                print(f"  Total de productos en inventario: {len(inventario)}")
        else:
            inventario.extend(productos_cargados)
            print(f"\nInventario cargado. Total de productos: {len(inventario)}")
    
    except FileNotFoundError as e:
        print(f"\nError: {e}")
    except UnicodeDecodeError:
        print("\nError: El archivo no tiene una codificación válida.")
    except Exception as e:
        print(f"\nError al cargar archivo: {e}")


def mostrar_menu():
    """Muestra el menú principal."""
    print("\n" + "=" * 70)
    print("SISTEMA DE INVENTARIO AVANZADO")
    print("=" * 70)
    print("1. Agregar producto")
    print("2. Mostrar inventario")
    print("3. Buscar producto")
    print("4. Actualizar producto")
    print("5. Eliminar producto")
    print("6. Ver estadísticas")
    print("7. Guardar inventario en CSV")
    print("8. Cargar inventario desde CSV")
    print("9. Salir")
    print("=" * 70)


def main():
    """Función principal del programa."""
    inventario = []
    
    print("Bienvenido al Sistema de Inventario Avanzado")
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\nSeleccione una opción (1-9): ").strip()
            
            if opcion == '1':
                opcion_agregar(inventario)
            
            elif opcion == '2':
                opcion_mostrar(inventario)
            
            elif opcion == '3':
                opcion_buscar(inventario)
            
            elif opcion == '4':
                opcion_actualizar(inventario)
            
            elif opcion == '5':
                opcion_eliminar(inventario)
            
            elif opcion == '6':
                opcion_estadisticas(inventario)
            
            elif opcion == '7':
                opcion_guardar_csv(inventario)
            
            elif opcion == '8':
                opcion_cargar_csv(inventario)
            
            elif opcion == '9':
                print("\nGracias por usar el Sistema de Inventario.")
                print("Cerrando programa...")
                break
            
            else:
                print("\nError: Opción inválida. Seleccione un número del 1 al 9.")
        
        except KeyboardInterrupt:
            print("\n\nInterrupción detectada. Cerrando programa...")
            break
        
        except Exception as e:
            print(f"\nError inesperado: {e}")
            print("El programa continuará ejecutándose.")


if __name__ == "__main__":
    main()