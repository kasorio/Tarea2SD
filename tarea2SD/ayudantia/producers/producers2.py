from kafka import KafkaProducer
from json import dumps
import time
import random
import string

servidores_bootstrap = 'kafka:9092'
topic_temperatura = 'temperatura'

productor = KafkaProducer(
    bootstrap_servers=[servidores_bootstrap],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

def generar_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

# Mapeo de unidades a números de partición
unidad_particion_map = {
    'celsius': 0,
    'fahrenheit': 1,
    'kelvin': 2
}

def enviar_temperatura():
    topic = topic_temperatura
    unidades = ['celsius', 'fahrenheit', 'kelvin']
    while True:
        temperatura = round(random.uniform(10, 30), 1)
        unidad = random.choice(unidades)
        try:
            particion = unidad_particion_map[unidad]
            mensaje = {
                "timestamp": int(time.time()),
                "id": generar_id(),
                "temperatura": temperatura,
                "unidad": unidad
            }
            #print(particion)
            productor.send(topic, value=mensaje, partition=particion)
            print(f"Enviando JSON a la partición {particion}: {mensaje}")
        except KeyError:
            print(f"Unidad de temperatura '{unidad}' no mapeada a ninguna partición")
        except Exception as e:
            print(unidad)
            print(f"Error al enviar mensaje: {e}")

        time.sleep(3)

if __name__ == "__main__":
    enviar_temperatura()

# Ocupar el siguiente comando para crear los topics dentro de kafka: kafka-topics.sh --alter --bootstrap-server kafka:9092 --partitions 3 --topic temperatura
