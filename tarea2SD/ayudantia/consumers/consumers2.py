from kafka import KafkaConsumer
import json

servidores_bootstrap = 'kafka:9092'
topic_temperatura = 'temperatura'
grupo_consumidores = 'grupo_consumidores_temperatura'

consumer = KafkaConsumer(
    topic_temperatura,
    group_id=grupo_consumidores,
    bootstrap_servers=[servidores_bootstrap],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Se utiliza json.loads para deserializar el mensaje JSON
)

# Consumir mensajes de los topics elegidos
for msg in consumer:
    # Utilizamos el método get() para evitar KeyError en caso de que la clave no exista en el mensaje
    temperatura = msg.value.get('temperatura')
    unidad = msg.value.get('unidad')

    # Verificamos si tanto la temperatura como la unidad están presentes antes de intentar imprimirlos
    if temperatura is not None and unidad is not None:
        print(f"Topic: {msg.topic}, Partición: {msg.partition}, Unidad: {unidad}, Temperatura: {temperatura}")
    else:
        print("Mensaje incompleto recibido.")