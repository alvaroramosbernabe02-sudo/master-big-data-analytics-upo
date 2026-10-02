from kafka import KafkaConsumer
from collections import Counter
import json, time

def create_consumer():
    while True:
        try:
            c = KafkaConsumer(
                'lotr', 'starwars',                 # un único consumer suscrito a los dos topics
                bootstrap_servers='kafka:9092',
                auto_offset_reset='earliest',
                group_id='wordcount-group-2')
            print("Conectado a Kafka"); return c
        except Exception as e:
            print(f"Error conectando a Kafka: {e}. Reintentando en 5s..."); time.sleep(5)

consumer = create_consumer()
word_count = Counter(); por_topic = Counter()
print("Esperando mensajes...", flush=True)
for message in consumer:
    phrase = message.value.decode('utf-8')
    por_topic[message.topic] += 1
    print(f"Recibido [{message.topic} p{message.partition} off{message.offset}]: {phrase}", flush=True)
    word_count.update(phrase.lower().split())
    print(f"Mensajes por topic: {dict(por_topic)} | top-5 palabras: {word_count.most_common(5)}", flush=True)
