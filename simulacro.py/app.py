import funciones

def mostrar_menu():
    """Mostrar menú principal"""
    print("\n" + "="*65)
    print("  TIENDA DE ELECTRÓNICA - SISTEMA DE GESTIÓN DE INVENTARIO Y VENTAS")
    print("="*65)
    print("  1. Agregar nuevo producto")
    print("  2. Ver todos los productos")
    print("  3. Actualizar producto")
    print("  4. Eliminar producto")
    print("  5. Registrar nueva venta")
    print("  6. Ver historial de ventas")
    print("  7. Top 3 productos más vendidos")
    print("  8. Ventas por marca")
    print("  9. Reporte de ingresos")
    print("  10. Rendimiento del inventario")
    print("\n  0. Salir")
    print("="*65)

def main():
    """Bucle principal de la aplicación"""
    print("\n🔧 Inicializando sistema...")
    funciones.inicializar_datos()
    print("✅ ¡Sistema listo!\n")
    
    while True:
        try:
            mostrar_menu()
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == '1':
                funciones.agregar_producto()
            
            elif opcion == '2':
                funciones.ver_productos()
            
            elif opcion == '3':
                funciones.actualizar_producto()
            
            elif opcion == '4':
                funciones.eliminar_producto()
            
            elif opcion == '5':
                funciones.registrar_venta()
            
            elif opcion == '6':
                funciones.ver_ventas()
            
            elif opcion == '7':
                funciones.top_3_productos()
            
            elif opcion == '8':
                funciones.ventas_por_marca()
            
            elif opcion == '9':
                funciones.calcular_ingresos()
            
            elif opcion == '10':
                funciones.rendimiento_inventario()
            
            elif opcion == '0':
                print("\n ¡Gracias por usar el sistema. Hasta luego!")
                break
            
            else:
                print("\n Opción inválida. Por favor intente nuevamente.")
            
            input("\nPresione Enter para continuar...")
            
        except KeyboardInterrupt:
            print("\n\n Operación cancelada por el usuario")
            confirmar = input("¿Desea salir? (si/no): ").lower()
            if confirmar == 'si':
                print("\n👋 ¡Hasta luego!")
                break
        
        except Exception as e:
            print(f"\n Error inesperado: {e}")
            print("El sistema continuará funcionando...")

if __name__ == "__main__":
    main()