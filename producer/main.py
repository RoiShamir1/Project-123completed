import json
from time import sleep
from kafka import KafkaProducer
from event import Event
import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini')

producer = KafkaProducer(
    bootstrap_servers=cfg.get('Kafka','kafka_server'),
    api_version=(0,11,5),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

while True:
    event_instance = Event()
    event_data = event_instance.generate_event()
    print(event_data)
    producer.send(cfg.get('Kafka','topic'), event_data)
    producer.flush()
    sleep(1)
