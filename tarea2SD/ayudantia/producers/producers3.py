from kafka import KafkaProducer
from json import dumps
import time
import threading
import argparse
import random
import string

servidores_bootstrap = 'kafka:9092'

productor = KafkaProducer(
    bootstrap_servers=[servidores_bootstrap],
    value_serializer=lambda x: dumps(x).encode('utf-8')  # Se agregó un serializador para manejar directamente los diccionarios.
)

def generar_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(1, 20)))

def enviar_temperatura():
    topic = 'temperatura'  # Actualizado para consistencia
    while True:
        temperatura = round(random.uniform(10, 30), 1)
        mensaje = {
            "timestamp": int(time.time()),
            "id": generar_id(),
            "temperatura": temperatura
        }
        productor.send(topic, mensaje)  # Se envía el diccionario directamente gracias al serializador
        print('Enviando JSON:', mensaje)
        time.sleep(3)

def enviar_porcentaje_humedad():
    topic = 'porcentaje_humedad'  # Actualizado para consistencia
    while True:
        humedad = random.randint(0, 100)
        mensaje = {
            "timestamp": int(time.time()),
            "id": generar_id(),
            "porcentaje_humedad": humedad
        }
        productor.send(topic, mensaje)  # Se envía el diccionario directamente gracias al serializador
        print('Enviando JSON:', mensaje)
        time.sleep(3)

def enviar_posicion():
    topic = 'posicion'  # Actualizado para consistencia
    while True:
        posicion = random.randint(0, 10)
        mensaje = {
            "timestamp": int(time.time()),
            "id": generar_id(),
            "posicion": posicion
        }
        productor.send(topic, mensaje)  # Se envía el diccionario directamente gracias al serializador
        print('Enviando JSON:', mensaje)
        time.sleep(3)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("num_threads", type=int, help="Número de hilos a crear")
    parser.add_argument("topic", type=str, help="Topic a usar")  # Nuevo argumento para el topic
    args = parser.parse_args()

    topic_to_function = {  # Mapeo de topics a funciones
        'temperatura': enviar_temperatura,
        'porcentaje_humedad': enviar_porcentaje_humedad,
        'posicion': enviar_posicion
    }

    funcion_envio = topic_to_function.get(args.topic)  # Obtener la función basada en el topic

    if funcion_envio is not None:  # Verificar si la función existe
        threads = []
        for _ in range(args.num_threads):
            t = threading.Thread(target=funcion_envio)
            t.start()
            threads.append(t)

        # Esperar a que todos los hilos finalicen
        for t in threads:
            t.join()
    else:
        print(f"El topic {args.topic} no es válido.")