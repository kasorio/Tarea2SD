kafka-topics.sh --create --bootstrap-server kafka:9092 --topic temperatura

kafka-topics.sh --create --bootstrap-server kafka:9092 --topic porcentaje_humedad

kafka-topics.sh --create --bootstrap-server kafka:9092 --topic posicion

kafka-topics.sh --create --bootstrap-server kafka:9092 --topic color

kafka-topics.sh --create --bootstrap-server kafka:9092 --topic peso

kafka-topics.sh --alter --bootstrap-server kafka:9092 --partitions 3 --topic temperatura