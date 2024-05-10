import json
from confluent_kafka import Producer
import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime
import time

def load_config(file_path='config.json'):
    """ Load configuration from a JSON file. """
    with open(file_path, 'r') as file:
        return json.load(file)

config = load_config()

def acked(err, msg):
    """ Callback function for Kafka produce acknowledgement. """
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

def buildConnection():
    """ Create and return a MySQL database connection using the loaded configuration. """
    db_config = config['database']
    connection = mysql.connector.connect(
        host=db_config['host'],
        database=db_config['database'],
        user=db_config['user'],
        password=db_config['password']
    )
    return connection

def kafka_producer():
    """ Kafka Producer to simulate sonar data using the loaded configuration. """
    kafka_conf = config['kafka']
    producer = Producer(**kafka_conf)
    topic = kafka_conf['topic']
    try:
        depth = random.uniform(5, 100)  # Depth in meters
        sound_signature = random.randint(1000, 9999)  # Simulate a sonar signature
        data = {
            'timestamp': str(datetime.now()),
            'depth': depth,
            'sound_signature': sound_signature
        }
        producer.produce(topic, json.dumps(data).encode('utf-8'))
        producer.flush()
        print(f"Produced: {data}")
    except Exception as e:
        print("Failed to produce: ", e)

def main():
    while True:
        kafka_producer()
        time.sleep(config['app_settings']['poll_interval_seconds'])  # Pause based on config setting

if __name__ == '__main__':
    main()


