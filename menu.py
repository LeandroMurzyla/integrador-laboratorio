import buscalibre
import datetime


class MenuBuscalibre:
    def __init__(self):
        # Llamada a la función crear_tablas para asegurarnos de que las tablas existan
        buscalibre.crear_tablas()
        

    def mostrar_menu(self):
        while True:
            print("=== MENÚ DE OPCIONES ===")
            print("1. Cargar Libros")
            print("2. Modificar precio de un libro")
            print("3. Borrar un libro")
            print("4. Cargar disponibilidad")
            print("5. Listado de Libros")
            print("0. Salir del menú")
            print("========================")

            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                self.cargar_libros()
            elif opcion == "2":
                self.modificar_precio()
            elif opcion == "3":
                self.borrar_libro()
            elif opcion == "4":
                self.cargar_disponibilidad()
            elif opcion == "5":
                self.listar_libros()
            elif opcion == "0":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida. Inténtalo nuevamente.")



    def cargar_libros(self):
        valid_input = False

        while not valid_input:
            try:
                # Solicitar los datos del libro al usuario
                isbn = input("ISBN (13 dígitos): ")
                if len(isbn) != 13:
                    print("Error: El ISBN debe tener 13 dígitos.")
                    continue

                titulo = input("Título: ")
                if not titulo:
                    print("Error: El título no puede estar vacío.")
                    continue

                autor = input("Autor: ")
                if not autor.isalpha():
                    print("Error: El autor debe ser una cadena de texto sin números.")
                    continue

                genero = input("Género: ")
                if not genero.isalpha():
                    print("Error: El género debe ser una cadena de texto sin números.")
                    continue

                while True:
                    try:
                        precio = float(input("Precio: "))
                        break
                    except ValueError:
                        print("Error: El precio debe ser un número válido.")
                        continue

                while True:
                    try:
                        fecha_str = input("Fecha último precio (YYYY-MM-DD): ")
                        fecha_ultimo_precio = datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
                        break
                    except ValueError:
                        print("Error: Formato de fecha inválido. Debe ser YYYY-MM-DD.")
                        continue

                while True:
                    try:
                        cant_disponible = int(input("Cantidad disponible: "))
                        break
                    except ValueError:
                        print("Error: La cantidad disponible debe ser un número válido.")
                        continue

                # Validar que el autor y el género no contengan números
                if not autor.isalpha() or not genero.isalpha():
                    print("Error: El autor y el género deben ser cadenas de texto sin números.")
                    continue

                # Crear una tupla con los datos del libro
                libro = (isbn, titulo, autor, genero, precio, fecha_ultimo_precio, cant_disponible)

                # Insertar el libro en la base de datos
                query = "INSERT INTO Libros (ISBN, Titulo, Autor, Genero, Precio, FechaUltimoPrecio, CantDisponible) VALUES (?, ?, ?, ?, ?, ?, ?)"
                buscalibre.ejecutar_actualizacion(query, libro)
                print("Libro cargado exitosamente.")
                valid_input = True

            except Exception as e:
                print("Error al cargar el libro:", str(e))
    pass








    def modificar_precio(self, id_libro, nuevo_precio):
        try:
            # Verificar si el libro existe en la base de datos
            query_verificar = "SELECT COUNT(*) FROM Libros WHERE ID = ?"
            resultado = buscalibre.ejecutar_consulta(query_verificar, (id_libro,))
            if resultado[0][0] == 0:
                print("Error: El libro con ID", id_libro, "no existe.")
                return

            # Confirmar la modificación de precio
            confirmacion = input("¿Estás seguro de modificar el precio del libro? (S/N): ")
            if confirmacion.lower() != "s":
                print("Modificación de precio cancelada.")
                return

            # Actualizar el precio del libro en la base de datos
            query_actualizar = "UPDATE Libros SET Precio = ? WHERE ID = ?"
            parametros = (nuevo_precio, id_libro)
            buscalibre.ejecutar_actualizacion(query_actualizar, parametros)

            print("Precio del libro modificado exitosamente.")

        except Exception as e:
            print("Error al modificar el precio del libro:", str(e))
    pass



    def borrar_libro(self):
        # Solicitar el ID del libro al usuario
        id_libro = int(input("ID del libro: "))

        try:
            # Verificar si el libro existe en la base de datos
            consulta = f"SELECT * FROM Libros WHERE ID = {id_libro}"
            resultado = buscalibre.ejecutar_consulta(consulta)

            if resultado:
                libro = resultado[0]
                isbn = libro[1]
                titulo = libro[2]
                autor = libro[3]

                # Confirmar el borrado del libro
                confirmacion = input(
                    f"¿Deseas borrar el libro {titulo} de {autor}? (S/N): ")

                if confirmacion.upper() == "S":
                    # Eliminar el libro de la base de datos
                    consulta = "DELETE FROM Libros WHERE ID = ?"
                    parametros = (id_libro,)
                    buscalibre.ejecutar_actualizacion(consulta, parametros)
                    print("Libro borrado exitosamente.")
                else:
                    print("Borrado de libro cancelado.")
            else:
                print("El libro con el ID especificado no existe.")

        except Exception as e:
            print("Error al borrar el libro:", str(e))
    pass

    def cargar_disponibilidad(self):
        # Solicitar el ID del libro y la cantidad a incrementar al usuario
        id_libro = int(input("ID del libro: "))
        incremento = int(input("Cantidad a incrementar: "))

        try:
            # Verificar si el libro existe en la base de datos
            consulta = f"SELECT * FROM Libros WHERE ID = {id_libro}"
            resultado = buscalibre.ejecutar_consulta(consulta)

            if resultado:
                libro = resultado[0]
                isbn = libro[1]
                titulo = libro[2]
                autor = libro[3]
                cant_disponible_actual = libro[7]

                # Calcular la nueva cantidad disponible
                nueva_cant_disponible = cant_disponible_actual + incremento

                # Confirmar el incremento de disponibilidad
                confirmacion = input(
                    f"¿Deseas cargar {incremento} unidades al libro {titulo} de {autor}? (S/N): ")

                if confirmacion.upper() == "S":
                    # Actualizar la disponibilidad del libro en la base de datos
                    consulta = "UPDATE Libros SET CantDisponible = ? WHERE ID = ?"
                    parametros = (nueva_cant_disponible, id_libro)
                    buscalibre.ejecutar_actualizacion(consulta, parametros)
                    print(
                        f"Disponibilidad del libro actualizada: {nueva_cant_disponible} unidades.")
                else:
                    print("Carga de disponibilidad cancelada.")
            else:
                print("El libro con el ID especificado no existe.")

        except Exception as e:
            print("Error al cargar la disponibilidad del libro:", str(e))
    pass

    def listar_libros(self):
        try:
            # Consultar todos los libros ordenados por ID, autor y título
            consulta = "SELECT * FROM Libros ORDER BY ID, Autor, Titulo"
            resultado = buscalibre.ejecutar_consulta(consulta)

            if resultado:
                print("Listado de Libros:")
                print("------------------")

                for libro in resultado:
                    id_libro = libro[0]
                    isbn = libro[1]
                    titulo = libro[2]
                    autor = libro[3]
                    genero = libro[4]
                    precio = libro[5]
                    fecha_ultimo_precio = libro[6]
                    cant_disponible = libro[7]

                    print(f"ID: {id_libro}")
                    print(f"ISBN: {isbn}")
                    print(f"Título: {titulo}")
                    print(f"Autor: {autor}")
                    print(f"Género: {genero}")
                    print(f"Precio: {precio}")
                    print(f"Fecha Último Precio: {fecha_ultimo_precio}")
                    print(f"Cantidad Disponible: {cant_disponible}")
                    print("------------------")

            else:
                print("No hay libros registrados en la base de datos.")

        except Exception as e:
            print("Error al listar los libros:", str(e))

    pass


# Crear una instancia de la clase MenuBuscalibre y llamar a mostrar_menu()
menu = MenuBuscalibre()
menu.mostrar_menu()
