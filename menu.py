from conexion import ConexionSQLite
from buscalibre import BuscaLibre

def mostrar_menu():
    print("=== MENÚ DE OPCIONES ===")
    print("1. Cargar Libros")
    print("2. Modificar precio de un libro")
    print("3. Borrar un libro")
    print("4. Cargar disponibilidad")
    print("5. Listado de Libros")
    print("6. Ventas")
    print("7. Actualizar precios")
    print("8. Mostrar histórico de libros")
    print("9. Mostrar registros anteriores a una fecha")
    print("10. Mostrar ventas")
    print("0. Salir del menú")
    print("========================")

def ejecutar_menu():
    conexion = ConexionSQLite("buscalibre.db")
    conexion.conectar()

    buscalibre = BuscaLibre(conexion)

    buscalibre.crear_tabla_libros()
    buscalibre.crear_tabla_ventas()
    buscalibre.crear_tabla_historico_libros()

    opcion = None
    while opcion != "0":
        mostrar_menu()
        opcion = input("Selecciona una opción: ")
        print("\n")

        if opcion == "1":
            buscalibre.cargar_libros()
        elif opcion == "2":
            buscalibre.modificar_precio()
        elif opcion == "3":
            buscalibre.borrar_libro()
        elif opcion == "4":
            buscalibre.cargar_disponibilidad()
        elif opcion == "5":
            buscalibre.listar_libros()
        elif opcion == "6":
            buscalibre.ventas()
        elif opcion == "7":
            buscalibre.actualizar_precios()
        elif opcion == "8":
            buscalibre.mostrar_historico_libros()
        elif opcion == "9":
            buscalibre.mostrar_registros_anteriores_fecha()
        elif opcion == "10":
            buscalibre.mostrar_ventas()
        elif opcion == "0":
            print("¡Hasta luego!")
        else:
            print("Opción inválida. Inténtalo nuevamente.")


    
    conexion.desconectar()


if __name__ == "__main__":
    ejecutar_menu()
