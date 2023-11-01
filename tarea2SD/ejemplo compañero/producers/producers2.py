from kafka import KafkaProducer
from json import dumps
import time
import random
import string

servidores_bootstrap = '172.18.0.3:9092'
topic_ingredientes = 'ingredientes'

productor = KafkaProducer(
    bootstrap_servers=[servidores_bootstrap],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

def generar_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

def enviar_falta_stock():
    topic = topic_ingredientes
    ingredientes = ['mote', 'pepino', 'durazno', 'azúcar', 'agua', 'huesillo']

    
    while True:
        ingrediente = random.choice(ingredientes)
        cantidad = random.randint(0, 10)  # Simula la cantidad en stock

        if cantidad <= 1:
            try:
                mensaje = {
                    "timestamp": int(time.time()),
                    "id": generar_id(),
                    "ingrediente": ingrediente,
                    "stock": cantidad
                }
                productor.send(topic, value=mensaje)
                print(f"Falta de stock notificada para {ingrediente}. Stock actual: {cantidad}")
            except Exception as e:
                print(f"Error al enviar mensaje: {e}")

        time.sleep(60 * 30)  # Comprueba la falta de stock cada 30 minutos

if __name__ == "__main__":
    enviar_falta_stock()
