import psycopg2 as pg
from time import sleep
import tqdm
from tabulate import tabulate

for i in tqdm.tqdm(range(100)):
    sleep(0)


host_name = 'localhost'
data_base = 'test1'
username = 'postgres'
pwd = '123456789'
port_id = 5432

conn = None

try:
    conn = pg.connect(
        host = host_name, 
        database = data_base,
        user = username,
        password = pwd,
        port = port_id
    )

    print("Conexión Exitosa")

    c = conn.cursor()
    c.execute("""
                CREATE TABLE if not exists cliente(
                    rut TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    empresa TEXT NOT NULL
                );
    """)

    conn.commit()

    opcion = input("Ingrese la opcion que desea realizar: \n(1) Ingresar Cliente \n(2) Visualizar Clientes \n(3) Actualizar Cliente \n(4) Eliminar Cliente \n(5) Salir : ")
    print("\n")
    while opcion != '5':
        if opcion == '1':
            nombre = input("Ingrese nombre del cliente: ")
            rut = input("Ingrese el RUT de {}: ".format(nombre))
            telefono = input("Ingrese el teléfono de {}: ".format(nombre))
            empresa = input("Ingrese la empresa de {}: ".format(nombre))

            c.execute("INSERT INTO cliente (rut, nombre, telefono, empresa) values (%s, %s, %s, %s)",(rut, nombre, telefono, empresa))
            conn.commit()

            print("\n")

        if opcion == '2':
            c.execute("SELECT * FROM cliente")
            registros = c.fetchall()
            conn.commit()
            registros = list(registros)
            registros.insert(0, ("Rut", "Nombre", "Teléfono", "Empresa"))
            print(tabulate(registros, tablefmt='fancy_grid'))
            print("\n")

        if opcion == '3':
            id = input("Ingrese el rut del cliente que desea actualizar: ")
            c.execute("SELECT * FROM cliente WHERE rut = %s", (id,))
            cliente_actualizar = c.fetchall()
            print(tabulate(cliente_actualizar, tablefmt='fancy_grid'))
            conn.commit()
            print("\n")
            
            print("Ingrese los datos a actualizar: ")
            nombre_a = input("Ingrese el nuevo Nombre: ")
            telefono_a = input("Ingrese el nuevo Teléfono: ")
            empresa_a = input("Ingrese nueva Empresa:")
            c.execute("UPDATE cliente SET nombre = %s, telefono = %s, empresa = %s WHERE rut = %s", (nombre_a, telefono_a, empresa_a, id))
            conn.commit()
            print("\n")
            print("El cliente ha sido modificado satisfactoriamente. ")
            print("\n")

        if opcion == '4':
            id = input("Ingrese el rut que desea eliminar: ")
            c.execute("SELECT * FROM cliente WHERE rut = %s", (id,))
            cliente_eliminar = c.fetchall()
            conn.commit()
            print(tabulate(cliente_eliminar, tablefmt='fancy_grid'))
            print("\n")
            respuesta = input("\n¿Está seguro de eliminar el siguiente registro?: (Si)(No)")
            if respuesta == 'Si':
                c.execute("DELETE FROM cliente WHERE rut = %s", (id, ))
                conn.commit()
                print("El registro ha sido eliminado correctamente")
            else:
                print("El registro no ha sido eliminado")
        
        
        opcion = input("Ingrese la opcion que desea realizar: \n(1) Ingresar Cliente \n(2) Visualizar Clientes \n(3) Actualizar Cliente \n(4) Eliminar Cliente \n(5) Salir : ")

except Exception as error:
    print("Error al conectarse a la base de datos", error)


conn.close()