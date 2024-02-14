import json
from kafka import KafkaConsumer
from pymongo import MongoClient
from datetime import datetime
import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini')

consumer = KafkaConsumer(
    cfg.get('Kafka','topic'),
    bootstrap_servers=cfg.get('Kafka','kafka_server'),
    api_version=(0,11,5),
    auto_offset_reset=cfg.get('Kafka','autoOffsetReset'),
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

mongo_client = MongoClient(cfg.get('MongoDb','MongoConnectionString'))
db = mongo_client[cfg.get('MongoDb','MongoDbName')]
collection = db[cfg.get('MongoDb','MongoDbCollectionName')]

for message in consumer:
    print("Received message from Kafka")
    event_data = message.value
    print("Event Data:", event_data)

    event_data["timestamp"] = datetime.strptime(event_data["timestamp"], '%Y-%m-%d-%H:%M:%S')
    collection.insert_one(event_data)
    print("Inserted into MongoDB")