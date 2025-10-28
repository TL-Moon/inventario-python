from colorama import Fore, Back, init
import sqlite3

init()

db="inventario.db"
def busquedaID(db): ## Búsqueda por ID
    while True:
        with sqlite3.connect(db) as conn:
            cursor=conn.cursor()
            
            busquedaID=input(Fore.LIGHTCYAN_EX + "Ingrese el ID del producto a buscar o 'salir' para volver: ").strip() ## pido el id a buscar
            if busquedaID=="salir": ## si es salir se rompe el bucle
                break
            elif busquedaID.isdigit():
                busquedaID=int(busquedaID) ## si es un dígito lo transformo en int
            else:
                print(Back.LIGHTRED_EX + Fore.BLACK + "[ERROR] Número inválido" + Back.RESET + Fore.RESET) ## si no sale error
                
            cursor.execute(''' SELECT * FROM productos WHERE id=?''',(busquedaID,)) ## selecciono la parte con ese id
            
            idEncontrado=cursor.fetchone() ## almaceno la tupla en una variable
            
            if idEncontrado: ## si se encuentra ese id (o sea si se almacena), se da toda la informacion
                print(Back.LIGHTGREEN_EX + Fore.BLACK + f"Se ha encontrado un producto con ID {busquedaID}" + Back.RESET + Fore.RESET)
                print(Fore.LIGHTMAGENTA_EX + f"Nombre: {idEncontrado[1]}\n" + Fore.LIGHTBLUE_EX + f"Descripcion: {idEncontrado[2]}\n" + Fore.LIGHTCYAN_EX + f"Cantidad: {idEncontrado[3]}\n" + Fore.LIGHTGREEN_EX + f"Precio: ${idEncontrado[4]}\n" + Fore.LIGHTRED_EX + f"Categoria: {idEncontrado[5]}" + Fore.RESET)
            else: ## si no, sale error
                print(Back.LIGHTRED_EX + Fore.BLACK + "[ERROR] No se encontró producto con ese id" + Back.RESET + Fore.RESET)

def busquedaNomb(db): ## busqueda por nombre
    while True:
        with sqlite3.connect(db) as conn:
            cursor=conn.cursor()
            
            busquedaID=input(Fore.LIGHTCYAN_EX + "Ingrese el nombre del producto a buscar o 'salir' para volver: ").strip().capitalize() ## pido nombre
            if busquedaID=="Salir": ## si es salir se rompe el bucle
                break
                
            cursor.execute(''' SELECT * FROM productos WHERE nombre=?''',(busquedaID,)) ## lo mismo que id, pero se selecciona por nombre
            
            idEncontrado=cursor.fetchone() ## se almacena en una variable
            
            if idEncontrado: ## si se encuentra se muestra el producto
                print(Back.LIGHTGREEN_EX + Fore.BLACK + f"Se ha encontrado un producto con nombre {busquedaID}" + Back.RESET + Fore.RESET)
                print(Fore.LIGHTMAGENTA_EX + f"Nombre: {idEncontrado[1]}\n" + Fore.LIGHTBLUE_EX + f"Descripcion: {idEncontrado[2]}\n" + Fore.LIGHTCYAN_EX + f"Cantidad: {idEncontrado[3]}\n" + Fore.LIGHTGREEN_EX + f"Precio: ${idEncontrado[4]}\n" + Fore.LIGHTRED_EX + f"Categoria: {idEncontrado[5]}" + Fore.RESET)
            else: ## si no sale error
                print(Back.LIGHTRED_EX + Fore.BLACK + "[ERROR] No se encontró un producto con ese nombre" + Back.RESET + Fore.RESET)

def busquedaCateg(db): ## busqueda por categoria
    while True:
        with sqlite3.connect(db) as conn:
            cursor=conn.cursor()
            
            busquedaID=input(Fore.LIGHTCYAN_EX + "Ingrese la categoría buscar o 'salir' para volver: ").strip().capitalize() ## pido la categoria a buscar
            if busquedaID=="Salir":
                break ## si es salir se rompe el bucle
                
            cursor.execute(''' SELECT id, cantidad, nombre, precio FROM productos WHERE categoria=?''',(busquedaID,)) ## selecciono id cantidad nombre y precio de la categoria para no poner tantos datos
            
            idEncontrado=cursor.fetchall() ## almaceno la seleccion en variable
            
            if idEncontrado: ## si se encuentra 
                print(Back.LIGHTGREEN_EX + Fore.BLACK + f"Productos con la categoría: {busquedaID}" + Back.RESET + Fore.RESET)
                for id, cant , nomb, prec in idEncontrado: ## con for se muestran todos los productos
                    print(Fore.LIGHTBLUE_EX + f"ID: {id}. " + Fore.LIGHTMAGENTA_EX + f"Nombre: {nomb}. " + Fore.LIGHTGREEN_EX + f"Precio: ${prec}. " + Fore.LIGHTRED_EX + f"Cantidad: {cant}")
            else: ## si no sale error
                print(Back.LIGHTRED_EX + Fore.BLACK + "[ERROR] No se encontraron productos con esa categoría" + Back.RESET + Fore.RESET)

def busquedaCant(db): ## busqueda por cantidad
    while True:
        with sqlite3.connect(db) as conn:
            cursor=conn.cursor()
            
            busquedaID=input(Fore.LIGHTCYAN_EX + "Ingrese una cantidad para buscar o 'salir' para volver: ").strip() ## pido la cantidad a buscar
            if busquedaID=="salir":
                break ## si es salir se rompe el bucle
            elif busquedaID.isdigit():
                busquedaID=int(busquedaID) ## si es digito lo transformo en int
            else:
                print(Back.LIGHTRED_EX + Fore.BLACK + "[ERROR] Número inválido" + Back.RESET + Fore.RESET) ## si no sale error
                
            cursor.execute(''' SELECT id, cantidad, nombre, precio FROM productos WHERE cantidad<=?''',(busquedaID,)) ## selecciono los mismos datos que el anterior
            
            idEncontrado=cursor.fetchall() ## almaceno todo en una variable
            
            if idEncontrado: ## si se encuentra:
                print(Back.LIGHTGREEN_EX + Fore.BLACK + f"Productos con la cantidad indicada o menos: {busquedaID}" + Back.RESET + Fore.RESET)
                for id, cant, nomb, prec in idEncontrado: ## uso for para mostrar los datos almacenados
                    print(Fore.LIGHTBLUE_EX + f"ID: {id}. " + Fore.LIGHTMAGENTA_EX + f"Nombre: {nomb}. " + Fore.LIGHTGREEN_EX + f"Precio: ${prec}. " + Fore.LIGHTRED_EX + f"Cantidad: {cant}")
            else: ## si no sale error
                print(Back.LIGHTRED_EX + Fore.BLACK + "[ERROR] No se encontraron productos" + Back.RESET + Fore.RESET)

def menuBusqueda(db): ## menu de busqueda
    while True:
        print(Back.LIGHTBLUE_EX + Fore.BLACK + "-Menú de búsqueda-" + Back.RESET + Fore.RESET)

        opcion=input(Fore.LIGHTMAGENTA_EX + "1. Buscar por ID.\n" + Fore.LIGHTBLUE_EX + "2. Buscar por nombre.\n" + Fore.LIGHTYELLOW_EX + "3. Buscar por categoría.\n" + Fore.LIGHTGREEN_EX + "4. Búsqueda por cantidad.\n" + Fore.LIGHTRED_EX + "5. Salir\n" + Fore.RESET + "Opcion: ")
        ## dependiendo del número que ponga el usuario, se ejecutan diferentes funciones
        if opcion=="1":
            busquedaID(db)
        elif opcion=="2":
            busquedaNomb(db)
        elif opcion=="3":
            busquedaCateg(db)
        elif opcion=="4":
            busquedaCant(db)
        elif opcion=="5" or opcion=="salir":
            break
        else:
            print(Back.LIGHTRED_EX + Fore.BLACK + "[ERROR] Opcion inválida." + Back.RESET + Fore.RESET)
