# Importar el módulo personalizado para manejo de archivos
import files  

inventory = {}     #Diccionario: clave=ID, valor=datos del libro
sales = []         #Lista para almacenar las ventas
cont_sales = 1 #Contador para generar IDs únicos de ventas

def initialize_data():
    # Inicializar el sistema con datos precargados
    global inventory, sales, cont_sales # Acceder a variables globales

    # Crear archivos CSV si no existen
    files.create_file()
    # Cargar datos desde archivos a memoria
    inventory = files.upload_books()
    sales = files.upload_sales()

    # Configurar contador de ventas basado en el último ID
    # Esto evita duplicados de IDs al reiniciar el programa
    if sales:
        last_id = int(sales[-1]["id_sale"].replace("V", ""))  # Extraer número del ID
        cont_sales = last_id + 1  # Siguiente ID disponible
        
    # Inventario inicial
    if not inventory:
        inventory = {
            "B001": {
                "name": "La biblioteca de la medianoche",
                "author": "Matt Haig",
                "category": "Literatura fantástica",
                "price": 30,
                "stock": 20
            },
            "B002": {
                "name": "Pensar con claridad",
                "author": "Shane Parrish",
                "category": "Desarrollo personal",
                "price": 18,
                "stock": 15
            },
            "B003": {
                "name": "Hábitos atómicos",
                "author": "James Clear",
                "category": "Autoayuda",
                "price": 25,
                "stock": 10
            },
            "B004": {
                "name": "100 años de soledad",
                "author": "Gabriel García Márquez",
                "category": "Novela",
                "price": 23,
                "stock": 12
            },
            "B005": {
                "name": "El monje que vendió su Ferrari",
                "author": "Robin S. Sharma",
                "category": "Ficción",
                "price": 15,
                "stock": 8
            },
        }
        # Guardar los productos de ejemplo en el archivo
        files.save_book(inventory)

# CRUD

def add_book():
    # Agregar un nuevo libro al inventario
    try:
        print("\n=== ADD NEW BOOK ===")

        # Generar nuevo ID automáticamente - EVITA IDs DUPLICADOS
        if inventory:
            # Encontrar el máximo ID existente e incrementarlo
            last_id = max([int(pid.replace("B", "")) for pid in inventory.keys()])
            new_id = f"B{str(last_id + 1).zfill(3)}"  # Formato: B001, B002, etc.
        else:
            new_id = "B001"  # Primer producto

        # Validaciones de entrada
        name = input("Book name: ").strip()
        if not name:
            print("The name cannot be empty")
            return  # Salir temprano si hay error
        
        author = input("Author: ").strip()
        if not author:
            print("The author cannot be empty")
            return
        
        category = input("Category: ").strip()
        if not category:
            print("The category cannot be empty")
            return
        
        # Conversión con validación
        price = float(input("Price: $"))
        if price <= 0:
            print("The price must be positive")
            return
        
        stock = int(input("Stock inicial: "))
        if stock < 0:
            print("Stock cannot be negative")
            return
        
        # Agregar producto al diccionario
        inventory[new_id] = {
            "name": name,
            "author": author,
            "category": category,
            "price": price,
            "stock": stock
        }

        # Persistir inmediatamente - Guardar cambios en disco
        files.save_book(inventory)
        print(f"Book successfully registered with ID: {new_id}")

    except ValueError:
        print("Invalid entry. Please enter the correct information")
    except Exception as e:
        print(f"Error adding book: {e}")
    
def show_inventory():
    # Mostrar todos los productos
    if not inventory:
        print("\nThere are no products in stock")
        return
    
    # Formato de tabla para mejor legibilidad
    print("\n" + "="*123)
    print(f"{'ID':<8} {'Name':<35} {'Author':<30} {'Category':<30} {'Price':<10} {'Stock':<8}")
    print("="*123)

    # Iterar sobre todos los productos
    for id_book, data in inventory.items():
        print(f"{id_book:<8} {data['name']:<35} {data['author']:<30} {data['category']:<30} ${float(data['price']):<9.2f} {data['stock']:<8}")

    print("="*123)

def update_book():
    # Actualizar un producto existente
    try:
        show_inventory()    # Mostrar productos para que usuario elija
        id_book = input("\nEnter the ID of the product to be updated:").strip().upper()

        if id_book not in inventory:
            print("Book not found")
            return
        
        print(f"\nUpdating: {inventory[id_book]['name']}")
        print("(Press Enter to keep the current value)")

        # Solicitar nuevos valores (Enter mantiene el actual)
        name = input(f"Name [{inventory[id_book]['name']}]: ").strip()
        author = input(f"Author [{inventory[id_book]['author']}]: ").strip()
        category = input(f"Category [{inventory[id_book]['category']}]: ").strip()
        price = input(f"Price [{inventory[id_book]['price']}]: ").strip()
        stock = input(f"Stock [{inventory[id_book]['stock']}]: ").strip()

        # Actualizar solo los campos que cambiaron
        if name:
            inventory[id_book]["name"] = name
        if author:
            inventory[id_book]["author"] = author
        if category:
            inventory[id_book]["category"] = category
        if price:
            inventory[id_book]["price"] = float(price)
        if stock:
            inventory[id_book]["stock"] = int(stock)
        
        files.save_book(inventory)
        print("Product successfully updated")
        
    except ValueError:
        print("Invalid entry")
    except Exception as e:
        print(f"Error updating book:: {e}")

def remove_book():
    #Eliminar un producto del inventario
    try:
        show_inventory()
        id_book = input("\nEnter the ID of the product to be deleted: ").strip().upper()

        if id_book not in inventory:
            print("Book not found")
            return
        
        confirm = input(f"¿Are you sure you want to delete '{inventory[id_book]['name']}'? (si/no): ").lower()

        if confirm == "si":
            del inventory[id_book]  # Eliminar del diccionario
            files.save_book(inventory)
            print("Product successfully deleted")
        else:
            print("Canceled elimination")

    except Exception as e:
        print(f"Error deleting product: {e}")

# GESTIÓN DE VENTAS

def add_sale():
    # Registrar una nueva venta
    global cont_sales   # Modificar variable global

    try:
        print("\n=== REGISTER NEW SALE ===")

        show_inventory()    # Mostrar productos disponibles

        customer = input("\nClient's name: ").strip()
        if not customer:
            print("The customer name cannot be empty")
            return
        
        id_book = input("Book ID: ").strip().upper()
        if id_book not in inventory:
            print("Product not found")
            return
        
        amount = int(input("¿How many?: "))
        if amount <= 0:
            print("The amount must be positive")
            return
        
        # Validar stock disponible
        if inventory[id_book]["stock"] < amount:
            print(f"Insufficient stock. Available: {inventory[id_book]['stock']}")
            return

        #Cálculos de la venta
        unit_price = inventory[id_book]["price"]
        total = unit_price * amount

        # Crear registro de venta con todos los datos necesarios
        id_sale = f"V{str(cont_sales).zfill(4)}"    # Formato: V0001, V0002, etc.
        sale = {
            "id_sale": id_sale,
            "customer": customer,
            "id_book": id_book,
            "name_book": inventory[id_book]["name"],
            "amount": amount,
            "unit_price": unit_price,
            "total": total
        }

        # Actualizar stock del producto
        inventory[id_book]["stock"] -= amount

        # Persistir todos los cambios
        sales.append(sale)
        files.save_sale(sale)   # Guardar en archivo
        files.save_book(inventory)  # Actualizar stock en archivo

        cont_sales += 1 # Incrementar para próxima venta

        # Mostrar recibo detallado al usuario
        print("\n" + "="*50)
        print("SALES RECEIPT")
        print("="*50)
        print(f"Sale ID : {id_sale}")
        print(f"Customer: {customer}")
        print(f"Book: {inventory[id_book]['name']}")
        print(f"Amount: {amount}")
        print(f"Unit price: ${unit_price:.2f}")
        print(f"TOTAL: ${total:.2f}")
        print("="*50)
        print("Sale successfully recorded")

    except ValueError:
        print("Invalid entry")
    except Exception as e:
        print(f"Error recording sale: {e}")

def show_sales():
    # Mostrar todas las ventas
    if not sales:
        print("No sales recorded")
        return
    
    # Formato de tabla para mejor visualización
    print("\n" + "="*95)
    print(f"{'Sale ID':<10} {'Customer':<20} {'Book':<30} {'Amount':<10} {'Price':<12} {'Total':<10}")
    print("="*95)

    for sale in sales:
        print(f"{sale['id_sale']:<10} {sale['customer']:<20} {sale['name_book']:<30} {sale['amount']:<10} ${sale['unit_price']:<10.2f}  ${sale['total']:<10.2f}")

    print("="*95)

#REPORTES

def top_3_products():
    #Mostrar top 3 libros más vendidos
    print("\n=== TOP 3 BEST-SELLING PRODUCTS ===")

    if not sales:
        print("No sales data available")
        return
    
    # Agrupar ventas por producto usando diccionario
    sales_by_book = {}
    for sales in sales:
        pid = sales["id_book"]
        if pid in sales_by_book:
            # Acumular cantidad e ingresos
            sales_by_book[pid]["amount"] += sales["amount"]
            sales_by_book[pid]["revenue"] += sales["total"]
        else:
            # Primera vez que aparece este producto
            sales_by_book[pid] = {
                "name": sales["name_book"],
                "amount": sales["amount"],
                "revenue": sales["total"]
            }

    # Ordenar por cantidad vendida (descendente) usando lambda
    products_sorted = sorted(sales_by_book.items(), key=lambda x: x[1]["amount"], reverse=True)

    print(f"\n{'Position':<10} {'Book ID':<12} {'Name':<35} {'Amount':<12} {'Revenue':<12}")
    print("="*85)

    # Mostrar solo los top 3
    for i, (pid, data) in enumerate(products_sorted[:3], 1):
        print(f"{i:<10} {pid:<12} {data['name']:<35} {data['amount']:<12} ${data['revenue']:<11.2f}")

def sales_by_author():
    # Mostrar ventas agrupadas por autor
    print("\n=== SALES BY AUTHOR ===")

    sales_author = {}

    for sale in sales:
        pid = sale["id_book"]
        if pid in inventory:
            author = inventory[pid]["author"]
            if author in sales_author:
                # Acumular unidades e ingresos por autor
                sales_author[author]["amount"] += sale["amount"]
                sales_author[author]["revenue"] += sale["total"]
            else:
                # Primera vez que aparece este autor/a
                sales_author[author] = {
                    "amount": sale["amount"],
                    "revenue": sale["total"]
                }

    print(f"\n{'Author':<20} {'Units sold':<20} {'Total income':<20}")
    print("="*60)

    # Mostrar autores ordenadas alfabéticamente
    for author, data in sorted(sales_author.items()):
        print(f"{author:<20} {data['amount']:<20} ${data['revenue']:<19.2f}")

def income_statement():
    # Calcular ingresos
    print("\n=== REVENUE REPORTS ===")

    if not sales:
        print("No sales data available")
        return
    
    # Usando map y lambda para cálculos funcionales
    revenue = sum(map(lambda x: x["unit_price"] * x["amount"], sales))

    print(f"Total Revenue: ${revenue:.2f}")

def inventory_performance():
    # Mostrar reporte de rendimiento del inventario

    print("\n=== INVENTORY PERFORMANCE REPORTS ===")

    print(f"\n{'Book ID':<12} {'Book':<35} {'Stock':<10} {'Sold':<10} {'Status':<20}")
    print("="*90)

    for pid, data in inventory.items():
        # Calcular total vendido para este producto
        sold = sum([v["amount"] for v in sales if v["id_book"] == pid])

        # Lógica de clasificación de estado
        if data["stock"] == 0:
            status = "OUT OF STOCK"
        elif data["stock"] < 10:
            status = "LIMITED STOCK"
        elif sold > data["stock"]:
            status = "HIGH DEMAND"
        else:
            status = "NORMAL"
        
        print(f"{pid:<12} {data['name']:<35} {data['stock']:<10} {sold:<10} {status:<20}")