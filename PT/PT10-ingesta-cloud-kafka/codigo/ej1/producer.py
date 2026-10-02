from kafka import KafkaProducer
import random
import time

# Intentar conectarse a Kafka con reintentos
def create_producer():
    while True:
        try:
            producer = KafkaProducer(bootstrap_servers="kafka:9092")
            print("Conectado a Kafka")
            return producer
        except Exception as e:
            print(f"Error conectando a Kafka: {e}. Reintentando en 5s...")
            time.sleep(5)

# Crear el productor con reintentos
producer = create_producer()

# Función para generar frases aleatorias
def generate_phrases():
    phrases = [
        "Happiness can be found even in the darkest of times",
        "It is our choices that show what we truly are",
        "Fear of a name increases fear of the thing itself",
        "We are only as strong as we are united"
    ]
    return random.choice(phrases)

# Enviar frases al tema 'wordcount'
while True:
    phrase = generate_phrases()
    print(f"Producing: {phrase}")
    producer.send('wordcount', phrase.encode('utf-8'))
    time.sleep(3)  # Espera 3 segundos antes de enviar otra frase
