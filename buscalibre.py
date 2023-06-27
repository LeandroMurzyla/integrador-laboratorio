import sqlite3

# Función para establecer la conexión a la base de datos
def conectar():
    conexion = sqlite3.connect('buscalibre.db')
    return conexion

# Función para cerrar la conexión a la base de datos
def cerrar_conexion(conexion):
    conexion.close()

# Función para crear las tablas si no existen
def crear_tablas():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Libros
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    ISBN TEXT UNIQUE,
                    Titulo TEXT,
                    Autor TEXT,
                    Genero TEXT,
                    Precio REAL,
                    FechaUltimoPrecio DATE,
                    CantDisponible INTEGER)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Ventas
                    (ID INTEGER,
                    Cantidad INTEGER,
                    Fecha DATE,
                    FOREIGN KEY(ID) REFERENCES Libros(ID))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS historico_libros
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    ISBN TEXT UNIQUE,
                    Titulo TEXT,
                    Autor TEXT,
                    Genero TEXT,
                    Precio REAL,
                    FechaUltimoPrecio DATE,
                    CantDisponible INTEGER)''')

    conexion.commit()
    cerrar_conexion(conexion)

# Función para ejecutar consultas SELECT
def ejecutar_consulta(query):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(query)
    resultado = cursor.fetchall()
    cerrar_conexion(conexion)
    return resultado

# Función para ejecutar consultas INSERT, UPDATE o DELETE
def ejecutar_actualizacion(query, parametros):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(query, parametros)
    conexion.commit()
    cerrar_conexion(conexion)

# Llamada a la función crear_tablas para asegurarnos de que las tablas existan
crear_tablas()
