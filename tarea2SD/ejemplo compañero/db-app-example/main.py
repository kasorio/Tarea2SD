from connection import init_db


def ver_registros(tabla):
    # Consulta SELECT
    cursor.execute(f"SELECT * FROM {tabla}")
    registro = cursor.fetchall()
    print(registro)


if __name__ == "__main__":
    conn = init_db()
    cursor = conn.cursor()

    print("Menú de Tablas:")
    print("1. Ver registros de formulario")
    print("2. Ver registros de ingredientes")
    print("3. Ver registros de ventas")
    print("4. Salir")

    opcion = input("Elige una opción: ")

    if opcion == "1":
        ver_registros('formulario')
    elif opcion == "2":
        ver_registros('ingredientes')
    elif opcion == "3":
        ver_registros('ventas')
    elif opcion == "4":
        print("Saliendo...")
    else:
        print("Opción no válida.")