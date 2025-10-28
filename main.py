## importo las funciones externas que voy a usar
from colorama import Fore, Back, init
from funcionBusqueda import menuBusqueda
import sqlite3

init()

db="inventario.db"
with sqlite3.connect(db) as conn:   ## creación del archivo db
    cursor=conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS productos
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT)''')
    conn.commit()

def agregarProductos(db): ## funcion agregar
    while True:  
        try:
            nombre=input(Fore.LIGHTMAGENTA_EX + "Ingrese el nombre del producto o 'salir' para volver al menú principal: ").strip().capitalize() # pregunto el nombre, strip para que no se usen espacios de mas
            if nombre=="":
                raise NameError("El nombre no puede estar vacío") ## si el nombre esta vacio se genera error
            elif nombre=="Salir":
                break  ## si se escribe salir se sale del while
            
            descripcion=input(Fore.LIGHTMAGENTA_EX + "Ingrese la descripcion del producto: ").strip().capitalize() # tomo la descripcion, puede estar vacía
            
            cantidad=input("Ingrese la cantidad del producto: ").strip() ## tomo la cantidad
            if cantidad.isdigit():
                cantidad=int(cantidad) ## verifico si es un dígito, si lo es se transforma en int
            else:
                raise NameError("La cantidad tiene que ser un número entero") ## si no, se genera error
            
            precio=float(input("Ingrese el precio del producto: ").replace(",",".")) ## pido el precio, como es un float automaticamente genera error si es inválido
            
            categoria=input("Ingrese la categoría del producto: ").strip().capitalize() ## tomo la categoria
        
            with sqlite3.connect(db) as conn:
                cursor=conn.cursor()
                cursor.execute('''INSERT INTO productos(nombre,descripcion,cantidad,precio,categoria)
                            VALUES(?,?,?,?,?)''',
                            (nombre, descripcion, cantidad, precio, categoria)) ## inserto el producto a la base de datos
                conn.commit() ## para que se apliquen los cambios
            
            print(Back.LIGHTGREEN_EX + Fore.BLACK + "El producto ha sido añadido correctamente" + Back.RESET + Fore.RESET) ## indicación que se hizo correctamente
        except ValueError:
            print(Back.LIGHTRED_EX + Fore.BLACK + "[ERROR] Asegúrese que el precio sea un número válido" + Back.RESET + Fore.RESET) ## ValueError para cuando se ingresa un numero no float
        except NameError as error:
            print(Back.LIGHTRED_EX + Fore.BLACK + f"[ERROR] {error}" + Back.RESET + Fore.RESET) ## NameError para cuando se pone mal el precio/nombre
 
def infoProductos(db): ## funcion lista de productos
    with sqlite3.connect(db) as conn:   
        cursor=conn.cursor()
        cursor.execute('''SELECT * FROM productos''') ## selecciono todos los datos
        datos=cursor.fetchall() ## almaceno los datos en una variable
        if not datos: ## verifico si los datos existen, si no existen sale error
            print(Back.RED + Fore.BLACK + "[ERROR] No hay productos ingresados" + Back.RESET + Fore.RESET)
        else:
            for id, nom, desc, cant, prec, cat in datos:
                print(Fore.LIGHTMAGENTA_EX + f"ID: {id} -" + Fore.LIGHTBLUE_EX + f" Producto: {nom} -" + Fore.LIGHTCYAN_EX + f" Descripción: {desc} -" + Fore.LIGHTRED_EX + f" Categoria: {cat} - " + Fore.LIGHTYELLOW_EX + F"Cantidad: {cant} -" + Fore.LIGHTGREEN_EX + f" Precio ${prec}" + Fore.RESET)

def modProductos(db): ## funcion modificacion de datos
    while True:
        try:
            with sqlite3.connect(db) as conn:
                cursor=conn.cursor()
                modID=input(Fore.YELLOW + "Ingrese el ID del producto a modificar o 'salir' para cancelar: ").strip() ## pido la id del producto
                if modID=="salir":
                    break   ## si el usuario escribe salir, se rompe el bucle
                if modID.isdigit():
                    modID=int(modID) ## si es un dígito se transforma en int
                else:
                    raise ValueError("ID inválido") ## si no, se crea error
                
                cursor.execute('''SELECT * FROM productos WHERE id=?''',(modID,)) ## selecciona la parte de la tabla con ese id
                if cursor.fetchone(): ## si se encuentra el id se continua el codigo
                    try:
                        newNombre=input("Ingrese el nuevo nombre: ").strip().capitalize() ## pido el nuevo nombre
                        if newNombre=="":
                            raise ValueError("El nombre no puede estar vacío") ## si esta vacio se genera error
                        
                        newDesc=input("Ingrese la nueva descripción: ").strip().capitalize() ## pido descripcion
                        
                        newCant=input("Ingrese la nueva cantidad: ") ## pido cantidad
                        
                        if newCant.isdigit():
                            newCant=int(newCant) ## me aseguro que sea digito y lo transformo en int
                        else:
                            raise ValueError("Cantidad inválida") ## si no sale error
                        
                        newPrec=float(input("Ingrese el nuevo precio: ").replace(",",".")) ## pido precio y lo hago float
                        
                        newCat=input("Ingrese la nueva categoría: ").strip().capitalize() ## pido categoria
                        
                        while True:
                            ## le repito al usuario los datos que ingresó y le pregunto si quiere continuar
                            confirmacion=input(f"Vas a modificar el ID {modID} con los siguientes datos:\nNombre: {newNombre}\nDescripcion: {newDesc}\nCantidad: {newCant}\nPrecio: ${newPrec}\nCategoria: {newCat}\n" + Fore.LIGHTRED_EX + "Escriba 'si' para confirmar, 'no' para volver: " + Fore.RESET).strip().lower() 
                            
                            if confirmacion=="si":
                                cursor.execute('''UPDATE productos
                                            SET nombre=?, descripcion=?, cantidad=?, precio=?, categoria=? WHERE id=?''',
                                            (newNombre, newDesc, newCant, newPrec, newCat, modID))
                                conn.commit() ## si el usuario confirma, se realizan los cambios
                                
                                print(Back.GREEN + Fore.BLACK + "Producto modificado con éxito" + Back.RESET + Fore.RESET) ## se avisa que se realizó con éxito
                                
                                break ## y se sale del bucle
                            
                            elif confirmacion=="no":
                                break ## si el usuario dice "no" simplemente se sale del bucle
                            
                            else:
                                print(Back.RED + Fore.BLACK + "[ERROR] Opción inválida" + Back.RESET + Fore.RESET) ## si el usuario pone algo mal sale error
                                
                    except ValueError as error:
                        print(Back.RED + Fore.BLACK + f"[ERROR] {error}" + Back.RESET + Fore.RESET)  ## error de nombre vacio    
                                
                else:
                    print(Back.RED + Fore.BLACK + "[ERROR] Producto no encontrado" + Back.RESET + Fore.RESET) ## error de producto inexistente
                    
        except ValueError:
            print(Back.RED + Fore.BLACK + "[ERROR] ID inválido" + Back.RESET + Fore.RESET) ## error de id inválido

def borrarProductos(db): ## funcion borrar productos
    with sqlite3.connect(db) as conn:
        while True:
            try:
                cursor=conn.cursor()
                borrar=input(Fore.LIGHTGREEN_EX + "Ingresa el ID del producto a eliminar o 'salir' para volver: ").strip() ## pido el id del producto a eliminar
                if borrar=="salir":
                    break ## si se escribe salir se sale del bucle
                elif borrar.isdigit():
                    borrar=int(borrar) ## si es un dígito se vuelve int
                else:
                    raise ValueError("ID inválido") ## si no se declara error
                
                cursor.execute('''SELECT nombre FROM productos WHERE id=?''',(borrar,))
                seleccion=cursor.fetchone() ## almaceno el dato en una variable 
                
                if seleccion: ## esto ocurre en caso de que la seleccion haya ocurrido
                    while True:
                        nombre=seleccion[0] ## almaceno el dato en otra variable porque es una tupla y si no sale con ('',)
                        confBorrar=input(Fore.LIGHTRED_EX + f"Vas a eliminar {nombre}, seguro? (si/no): " + Fore.RESET).strip().lower() ## le pregunto al usuario si esta seguro
                        
                        if confBorrar=="no":
                            break ## si el usuario dice no, se rompe el bulcle
                        elif confBorrar=="si": ## si el usuario dice si
                            cursor.execute('''DELETE FROM productos WHERE id=?''',(borrar,)) ## se ejecuta el comando de borrar
                            conn.commit() ## se aplica
                            print(Back.LIGHTGREEN_EX + Fore.BLACK + "Producto eliminado con éxito" + Back.RESET + Fore.RESET) ## se le avisa al usuario
                            break ## y se rompe el bucle
                        else:
                            print(Back.LIGHTRED_EX + Fore.BLACK + "[ERROR] opción inválida" + Back.RESET + Fore.RESET) ## en caso de no escribir si o no
                            
                else:
                    raise ValueError("Producto no encontrado") ## en caso de que el producto no exista
                
            except ValueError as error:
                print(Back.LIGHTRED_EX + Fore.BLACK + f"[ERROR] {error}" + Back.RESET + Fore.RESET) ## mensaje de error para el ususario
            
def menuPrincipal(): ## funcion menú principal
    while True:
        print(Back.LIGHTBLUE_EX + Fore.BLACK + "-Menú Principal-" + Back.RESET + Fore.RESET)

        opcion=input(Fore.LIGHTMAGENTA_EX + "1. Agregar productos.\n" + Fore.LIGHTBLUE_EX + "2. Consultar Productos.\n" + Fore.LIGHTYELLOW_EX + "3. Modificar Productos.\n" + Fore.LIGHTGREEN_EX + "4. Eliminar productos\n" + Fore.LIGHTCYAN_EX + "5. Buscar Productos\n" + Fore.LIGHTRED_EX + "6. Salir\n" + Fore.RESET + "Opcion: ")
        ## dependiendo del número que ponga el usuario, se ejecutan diferentes funciones
        if opcion=="1":
            agregarProductos(db)
        elif opcion=="2":
            infoProductos(db)
        elif opcion=="3":
            modProductos(db)
        elif opcion=="4":
            borrarProductos(db)
        elif opcion=="5":
            menuBusqueda(db)
        elif opcion=="6" or opcion=="salir":
            break
        else:
            print(Back.LIGHTRED_EX + Fore.BLACK + "[ERROR] Opcion inválida." + Back.RESET + Fore.RESET)

menuPrincipal() ## se ejecuta el menú principal