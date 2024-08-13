from confluent_kafka import Consumer, KafkaError
import json
from cassandra_setup import setup_cassandra


def load_config(file_path='config.json'):
    with open(file_path, 'r') as file:
        return json.load(file)

config = load_config()

session, cassandra_cluster = setup_cassandra(config)

kafka_conf = config['kafka']
consumer_conf = kafka_conf['consumer']
consumer_conf['bootstrap.servers'] = kafka_conf['bootstrap.servers']

# Initialize Consumer
consumer = Consumer(consumer_conf)
# consumer.subscribe([kafka_conf['producer']['topics']])
consumer.subscribe(['sonar_data'])
print('consumer initialized')

def project_into_cassandra(event_data):
    """Inserts the event data into Cassandra."""
    sonar_data_blob = json.dumps(event_data['sonar_data']).encode('utf-8')

    cql = """
    INSERT INTO sonar_readings (diver_id, dive_id, timestamp, sonar_data)
    VALUES (%s, %s, %s, %s)
    """
    
    session.execute(cql, (
        event_data['diver_id'],
        event_data['dive_id'],
        event_data['timestamp'],
        sonar_data_blob
    ))

try:
    while True:
        msg = consumer.poll(timeout=5.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                continue
            else:
                print(msg.error())
                break

        event_data = json.loads(msg.value().decode('utf-8'))
        project_into_cassandra(event_data)

        # print(f"Inserted event {event_data} into Cassandra.")
except KeyboardInterrupt:
    print('except')
    pass
finally:
    print('Shutting down...projection service')
    consumer.close()
    cassandra_cluster.shutdown()
