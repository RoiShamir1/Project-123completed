from faker import Faker
from datetime import datetime
import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini')

class Event:
    fake = Faker()
    reporter_counter = cfg.getint('EventClass','reporterIdCounterStart')

    @classmethod
    def generate_event(cls):
        cls.reporter_counter += cfg.getint('EventClass','reporterIdCounterIncrementNumber')
        return {
            "reporterId": cls.reporter_counter,
            "timestamp": datetime.strftime(datetime.now(), '%Y-%m-%d-%H:%M:%S'),
            "metricId": cls.fake.random_int(min=cfg.getint('EventClass','metricIdMin'), max=cfg.getint('EventClass','metricIdMax')),
            "metricValue": cls.fake.random_int(min=cfg.getint('EventClass','metricValueMin'), max=cfg.getint('EventClass','metricValueMax')),
            "message": cls.fake.text(),
        }