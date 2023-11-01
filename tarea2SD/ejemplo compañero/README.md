# Ayudantia-Kafka
joaquin.fernandez1@mail.udp.cl

Para levantar topologia de contenedores:
```sh
docker compose up --build
```
Para visualizar contenedores y sus estados:
```sh
docker ps -a
```
---
Para realizar pruebas pertinentes entre par producer y consumer colocar los siguientes comandos:

Entran al producer
```sh
docker exec -it producer_kafka bash
```
Entran al consumer:
```sh
docker exec -it consumer_kafka bash
```
## *Caso1*
Para el primer caso que es de trabajo con Consumer Groups, ejecutar el siguiente comando dentro de la bash del contenedor producer (se coloca un numero como argumento ya que está usando threads para que no hayan conflictos con enviados anteriores):
```sh
python3 producers.py 5
```
Luego dentro de la bash del consumer ejecutan el siguiente comando:
```sh
python3 consumers.py
```
nota: el producer estara enviando y el consumer se demora un poco en establecer la conexión con el producer en caso que se demore un poco en recibir la información, ahí tendrán que esperar.

## *Caso2*
Para el segundo caso que es de trabajo con particiones, está la conexión simplificada entre topics lo importante es el trabajo de los subtopics y estos vendíran a ser las particiones como lo es en el ejemplo de temperatura con casos como celcius, kelvin y fahrenheit.

Aunque deben de entrar en otra bash a kafka esto con la razón de que kafka debe de identificar que las particiones existen y están asociadas al topic respectivo y pueden hacerlo con el siguiente comando (cabe recordar que deben de entrar a la consola del servicio kafka (docker exec -it kafka bash)):
```sh
kafka-topics.sh --alter --bootstrap-server kafka:9092 --partitions 3 --topic temperatura
```

Nuevamente para la ejecución del producer deben de colocar el siguiente comando:
```sh
python3 producers2.py 5
```

Nuevamente para la ejecución del consumer deben de colocar el siguiente comando:
```sh
python3 consumers2.py
```

## *Caso3*
Para el tercer caso se aplicó el uso de brokers, ya que se trabaja con clusters de kafka entonces se tendrían cada topic adherido con un contenedor en específico casi como un server de kafka que trabaja con varios producers a la vez. \
Primero deben de ejecutar el docker-compose-brokers.yml para levantar la topología mediante el siguiente comando:
```sh
docker compose -f docker-compose-brokers.yml up --build
```
Por lo que para ejecutar cada contenedor se deben de aplicar los siguientes comandos:
```sh
docker exec -it producer_kafka bash
docker exec -it producer_kafka2 bash
docker exec -it producer_kafka3 bash
```
Aquí deben de aplicar en cada uno de ellos el siguiente comando:\
Para el producer dentro del primer contenedor:
```sh
python3 producers3.py 4 temperatura
```
Para el producer dentro del segundo contenedor:
```sh
python3 producers3.py 4 porcentaje_humedad
```
Para el producer dentro del tercer contenedor:
```sh
python3 producers3.py 4 posicion
```
Para el consumer:
```sh
python3 consumers3.py
```
Y debería de aparecer en el consumer los mensajes de cada uno de los topics asociados al servidor de Kafka procedentes de cada contenedor.\
Por último para bajar la topología deben de ejecutar el siguiente comando:
```sh
docker compose -f docker-compose-brokers.yml down -v
```

## *Ejemplo Conexión DB*
Para realizar pruebas de conexión a DB se dejó un ejemplo con postgresql, de igual forma pueden hacer lo mismo con cualquier otra base detaos de su gusto. Cabe recalcar que esta es una app de prueba, tendrán que por su parte hacer los cambios pertinenetes que se aomoden a lo solicitado en su tarea.\
Para levantar la topología deben de colocar el siguiente comando:
```sh
docker compose -f docker-compose-db.yml up --build
```
Luego tienen que entrar al servicio pertinente de example-app, mediante el siguiente comando:
```sh
docker exec -it example-app bash
```
Luego tienen que ejecutar el siguiente comando para que imprima una simple query por consola desde el archivo main.py
```sh
python3 main.py
```
## *Configuración DB*
Para todo lo que es configuración de la db pueden cambiar el archivo init.sql que se encuentra en la carpeta db.\
Ahora bien si quieren interactura directamente con el servicio de postgres, pueden hacerlo a travez de la interfaz de pgadmin \
Deben de entrar al siguiente dominio desde su ordenador
```sh
lohalhost:81
```
Ahí tendrán una interfaz de login de usuario las credenciales se encuentran en el compose.\
Luego Tendrán que dar click derecho en servers, dan click en Register y luego en Server. Posterior a ello se abrirá una ventana en donde tendrán que colocar:\

*General*:
- Name: db

*Connection*:
- Host name/address: db
- Maintenance database: proyecto
- Username: postgres
- Password: postgres
- Dan click en Save y sha esta.

O también pueden utilizar la misma bash para establecer la conexión mediante los siguiente comandos:\
En otra bash o desde docker desktop entran al servicio, en caso que usen la bash pueden aplicar simplemente la siguiente instrucción:
```sh
docker exec -it db bash
```
Luego de estar dentro del servicio aplicar el siguiente comando:
```sh
psql -d proyecto -U postgres
```
Y ya con eso deberían de estar conectados a su respectiva db.