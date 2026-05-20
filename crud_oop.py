import pyodbc
import json


class GestorEstudiantes:

    def __init__(self):

        try:

            with open('config.json', 'r') as archivo_config:

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


    def insertar_estudiante(self):

        try:

            id_estudiante = int(input("ID Estudiante: "))
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            email = input("Email: ")
            telefono = input("Telefono: ")

            cursor = self.conexion.cursor()

            cursor.execute("""
            EXEC sp_insertar_estudiante ?,?,?,?,?
            """,
            (
                id_estudiante,
                nombre,
                apellido,
                email,
                telefono
            ))

            self.conexion.commit()

            print("\nEstudiante insertado correctamente.")

        except Exception as e:
            print("\nError:", e)


    # CONSULTAR
  

    def consultar_estudiantes(self):

        try:

            cursor = self.conexion.cursor()

            cursor.execute("EXEC sp_consultar_estudiantes")

            registros = cursor.fetchall()

            print("\n===== ESTUDIANTES =====\n")

            for r in registros:

                print(f"""
ID: {r.IDEstudiante}
Nombre: {r.NombreEstudiante}
Apellido: {r.ApellidoEstudiante}
Email: {r.Email}
Telefono: {r.Telefono}
------------------------
""")

        except Exception as e:
            print("\nError:", e)

   
    # ACTUALIZAR
    

    def actualizar_estudiante(self):

        try:

            id_estudiante = int(input("ID Estudiante: "))
            nombre = input("Nuevo Nombre: ")
            apellido = input("Nuevo Apellido: ")
            email = input("Nuevo Email: ")
            telefono = input("Nuevo Telefono: ")

            cursor = self.conexion.cursor()

            cursor.execute("""
            EXEC sp_actualizar_estudiante ?,?,?,?,?
            """,
            (
                id_estudiante,
                nombre,
                apellido,
                email,
                telefono
            ))

            self.conexion.commit()

            print("\nEstudiante actualizado.")

        except Exception as e:
            print("\nError:", e)

    
    # ELIMINAR
    

    def eliminar_estudiante(self):

        try:

            id_estudiante = int(input("ID Estudiante a eliminar: "))

            cursor = self.conexion.cursor()

            cursor.execute("""
            EXEC sp_eliminar_estudiante ?
            """,
            (id_estudiante,)
            )

            self.conexion.commit()

            print("\nEstudiante eliminado.")

        except Exception as e:
            print("\nError:", e)

    # MENU
    
    def ejecutar_menu(self):

        while True:

            print("\n\t** SISTEMA CRUD UDEMYTEST **")
            print("\t1. Crear registro")
            print("\t2. Consultar registros")
            print("\t3. Actualizar registro")
            print("\t4. Eliminar registro")
            print("\t5. Salir")

            opcion = input("\nSeleccione opción: ")

            if opcion == '1':
                self.insertar_estudiante()

            elif opcion == '2':
                self.consultar_estudiantes()

            elif opcion == '3':
                self.actualizar_estudiante()

            elif opcion == '4':
                self.eliminar_estudiante()

            elif opcion == '5':

                print("\nSaliendo...")
                self.conexion.close()
                break

            else:
                print("\nOpción inválida")


# =====================================
# PROGRAMA PRINCIPAL
# =====================================

gestor = GestorEstudiantes()

gestor.ejecutar_menu()