from kafka import KafkaConsumer
import json  # Agrega la importación de json para deserializar los mensajes

servidores_bootstrap = 'kafka:9092'
topics = ['temperatura', 'porcentaje_humedad', 'posicion']

grupo_consumidores = 'grupo_consumidores'

# Configurar el consumidor con el group_id y añadir deserializador de json
consumer = KafkaConsumer(
    *topics,
    group_id=grupo_consumidores,
    bootstrap_servers=[servidores_bootstrap],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  
)

# Consumir mensajes de los topics elegidos
for msg in consumer:
    print(f"Recibido de tópico {msg.topic}: {msg.value}")

    if msg.topic == 'temperatura':
        print(f"Procesando temperatura: {msg.value['temperatura']}°C")
    elif msg.topic == 'porcentaje_humedad':
        print(f"Procesando humedad: {msg.value['porcentaje_humedad']}%")
    elif msg.topic == 'posicion':
        print(f"Procesando posición: {msg.value['posicion']}")
