import json
from confluent_kafka import Producer
import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime
import time
from cassandra_setup import setup_cassandra
import threading
import uuid
import pdb

def load_config(file_path='config.json'):
    """ Load configuration from a JSON file. """
    with open(file_path, 'r') as file:
        return json.load(file)

config = load_config()
kafka_conf = config['kafka']
producer = Producer(**{'bootstrap.servers': kafka_conf['bootstrap.servers']})
print('producer initialized')


def acked(err, msg):
    """ Callback function for Kafka produce acknowledgement. """
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        None
        # print("Message produced: %s" % (str(msg)))

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

def get_diver_info():
    try:
        connection = buildConnection()
        cursor = connection.cursor()

        diver_sql = "SELECT diver_id FROM divers LIMIT 1"
        cursor.execute(diver_sql)
        diver_id = cursor.fetchone()

        dive_session_sql = "SELECT dive_id FROM dives WHERE diver_id = %s AND status = 'Active' LIMIT 1"
        cursor.execute(dive_session_sql, (diver_id[0],))
        dive_id = cursor.fetchone()

        return diver_id[0], dive_id[0]

    except mysql.connector.Error as err:
        print("MySQL Error: ", err)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def produce_sonar_data(data):
    try:
        topic = kafka_conf['producer']
        topic = topic['topics']

        event_json = json.dumps(data)
        producer.produce('sonar_data', event_json.encode('utf-8'), callback=acked)
        producer.flush()
    except Exception as e:
        print("Failed to produce: ", e)

def collect_sonar_data(diver_id, dive_id):
    """ Simulate collecting sonar data. """
    depth = random.uniform(5, 100)  # Depth in meters
    sound_signature = random.randint(1000, 1010)  # Simulate a sonar signature
    data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'diver_id': diver_id,
        'dive_id': dive_id,
        'sonar_data': { 
            'depth': depth,
            'sound_signature': sound_signature}
    }
    return data

def main():

    diver_id, dive_id = get_diver_info()

    while True:
        if diver_id and dive_id:
            sonar_data = collect_sonar_data(diver_id, dive_id)
            produce_sonar_data(sonar_data)

        time.sleep(config['app_settings']['poll_interval_seconds'])

        

if __name__ == '__main__':
    main()


