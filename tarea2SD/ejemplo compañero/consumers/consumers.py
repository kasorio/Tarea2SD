from kafka import KafkaConsumer
import json
import psycopg2

servidores_bootstrap = 'kafka:9092'
DATABASE_CONFIG = {
    'dbname': 'proyecto',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'db'
}

def consume_messages(topic_name, table_name):
    # Conectar a PostgreSQL
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=servidores_bootstrap,
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        print(f"Recibido mensaje de {message.topic}: {message.value}")
        columns = ", ".join(message.value.keys())
        values = tuple(message.value.values())
        placeholders = ", ".join(['%s'] * len(message.value))  # Crear marcadores de posición
        insert_stmt = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        try:
            cursor.execute(insert_stmt, values)
            conn.commit()
        except psycopg2.Error as e:
            print(f"Error al insertar en la base de datos: {e}")
            conn.rollback()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("Menú Consumidores:")
    print("1. Consumir mensajes de inscripcion y almacenar en 'formulario'")
    print("2. Consumir mensajes de otro topic y almacenar en otra tabla")
    print("3. Salir")

    opcion = input("Elige una opción: ")

    if opcion == "1":
        consume_messages('inscripcion', 'formulario')
    elif opcion == "2":
        # Personaliza el nombre del topic y la tabla
        custom_topic = input("Ingresa el nombre del topic: ")
        custom_table = input("Ingresa el nombre de la tabla: ")
        consume_messages(custom_topic, custom_table)
    elif opcion == "3":
        print("Saliendo...")
    else:
        print("Opción no válida.")
