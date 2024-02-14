import json
import redis
from pymongo import MongoClient
from datetime import datetime
import time
import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini')

mongo_client = MongoClient(cfg.get('MongoDb','MongoConnectionString'))
mongo_db = mongo_client[cfg.get('MongoDb','MongoDbName')]
mongo_collection = mongo_db[cfg.get('MongoDb','MongoDbCollectionName')]

redis_client = redis.Redis(host=cfg.get('Redis','RedisHostName'), port=cfg.getint('Redis','RedisPort'), decode_responses=True)

def get_latest_timestamp():
    latest_timestamp = redis_client.get('latest_timestamp')
    if latest_timestamp:
        return datetime.strptime(latest_timestamp, '%Y-%m-%d-%H:%M:%S')
    return None

def update_latest_timestamp(timestamp):
    redis_client.set('latest_timestamp', timestamp.strftime('%Y-%m-%d-%H:%M:%S'))
    print(f"---------------------latest_timestamp: {timestamp}---------------------")

def process_new_objects():
    latest_timestamp = get_latest_timestamp()

    query = {"timestamp": {"$gt": latest_timestamp}} if latest_timestamp else {}
    new_objects = list(mongo_collection.find(query).sort("timestamp", 1))

    for obj in new_objects:
        key = f"{obj['reporterId']}:{datetime.strftime(obj['timestamp'],'%Y-%m-%d-%H:%M:%S')}"
        obj_json = json.dumps(obj, default=str)
        redis_client.set(key, obj_json)
        print(f"Inserted new object into Redis: {obj_json}")
        update_latest_timestamp(obj['timestamp'])


def main():
    while True:
        process_new_objects()
        time.sleep(cfg.getint('Redis','RedisSleepTime'))

if __name__ == "__main__":
    main()