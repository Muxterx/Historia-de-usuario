# SISTEMA DE INVENTARIO - SEMANA 2
# Estudiante aprendiendo control de flujo y listas

# Lista para guardar los productos
inventario = []

# Bucle principal - el programa sigue hasta que el usuario elija salir
while True:
    # Mostrar el menú
    print("\n===== MENÚ DE INVENTARIO =====")
    print("1. Agregar producto")
    print("2. Mostrar inventario")
    print("3. Calcular estadísticas")
    print("4. Salir")
    
    # Pedir la opción al usuario
    opcion = input("Elige una opción: ")
    
    # Opción 1: Agregar producto
    if opcion == "1":
        print("\n--- Agregar Producto ---")
        nombre = input("Nombre del producto: ")
        precio = float(input("Precio: "))
        cantidad = int(input("Cantidad: "))
        
        # Crear un diccionario con los datos del producto
        producto = {"nombre": nombre, "precio": precio, "cantidad": cantidad}
        
        # Agregar el producto a la lista
        inventario.append(producto)
        print("Producto agregado!")
    
    # Opción 2: Mostrar inventario
    elif opcion == "2":
        print("\n--- Inventario ---")
        
        # Verificar si hay productos
        if len(inventario) == 0:
            print("El inventario está vacío")
        else:
            # Recorrer la lista con un for
            for producto in inventario:
                nombre = producto["nombre"]
                precio = producto["precio"]
                cantidad = producto["cantidad"]
                print(f"Producto: {nombre} | Precio: {precio} | Cantidad: {cantidad}")
    
    # Opción 3: Calcular estadísticas
    elif opcion == "3":
        print("\n--- Estadísticas ---")
        
        # Verificar si hay productos
        if len(inventario) == 0:
            print("No hay productos para calcular")
        else:
            # Variables para ir sumando
            valor_total = 0
            total_productos = 0
            
            # Recorrer todos los productos
            for producto in inventario:
                # Calcular el valor de cada producto (precio x cantidad)
                valor = producto["precio"] * producto["cantidad"]
                valor_total = valor_total + valor
                total_productos = total_productos + 1
            
            # Mostrar resultados
            print(f"Valor total del inventario: ${valor_total}")
            print(f"Cantidad de productos: {total_productos}")
    
    # Opción 4: Salir
    elif opcion == "4":
        print("Saliendo del programa...")
        break  # Sale del while
    
    # Si la opción no es válida
    else:
        print("ERROR: Opción no válida, intenta de nuevo")

print("Programa terminado")

# Resumen semana 2:
# - Usé if, elif, else para el menú
# - Usé while para que el programa se repita
# - Usé for para recorrer el inventario
# - Guardé productos en una lista de diccionarios
# - Calculé estadísticas básicas con un bucle