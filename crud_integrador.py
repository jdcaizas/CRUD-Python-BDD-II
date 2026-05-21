import pyodbc
import json


class GestorArtistas:

    # CONSTRUCTOR

    def __init__(self):

        try:

            with open('config_integrador.json', 'r') as archivo_config:

                config = json.load(archivo_config)

            name_server = config['name_server']
            database = config['database']
            controlador_odbc = config['controlador_odbc']

            self.connection_string = f'''
            DRIVER={controlador_odbc};
            SERVER={name_server};
            DATABASE={database};
            Trusted_Connection=yes;
            '''

            self.conexion = pyodbc.connect(self.connection_string)

            print("\nCONEXION EXITOSA\n")

        except Exception as e:

            print("\nERROR DE CONEXION")
            print(e)

    # INSERTAR

    def insertar_artista(self):

        try:

            idPersona = int(input("Ingrese ID Persona: "))
            nombreArtistico = input("Ingrese Nombre Artistico: ")
            oyentesMensuales = int(input("Ingrese Oyentes Mensuales: "))

            cursor = self.conexion.cursor()

            cursor.execute("""
            EXEC sp_insertar_artista ?,?,?
            """,
            (
                idPersona,
                nombreArtistico,
                oyentesMensuales
            ))

            self.conexion.commit()

            print("\nArtista insertado correctamente.")

        except Exception as e:
            print("\nError:", e)

    # CONSULTAR

    def consultar_artistas(self):

        try:

            cursor = self.conexion.cursor()

            cursor.execute("EXEC sp_consultar_artistas")

            registros = cursor.fetchall()

            print("\n===== ARTISTAS =====\n")

            for r in registros:

                print(f"""
ID Artista: {r.idArtista}
ID Persona: {r.idPersona}
Nombre Artistico: {r.nombreArtistico}
Oyentes Mensuales: {r.oyentesMensuales}
------------------------
""")

        except Exception as e:
            print("\nError:", e)

    # ACTUALIZAR

    def actualizar_artista(self):

        try:

            idArtista = int(input("Ingrese ID Artista: "))
            nombreArtistico = input("Nuevo Nombre Artistico: ")
            oyentesMensuales = int(input("Nuevos Oyentes Mensuales: "))

            cursor = self.conexion.cursor()

            cursor.execute("""
            EXEC sp_actualizar_artista ?,?,?
            """,
            (
                idArtista,
                nombreArtistico,
                oyentesMensuales
            ))

            self.conexion.commit()

            print("\nArtista actualizado.")

        except Exception as e:
            print("\nError:", e)

    # ELIMINAR

    def eliminar_artista(self):

        try:

            idArtista = int(input("Ingrese ID Artista a eliminar: "))

            cursor = self.conexion.cursor()

            cursor.execute("""
            EXEC sp_eliminar_artista ?
            """,
            (idArtista,)
            )

            self.conexion.commit()

            print("\nArtista eliminado.")

        except Exception as e:
            print("\nError:", e)

    # MENU

    def ejecutar_menu(self):

        while True:

            print("\n\t** SISTEMA CRUD STREAMING MUSICAL **")
            print("\t1. Insertar artista")
            print("\t2. Consultar artistas")
            print("\t3. Actualizar artista")
            print("\t4. Eliminar artista")
            print("\t5. Salir")

            opcion = input("\nSeleccione opción: ")

            if opcion == '1':
                self.insertar_artista()

            elif opcion == '2':
                self.consultar_artistas()

            elif opcion == '3':
                self.actualizar_artista()

            elif opcion == '4':
                self.eliminar_artista()

            elif opcion == '5':

                print("\nSaliendo...")
                self.conexion.close()
                break

            else:
                print("\nOpción inválida")


# PROGRAMA PRINCIPAL

gestor = GestorArtistas()

gestor.ejecutar_menu()