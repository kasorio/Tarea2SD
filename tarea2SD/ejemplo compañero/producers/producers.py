from kafka import KafkaProducer
from json import dumps
import time
import threading
import argparse
import random
import string

# Configuración de los servidores Kafka y el tópico relevante
servidores_bootstrap = 'kafka:9092'
topic_inscripcion = 'inscripcion'

# Crea un productor Kafka
productor = KafkaProducer(bootstrap_servers=[servidores_bootstrap])

def generar_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(1, 20)))

def enviar_inscripcion():
    topic = topic_inscripcion
    while True:
        # Genera datos de inscripción
        nombre = 'Maestro ' + generar_id()
        email = generar_id() + '@example.com'
        estado = random.choice(['pendiente', 'aprobada', 'rechazada'])

        mensaje = {
            "timestamp": int(time.time()),
            "id": generar_id(),
            "nombre": nombre,
            "email": email,
            "estado": estado,
            "paid": random.choice([True, False])
        }
        json_mensaje = dumps(mensaje).encode('utf-8')
        productor.send(topic, json_mensaje)
        print('Enviando Inscripción:', json_mensaje)
        time.sleep(3)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("num_threads", type=int, help="Número de hilos a crear")
    args = parser.parse_args()

    threads = []
    for _ in range(args.num_threads):
        t = threading.Thread(target=enviar_inscripcion)
        t.start()
        threads.append(t)

    # Espera a que todos los hilos finalicen
    for t in threads:
        t.join()
