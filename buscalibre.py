from datetime import datetime

class BuscaLibre:
    def __init__(self, conexion):
        self.conexion = conexion

    # Métodos crear tablas
    def crear_tabla_libros(self):
        consulta = """
            CREATE TABLE IF NOT EXISTS libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isbn TEXT UNIQUE,
                titulo TEXT,
                autor TEXT,
                genero TEXT,
                precio REAL,
                fecha_ultimo_precio TEXT,
                cant_disponible INTEGER
            )
        """
        try:
            self.conexion.crear_tabla(consulta)
        except Exception as e:
            print("Error al crear la tabla de libros: ", str(e))


    def crear_tabla_ventas(self):
        consulta = """
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_libro INTEGER,
                cantidad INTEGER,
                fecha TEXT,
                precio REAL,
                FOREIGN KEY (id_libro) REFERENCES libros (id)
            )
        """
        try:
            self.conexion.crear_tabla(consulta)
        except Exception as e:
            print(f"Error al crear la tabla de ventas: {e}")


    def crear_tabla_historico_libros(self):
        consulta = """
            CREATE TABLE IF NOT EXISTS historico_libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isbn TEXT,
                titulo TEXT,
                autor TEXT,
                genero TEXT,
                precio REAL,
                fecha_ultimo_precio TEXT,
                cant_disponible INTEGER
            )
            """
        try:
            self.conexion.crear_tabla(consulta)
        except Exception as e:
            print("Error al crear la tabla de historico_libros: ", str(e))

    
    
    def cargar_libros(self):
        while True:
            try:
                print("\n")
                opcion_salir = input("Presione cualquier valor para continuar o 0 para volver al menú: ")
                if opcion_salir == "0":
                    break

        
                # Solicitar los datos del libro al usuario
                isbn = (input("ISBN (13 dígitos): "))
                while len(isbn) != 13 or not isbn.isdigit():
                    if len(isbn) != 13 or not isbn.isdigit():
                        print("Error: El ISBN debe tener 13 dígitos númericos.")
                    elif not isbn:
                        print("Error: El ISBN no puede estar vacío.")

                    isbn = input("ISBN (13 dígitos): ")    


                titulo = input("Título: ")
                while not titulo:
                    print("Error: El título no puede estar vacío.")
                    titulo = input("Título: ")
                    

                autor = input("Autor: ")
                while not autor or any(char.isdigit() for char in autor):
                    if not autor:
                        print("Error: El autor no puede estar vacío") 
                    elif any(char.isdigit() for char in autor):
                        print("Error: El autor debe ser una cadena de texto sin números.")

                    autor = input("Autor: ")
                        
                        
                genero = input("Género: ")
                while not genero or any(char.isdigit() for char in genero):
                    if not genero:
                        print("Error: El género no puede estar vacío")
                    elif any(char.isdigit() for char in genero):
                        print("Error: El género debe ser una cadena de texto sin números.")

                    genero = input("Género: ")


                while True:
                    try:
                        precio = float(input("Precio: $"))
                        break
                    except ValueError:
                        print("¡Precio inválido! Intente nuevamente.")                              
                
                fecha_ultimo_precio = datetime.today().strftime("%Y-%m-%d")


                while True:
                    try:
                        cant_disponible = int(input("Cantidad: "))
                        break
                    except ValueError:
                        print("Cantidad inválida! Intente nuevamente.")      
                
            
                consulta = "INSERT INTO libros (isbn, titulo, autor, genero, precio, fecha_ultimo_precio, cant_disponible) VALUES (?, ?, ?, ?, ?, ?, ?)"
                parametros = (isbn, titulo, autor, genero, precio, fecha_ultimo_precio, cant_disponible)
                self.conexion.ejecutar_consulta(consulta, parametros)
                

                print("Libro cargado exitosamente.")
            

            except Exception as e:
                print("Error al cargar el libro:", str(e))


    def modificar_precio(self):
        try:
            while True:
                try:
                    id_libro = int(input("\nIngrese el ID del libro: "))
                    break
                except ValueError:
                    print("Error: ID incorrecto, ingreselo nuevamente.")


            verificar_libro = f"SELECT COUNT(*) FROM libros WHERE id={id_libro}"
            registro = self.conexion.obtener_registro(verificar_libro)

            if registro[0] > 0:
                # Obtener información del libro
                consulta = f"SELECT * FROM libros WHERE id={id_libro}"
                libro = self.conexion.obtener_registro(consulta)

                # Mostrar información del libro
                print("\n> Información del libro: ")
                print(f"ID: {libro[0]} | ISBN: {libro[1]} | Título: {libro[2]} | Autor: {libro[3]} | "
                    f"Género: {libro[4]} | Precio: ${libro[5]:.2f} | Fecha Último Precio: {libro[6]} | "
                    f"CantDisponible: {libro[7]}")

                # Confirmar modificación del precio
                confirmacion = input("\nDesea modificar el precio del libro? (s/n): ")
                while not confirmacion or confirmacion.lower() != "s" or confirmacion.lower() != "n":
                    confirmacion = input("Valor inválido. Desea modificar el precio del libro? (s/n)")
                    break

                if confirmacion.lower() == "s":
                    # Actualizar precio del libro
                    while True:
                        try:
                            nuevo_precio = float(input("\nIngrese el nuevo precio: "))
                            break
                        except ValueError:
                            print("Precio inválido. Intente nuevamente.")                           

                    consulta = f"UPDATE libros SET precio={nuevo_precio}, fecha_ultimo_precio=DATETIME('now') WHERE id={id_libro}"
                    self.conexion.ejecutar_consulta(consulta)
                    print("\nPrecio del libro modificado correctamente.")
                    print(f"El libro con el ID {id_libro} se actualizó a {nuevo_precio}")

                elif confirmacion.lower() == "n":
                    print("\nNo se realizó la modificación del precio del libro.")
                

            else:
                print("El libro con el ID especificado no existe.")
                
        except Exception as e:
            print("Error al modificar el libro:", str(e))



    def borrar_libro(self):
        try:
            while True:
                try:
                    id_libro = int(input("Ingrese el ID del libro: "))
                    break
                except ValueError:
                    print("ID inválido. Intente nuevamente.")                              

            verificar_libro = f"SELECT COUNT(*) FROM libros WHERE id={id_libro}"
            registro = self.conexion.obtener_registro(verificar_libro)
            
            if registro[0] > 0:
                consulta_select = "SELECT * FROM libros WHERE id = ?"
                parametros_select = (id_libro,)
                registro = self.conexion.obtener_registros(consulta_select, parametros_select)

                print("Información del libro:")
                if registro:
                    libro = registro[0]
                    isbn = libro[1]
                    titulo = libro[2]
                    autor = libro[3]
                    genero = libro[4]
                    precio = libro[5]
                    fecha_ultimo_precio = libro[6]
                    cant_disponible = libro[7]

                    print(f"""ISBN: {libro[1]}
Titulo: {libro[2]}
Autor: {libro[3]}
Genero: {libro[4]}
Precio: {libro[5]}
Fecha ultimo precio: {libro[6]}
Cantidad: {libro[7]}                    
                    """)

                    confirmacion = input("\nDesea borrar el libro? (s/n): ")
                    while not confirmacion or confirmacion.lower() != "s" or confirmacion.lower() != "n":
                        confirmacion = input("Valor inválido. Desea borrar el libro? (s/n)")
                        break

                    if confirmacion.lower() == "s":
                        consulta_insert = "INSERT INTO historico_libros (isbn, titulo, autor, genero, precio, fecha_ultimo_precio, cant_disponible) VALUES (?, ?, ?, ?, ?, ?, ?)"
                        parametros_insert = (
                            isbn, titulo, autor, genero, precio, fecha_ultimo_precio, cant_disponible)

                        consulta_delete = "DELETE FROM libros WHERE id = ?"
                        parametros_delete = (id_libro,)

                        self.conexion.ejecutar_consulta(consulta_insert, parametros_insert)
                        self.conexion.ejecutar_consulta(consulta_delete, parametros_delete)

                        print("Libro borrado correctamente.")
                    elif confirmacion.lower() == "n":
                        print("No se borró el libro.")

                else:
                    print("El ID del libro no fue encontrado.")
            
        except Exception as e:
            print("Error al borrar el libro:", str(e))


    def cargar_disponibilidad(self):
        try:
            while True:
                try:
                    id_libro = int(input("Ingrese el ID del libro: "))
                    break
                except ValueError:
                    print("ID inválido. Intente nuevamente.")     

            verificar_libro = f"SELECT COUNT(*) FROM libros WHERE id={id_libro}"
            registro = self.conexion.obtener_registro(verificar_libro)
            
            if registro[0] > 0:
                consulta_select = "SELECT * FROM libros WHERE id = ?"
                parametros_select = (id_libro,)
                registro = self.conexion.obtener_registros(consulta_select, parametros_select)

                if registro:
                    libro = registro [0]
                    cant_disponible_actual = libro [7]

                    print("Información del libro: ")
                    print(f"ID: {libro[0]}")
                    print(f"ISBN: {libro[1]}") 
                    print(f"Título: {libro[2]}")
                    print(f"Autor: {libro[3]}")
                    print(f"Género: {libro[4]}")    
                    print(f"Cantidad disponible: {libro[7]}")    



                    while True:
                        try:
                            incrementar = int(input("Cantidad a incrementar: "))
                            break
                        except ValueError:
                            incrementar = int(input("Cantidad inválida. Ingresela nuevamente: "))

                    confirmacion = input("\nDesea incrementar la cantidad? (s/n): ")
                    while not confirmacion or confirmacion.lower() != "s" or confirmacion.lower() != "n":
                        confirmacion = input("Valor inválido. Desea incrementar la cantidad? (s/n)")
                        break

                    if confirmacion.lower() == "s":
                        cant_disponible_nueva = cant_disponible_actual + incrementar

                        consulta_update = "UPDATE libros SET cant_disponible = ? WHERE id = ?"
                        parametros_update = (cant_disponible_nueva, id_libro)

                        self.conexion.ejecutar_consulta(consulta_update, parametros_update)

                        print("\nDisponibilidad cargada correctamente.")
                    elif confirmacion.lower() == "n":
                        print("\nNo se realizó la carga de disponibilidad.")


                else:
                    print("El ID del libro no existe.")

        except Exception as e:
            print("Error al cargar disponibilidad del libro:", str(e))

    def listar_libros(self):
        try:
            consulta = "SELECT * FROM libros ORDER BY id, autor, titulo"
            registros = self.conexion.obtener_registros(consulta)

            if registros:
                print("Listado de libros: ")
                for detalle_libro in registros:
                    id_libro = detalle_libro[0]
                    isbn = detalle_libro[1]
                    titulo = detalle_libro[2]
                    autor = detalle_libro[3]
                    genero = detalle_libro[4]
                    precio = detalle_libro[5]
                    fecha_ultimo_precio = detalle_libro[6]
                    cant_disponible = detalle_libro[7]

                    print(f"ID: {id_libro}")
                    print(f"ISBN: {isbn}")
                    print(f"Título: {titulo}")
                    print(f"Autor: {autor}") 
                    print(f"Genero: {genero}")
                    print(f"Precio: ${precio:.2f}")
                    print(f"Fecha ultimo precio: {fecha_ultimo_precio}")
                    print(f"Cantidad disponible: {cant_disponible}")
                    print("=======================")
        except Exception as e:
            print("Error al listar libros:", str(e))
        

    def ventas(self):
        try:
            while True:
                try:
                    id_libro = int(input("Ingrese el ID del libro: "))
                    break
                except ValueError:
                    print("ID inválido. Intente nuevamente.")     

            consulta_select = "SELECT * FROM libros WHERE id = ?"
            parametros_select = (id_libro,)
            registro_libro = self.conexion.obtener_registros(consulta_select, parametros_select)

            if registro_libro:
                libro = registro_libro[0]
                cant_disponible_actual = libro[7]
                precio_venta = libro[5]

                print("\nInformación del libro: ")
                print(f"ID: {libro[0]}")
                print(f"ISBN: {libro[1]}") 
                print(f"Título: {libro[2]}")
                print(f"Autor: {libro[3]}")
                print(f"Género: {libro[4]}")    
                print(f"Cantidad disponible: {libro[7]}")   

                cantidad = int(input("\nCantidad vendida: "))

                if cantidad <= cant_disponible_actual:
                    consulta_insert_venta = "INSERT INTO ventas (id_libro, cantidad, fecha, precio) VALUES (?, ?, ?, ?)"
                    parametros_insert_venta = (id_libro, cantidad, datetime.today().strftime("%Y-%m-%d"), precio_venta)

                    consulta_update_libro = "UPDATE libros SET cant_disponible = ? WHERE id = ?"
                    parametros_update_libro = (cant_disponible_actual - cantidad, id_libro)

                    self.conexion.ejecutar_consulta(consulta_insert_venta, parametros_insert_venta)
                    self.conexion.ejecutar_consulta(consulta_update_libro, parametros_update_libro)

                    print("\nVenta realizada correctamente.")
                else:
                    print("\nNo hay suficiente disponibilidad del libro.")
            else:
                print("\nEl ID del libro no existe.")
        except Exception as e:
            print(f"Error al realizar la venta: {e}")


    def actualizar_precios(self):
        try:
            porcentaje_aumento = float(input("\nIngrese el porcentaje de aumento de precios (%): "))

            consulta_select_libros = "SELECT * FROM libros"
            registros_libros = self.conexion.obtener_registros(consulta_select_libros)

            if registros_libros:
                for libro in registros_libros:
                    id_libro = libro[0]
                    isbn = libro[1]
                    titulo = libro[2]
                    autor = libro[3]
                    genero = libro[4]
                    precio_actual = libro[5]
                    fecha_ultimo_precio = libro[6]
                    cant_disponible = libro[7]

                    nuevo_precio = precio_actual + (precio_actual * porcentaje_aumento / 100)

                    consulta_insert_historico = "INSERT INTO historico_libros (isbn, titulo, autor, genero, precio, fecha_ultimo_precio, cant_disponible) VALUES (?, ?, ?, ?, ?, ?, ?)"
                    parametros_insert_historico = (
                        isbn, titulo, autor, genero, precio_actual, fecha_ultimo_precio, cant_disponible)

                    consulta_update_libro = "UPDATE libros SET precio = ?, fecha_ultimo_precio = ? WHERE id = ?"
                    parametros_update_libro = (nuevo_precio, datetime.today().strftime("%Y-%m-%d"), id_libro)

                    self.conexion.ejecutar_consulta(consulta_insert_historico, parametros_insert_historico)
                    self.conexion.ejecutar_consulta(consulta_update_libro, parametros_update_libro)

                print("\nPrecios actualizados correctamente.")
            else:
                print("\nNo hay libros para actualizar los precios.")
        except Exception as e:
            print(f"\nError al actualizar los precios: {e}")

    def mostrar_registros_anteriores_fecha(self):
        try:
            fecha_valida = False
            while not fecha_valida:
                fecha_limite = input("Ingrese la fecha límite (YYYY-MM-DD): ")
                try:
                    datetime.strptime(fecha_limite, "%Y-%m-%d")
                    fecha_valida = True
                except ValueError:
                    print("\nFormato de fecha inválido. Por favor, ingrese la fecha en el formato YYYY-MM-DD.")

            consulta = "SELECT * FROM libros WHERE fecha_ultimo_precio <= ?"
            parametros = (fecha_limite,)
            registros = self.conexion.obtener_registros(consulta, parametros)

            if registros:
                print("\nRegistros anteriores a la fecha límite:")
                print("\n> Información del libro: ")
                for registro in registros:
                    id_libro = registro[0]
                    isbn = registro[1]
                    titulo = registro[2]
                    autor = registro[3]
                    genero = registro[4]
                    precio = registro[5]
                    fecha_ultimo_precio = registro[6]
                    cant_disponible = registro[7]

                    print(f"ID: {id_libro}")
                    print(f"ISBN: {isbn}") 
                    print(f"Título: {titulo}")
                    print(f"Autor: {autor}")
                    print(f"Género: {genero}") 
                    print(f"Precio: ${precio:.2f}")
                    print(f"Fecha último precio: {fecha_ultimo_precio}")
                    print(f"Cantidad disponible: {cant_disponible}")
                    print("=====================")
            else:
                print("\nNo hay registros anteriores a la fecha límite.")
        except Exception as e:
            print(f"\nError al mostrar los registros anteriores a la fecha: {e}")


    def mostrar_historico_libros(self):
        try:
            consulta = "SELECT * FROM historico_libros"
            registros = self.conexion.obtener_registros(consulta)

            if registros:
                print("\n> Información del libro: ")
                for registro in registros:
                    id_libro = registro[0]
                    isbn = registro[1]
                    titulo = registro[2]
                    autor = registro[3]
                    genero = registro[4]
                    precio = registro[5]
                    fecha_ultimo_precio = registro[6]
                    cant_disponible = registro[7]

                    print(f"ID: {id_libro}")
                    print(f"ISBN: {isbn}") 
                    print(f"Título: {titulo}")
                    print(f"Autor: {autor}")
                    print(f"Género: {genero}") 
                    print(f"Precio: ${precio:.2f}")
                    print(f"Fecha último precio: {fecha_ultimo_precio}")
                    print(f"Cantidad disponible: {cant_disponible}")
                    print("=====================")
            else:
                print("No hay registros en el historial de libros.")
        except Exception as e:
            print(f"Error al mostrar el historial de libros: {e}")

    def mostrar_ventas(self):
        try:
            consulta = "SELECT * FROM ventas"
            registros = self.conexion.obtener_registros(consulta)

            if registros:
                print("\n> Información del libro: ")
                for registro in registros:
                    id_venta = registro[0]
                    id_libro = registro[1]
                    cantidad = registro[2]
                    fecha = registro[3]
                    precio = registro[4]

                    print(f"ID Venta: {id_venta}")
                    print(f"ID Libro: {id_libro}")
                    print(f"Cantidad vendida: {cantidad}")
                    print(f"Fecha: {fecha}")
                    print(f"Precio/Unidad: {precio:.2f}")
                    print("=======================")

            else:
                print("No hay registros de ventas.")
        except Exception as e:
            print(f"Error al mostrar las ventas: {e}")