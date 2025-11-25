import csv  # Módulo para trabajar con archivos CSV
import os   # Módulo para operaciones del sistema de archivos

# Rutas de archivos
INVENTORY_FILE = "inventory.csv"
SALES_FILE = "sales.csv"

def create_file():
    # Crear archivos CSV si no existen
    if not os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Escribir encabezados
            writer.writerow(["ID", "Book", "Author", "Category", "Price", "Stock"])

    # VERIFICAR Y CREAR ARCHIVO DE VENTAS 
    if not os.path.exists(SALES_FILE):
        with open(SALES_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Sale ID", "Customer", "Book ID", "Book", "Amount", "Unit Price", "Total"])

def save_book(inventory):
    # Guardar todos los libros en el archivo CSV
    try:
        # 'w' sobrescribe el archivo completo - adecuado para guardar todo el inventario
        with open(INVENTORY_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Book", "Author", "Category", "Price", "Stock"])

            # Escribir cada producto como una fila en el CSV
            for id_book, data in inventory.items():
                writer.writerow([
                    id_book,
                    data["name"],
                    data["author"],
                    data["category"],
                    data["price"],
                    data["stock"],
                ])
        return True     # Indicar éxito
    except Exception as e:
        print(f"Error saving products: {e}")
        return False    # Indicar fallo

def upload_books():
    # Cargar productos desde el archivo CSV
    inventory = {}  # Diccionario vacío para llenar
    try:
        if os.path.exists(INVENTORY_FILE):
            with open(INVENTORY_FILE, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)  # Leer como diccionarios
                for fila in reader:
                    id_book = fila["ID"]
                    # Convertir tipos de datos apropiados
                    inventory[id_book] = {
                        'name': fila['Book'],
                        'author': fila['Author'],
                        'category': fila['Category'],
                        'price': float(fila['Price']),  # Convertir a float
                        'stock': int(fila['Stock']),    # Convertir a int
                    }
    except Exception as e:
        print(f"Error loading products: {e}")    
    
    return inventory

def save_sale(sale):
    # Agregar una nueva venta al archivo CSV
    try:
        # 'a' append - agrega al final sin borrar existentes
        with open(SALES_FILE, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                sale['id_sale'],
                sale['customer'],
                sale['id_book'],
                sale['name_book'],
                sale['amount'],
                sale['unit_price'],
                sale['total'],
            ])
        return True
    except Exception as e:
        print(f"Error saving sale: {e}")
        return False

def upload_sales():
    # Cargar todas las ventas desde el archivo CSV
    sales = []  # Lista vacía para llenar
    try:
        if os.path.exists(SALES_FILE):
            with open(SALES_FILE, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for fila in reader:
                    # Convertir tipos de datos apropiados
                    sales.append({
                        'id_sale': fila['Sale ID'],
                        'customer': fila['Customer'],
                        'id_book': fila['Book ID'],
                        'name_book': fila['Book'],
                        'amount': int(fila['Amount']),
                        'unit_price': float(fila['Unit Price']),
                        'total': float(fila['Total']),  # 'total' minúscula para coincidir
                    })
    except Exception as e:
        print(f"Error loading sales: {e}")
        
    return sales  # Devolver lista cargada (o vacía si hay error)

