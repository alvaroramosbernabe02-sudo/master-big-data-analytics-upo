from kafka import KafkaConsumer
from collections import Counter
import json
import time

# Intentar conectarse a Kafka con reintentos
def create_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                'wordcount',
                bootstrap_servers='kafka:9092',
                auto_offset_reset='earliest',
                group_id='wordcount-group'
            )
            print("Conectado a Kafka")
            return consumer
        except Exception as e:
            print(f"Error conectando a Kafka: {e}. Reintentando en 5s...")
            time.sleep(5)

consumer = create_consumer()
word_count = Counter()

print("Esperando mensajes...")

for message in consumer:
    phrase = message.value.decode('utf-8')
    print(f"Recibido: {phrase}")

    words = phrase.lower().split()  # Convertir a minúsculas y dividir en palabras
    word_count.update(words)  # Actualizar conteo de palabras

    print(f"Conteo actual: {json.dumps(dict(word_count), indent=2)}")
