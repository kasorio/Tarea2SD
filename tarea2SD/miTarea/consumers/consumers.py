#codigo utilizado de github proporcionado por los ayudantes

from kafka import KafkaConsumer
import psycopg2
import json
import random
import string, time
from datetime import datetime

servidores_bootstrap = 'kafka:9092'

DATABASE_CONFIG = {
    'dbname': 'proyecto',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'db',
    'port': '5432'
}

def generar_id():
    return ''.join(random.choices(string.digits, k=10))
    #return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

def consume_messages(topic_name, table_name):
    # Conectar a PostgreSQL
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()
    consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=servidores_bootstrap,
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    consumer_timeout_ms=5000  # Cierra el consumidor después de 5 segundos si no se reciben mensajes
)

    mensajes_guardados = []  # Lista para guardar los primeros 10 mensajes
    cont = 0
    
    try:
        for message in consumer:
            if cont == 10:
                break
            print(f"Recibido mensaje de {message.topic} en la partición {message.partition} con offset {message.offset}:")
            print(message.value)
            
            # Agregamos el mensaje a la lista
            mensajes_guardados.append(message.value)
            
            # Generar un timestamp actual
            timestamp = datetime.now().isoformat()
            
            # Crear una copia del mensaje y agregar el timestamp
            message_with_timestamp = message.value.copy()
            message_with_timestamp['timestamp'] = timestamp
            
            columns = ", ".join(message_with_timestamp.keys())
            values = tuple(message_with_timestamp.values())

            #insertar en base de datos
            #insert_query = f"INSERT INTO {table_name} ({columns}) VALUES {tuple(['%s' for _ in values])}"
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({', '.join(['%s' for _ in values])})"

            cursor.execute(insert_query, values)
            conn.commit()

            cont += 1
    finally:
        # Cerramos el consumidor explícitamente
        consumer.close()
        # Imprimir los mensajes guardados
        print("Mensajes guardados:", mensajes_guardados)


    # Ahora, la variable `mensajes_guardados` tiene los primeros 10 mensajes
    print("Mensajes guardados:", mensajes_guardados)

if __name__ == "__main__":
    print("Menú Consumidores:")
    print("1. Consumir mensajes de mote.formulario")
    print("2. Consumir mensajes de mote.ingredientes")
    print("3. Consumir mensajes de mote.ventas")
    print("4. Salir")

    opcion = input("Elige una opción: ")

    if opcion == "1":
        consume_messages('mote.formulario', 'formulario')
        print("Consumiendo mensajes de mote.formulario")
    elif opcion == "2":
        consume_messages('mote.ingredientes', 'ingredientes')
    elif opcion == "3":
        consume_messages('mote.ventas', 'ventas')
    elif opcion == "4":
        print("Saliendo...")
    else:
        print("Opción no válida.")
