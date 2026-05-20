import pyodbc


# =========================================
# MOSTRAR MENU
# =========================================

def mostrar_menu():

    print("\n")
    print("========= CRUD CURSOS =========")
    print("1. Insertar Curso")
    print("2. Consultar Cursos")
    print("3. Actualizar Curso")
    print("4. Eliminar Curso")
    print("5. Salir")


# =========================================
# INSERTAR
# =========================================

def insertar_registro(conexion):

    try:

        idcurso = int(input("Ingrese ID Curso: "))
        nombre = input("Ingrese Nombre Curso: ")
        descripcion = input("Ingrese Descripción: ")
        precio = float(input("Ingrese Precio por Hora: "))
        tipo = input("Ingrese Tipo Curso: ")

        cursor = conexion.cursor()

        sql = """
        INSERT INTO Cursos
        (IDCurso, NombreCurso, Descripcion, PrecioxHora, TipoCurso)
        VALUES (?, ?, ?, ?, ?)
        """

        cursor.execute(sql,
                       (idcurso,
                        nombre,
                        descripcion,
                        precio,
                        tipo))

        conexion.commit()

        print("\nCurso insertado correctamente.")

    except Exception as e:
        print("\nError:", e)


# =========================================
# CONSULTAR
# =========================================

def consultar_registros(conexion):

    try:

        cursor = conexion.cursor()

        sql = "SELECT * FROM Cursos"

        cursor.execute(sql)

        registros = cursor.fetchall()

        print("\n===== LISTA CURSOS =====\n")

        for r in registros:

            print(f"""
ID Curso: {r.IDCurso}
Nombre: {r.NombreCurso}
Descripción: {r.Descripcion}
Precio Hora: {r.PrecioxHora}
Tipo: {r.TipoCurso}
----------------------------
""")

    except Exception as e:
        print("\nError:", e)


# =========================================
# ACTUALIZAR
# =========================================

def actualizar_registro(conexion):

    try:

        idcurso = int(input("Ingrese ID Curso a actualizar: "))

        nuevo_nombre = input("Nuevo Nombre: ")
        nueva_descripcion = input("Nueva Descripción: ")
        nuevo_precio = float(input("Nuevo Precio: "))
        nuevo_tipo = input("Nuevo Tipo: ")

        cursor = conexion.cursor()

        sql = """
        UPDATE Cursos
        SET NombreCurso=?,
            Descripcion=?,
            PrecioxHora=?,
            TipoCurso=?
        WHERE IDCurso=?
        """

        cursor.execute(sql,
                       (nuevo_nombre,
                        nueva_descripcion,
                        nuevo_precio,
                        nuevo_tipo,
                        idcurso))

        conexion.commit()

        print("\nCurso actualizado correctamente.")

    except Exception as e:
        print("\nError:", e)


# =========================================
# ELIMINAR
# =========================================

def eliminar_registro(conexion):

    try:

        idcurso = int(input("Ingrese ID Curso a eliminar: "))

        cursor = conexion.cursor()

        sql = "DELETE FROM Cursos WHERE IDCurso=?"

        cursor.execute(sql, (idcurso,))

        conexion.commit()

        print("\nCurso eliminado correctamente.")

    except Exception as e:
        print("\nError:", e)


# =========================================
# CONEXION SQL SERVER
# =========================================

try:

    conexion = pyodbc.connect(
       'DRIVER=ODBC Driver 17 for SQL Server;'
        'SERVER=DESKTOP-LV97KDH;'
        'DATABASE=UDEMYTEST1;'
        'Trusted_Connection=yes;'
    )

    print("\nCONEXION EXITOSA\n")

    while True:

        mostrar_menu()

        opcion = input("Seleccione opción: ")

        if opcion == '1':
            insertar_registro(conexion)

        elif opcion == '2':
            consultar_registros(conexion)

        elif opcion == '3':
            actualizar_registro(conexion)

        elif opcion == '4':
            eliminar_registro(conexion)

        elif opcion == '5':

            print("\nSaliendo...")
            break

        else:
            print("\nOpción inválida.")

except Exception as e:

    print("\nERROR DE CONEXION:")
    print(e)

finally:

    try:
        conexion.close()
        print("\nConexión cerrada.")
    except:
        pass