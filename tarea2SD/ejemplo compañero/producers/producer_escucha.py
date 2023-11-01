from kafka import KafkaConsumer
import json

# Configura los servidores de Kafka y el tema 'stock.agotado'
servidores_bootstrap = 'kafka:9092'
topic_stock_agotado = 'stock.agotado'

# Configura el consumidor de Kafka
consumer = KafkaConsumer(
    topic_stock_agotado,
    bootstrap_servers=servidores_bootstrap,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Función para manejar mensajes de stock agotado
def manejar_stock_agotado(message):
    print("Stock de Mote con Huesillo agotado. Se requiere reposición.")
    print("Mensaje recibido:")
    print(message)

# Función para visualizar mensajes recibidos por el consumidor
def visualizar_mensajes_recibidos():
    print("Mensajes recibidos por el consumidor:")
    for message in consumer:
        print(f"Mensaje de {message.topic} en la partición {message.partition} con offset {message.offset}:")
        print(message.value)

if __name__ == "__main__":
    while True:
        print("\nMenú:")
        print("1. Escuchar mensajes de stock agotado")
        print("2. Visualizar mensajes recibidos por el consumidor")
        print("3. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            # Escucha continuamente el tema 'stock.agotado' y maneja los mensajes
            for message in consumer:
                manejar_stock_agotado(message.value)

        elif opcion == "2":
            # Visualiza mensajes recibidos por el consumidor
            visualizar_mensajes_recibidos()

        elif opcion == "3":
            print("Saliendo...")
            break

        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
