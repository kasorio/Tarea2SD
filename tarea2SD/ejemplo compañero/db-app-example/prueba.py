import psycopg2

# Configuración de la base de datos
DATABASE_CONFIG = {
    'dbname': 'proyecto',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'db'
}

def consultar_datos(tabla):
    # Conectar a PostgreSQL
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    # Consulta SELECT
    cursor.execute(f"SELECT * FROM {tabla}")
    registros = cursor.fetchall()

    # Imprimir los registros
    for registro in registros:
        print(registro)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    # Nombre de la tabla que deseas consultar
    tabla = 'formulario'

    # Llama a la función para consultar los datos de la tabla
    consultar_datos(tabla)
