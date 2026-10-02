from kafka import KafkaProducer
import random, time

def create_producer():
    while True:
        try:
            p = KafkaProducer(bootstrap_servers="kafka:9092")
            print("Conectado a Kafka"); return p
        except Exception as e:
            print(f"Error conectando a Kafka: {e}. Reintentando en 5s..."); time.sleep(5)

producer = create_producer()
frases = [  # El Señor de los Anillos
    "Not all those who wander are lost",
    "Even the smallest person can change the course of the future",
    "All we have to decide is what to do with the time that is given us",
    "One ring to rule them all",
]
while True:
    f = random.choice(frases)
    print(f"[topic=lotr] Producing: {f}", flush=True)
    producer.send('lotr', f.encode('utf-8'))
    time.sleep(2)   # antes 3 s
