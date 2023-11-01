from kafka import KafkaConsumer
import json

servidores_bootstrap = '172.18.0.3:9092'
topic_ingredientes = 'ingredientes'
grupo_consumidores = 'grupo_consumidores_ingredientes'

consumer = KafkaConsumer(
    topic_ingredientes,
    group_id=grupo_consumidores,
    bootstrap_servers=[servidores_bootstrap],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def reponer_stock(ingrediente):
    # Lógica para reponer el stock del ingrediente
    print(f"Reponiendo stock de {ingrediente} inmediatamente.")

# Consumir mensajes relacionados con la reposición de stock
for msg in consumer:
    print("Mensaje recibido:", msg.value)  # Agrega esta línea para imprimir el mensaje recibido
    ingrediente = msg.value.get('ingrediente')
    stock = msg.value.get('stock')

    if ingrediente is not None and stock is not None:
        if stock <= 1:
            reponer_stock(ingrediente)
        else:
            print(f"Stock de {ingrediente} es suficiente: {stock} unidades")
    else:
        print("Mensaje incompleto recibido.")
