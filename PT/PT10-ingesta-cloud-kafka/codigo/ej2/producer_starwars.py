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
frases = [  # Star Wars
    "May the Force be with you",
    "Do or do not there is no try",
    "I am your father",
    "Fear is the path to the dark side",
]
while True:
    f = random.choice(frases)
    print(f"[topic=starwars] Producing: {f}", flush=True)
    producer.send('starwars', f.encode('utf-8'))
    time.sleep(2)   # antes 3 s
