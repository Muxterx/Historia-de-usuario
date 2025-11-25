# Importar el módulo de funciones que contiene toda la lógica del negocio
import functions

def menu ():
    """Mostrar menú principal"""
    print("\n" + "="*37)
    print("INVENTORY AND SALES MANAGEMENT SYSTEM")
    print("="*37)
    print("1. Register new book")
    print("2. Show all books")
    print("3. Update book data")
    print("4. Remove book")
    print("5. Registrer new sale")
    print("6. Show sales history")
    print("7. Top 3 best-selling books")
    print("8. Sales by author")
    print("9. Income statement")
    print("10. Inventory performance")
    print("\n0. Exit")
    print("="*37)

def main():
    """Bucle principal de la aplicación"""
    functions.initialize_data() # Cargar datos iniciales y archivos

    # Bucle infinito que mantiene la aplicación corriendo
    while True:
        try:
            menu() # Mostrar opciones al usuario
            opcion = input("Select an option: ").strip()

            # Estructura if-elif para manejar todas las opciones del menú
            # Esta estructura es escalable y fácil de mantener
            if opcion == "1":
                functions.add_book()  # Llamar función especí­fica del CRUD
            
            elif opcion == "2":
                functions.show_inventory() # Función de lectura/consulta

            elif opcion == "3":
                functions.update_book()  # Función de actualización

            elif opcion == "4":
                functions.remove_book()  # Función de eliminación

            elif opcion == "5":
                functions.add_sale()  # Función de proceso de ventas

            elif opcion == "6":
                functions.show_sales()  # Consulta de historial

            elif opcion == "7":
                functions.top_3_products()  # Reporte analí­tico

            elif opcion == "8":
                functions.sales_by_author()  # Reporte por categoría

            elif opcion == "9":
                functions.income_statement()  # Reporte financiero

            elif opcion == "10":
                functions.inventory_performance()  # Reporte de inventario

            elif opcion == "0":
                print("Leaving the program...")
                break  # Romper el bucle para salir

            else:
                print("\nInvalid option. Please try again")

            # Pausa para que el usuario pueda leer los resultados
            input("\nPress Enter to continue...")

        # Manejo de cualquier error inesperado
        except Exception as e:
            print(f"Unexpected error: {e}")
            print("The system will continue to operate...")  # Sistema resiliente

# Patrón común en Python: ejecutar main() solo si es el script principal
if __name__ == "__main__":
    main()

        