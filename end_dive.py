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
print('consumer initialized in end_dive')

def invert_dive(session, diver_id, dive_id):
    cql = """
    SELECT *
    FROM sonar_readings
    WHERE diver_id = %s AND dive_id = %s
    ORDER BY timestamp DESC
    """
    rows = session.execute(cql, (diver_id, dive_id))
    rows_list = list(rows)
    inverted_data = {}
    total = len(rows_list)
    count = 1

    for row in rows_list:
        # Access the BLOB data
        sonar_data_blob = row.sonar_data
        
        sonar_data_str = sonar_data_blob.decode('utf-8')
        sonar_data = json.loads(sonar_data_str)
        sound_signature = sonar_data['sound_signature']
        depth = sonar_data['depth']

        inverted_data[sound_signature] = (depth, count/total)
        count += 1
    return inverted_data


def compare_with_inverted_data(inverted_data, sonar_data):
    """ Compare collected sonar data with the inverted data from Cassandra. """
    if sonar_data['sound_signature'] in inverted_data:
        depth, percentage = inverted_data[sonar_data['sound_signature']]
        
        print(f"Heading towards the start location based on data from {sonar_data['sound_signature']}, Progress: {percentage}")
        # Comparison logic
        if percentage > .90:
            print(f"You are more than 90% there! {event_data['timestamp']}, Progress: {percentage}")
            return True
    else:
        print(f' this is the current sound signatures in inverted: {inverted_data}')
        print(f' heading away from start point:{sonar_data["sound_signature"]} ')
    return False

try: 
    flag = True
    while flag:
        msg = consumer.poll(timeout=5.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break
        event_data = json.loads(msg.value().decode('utf-8'))
        # print(f'end_dive event data {event_data}')
        sonar_data = event_data['sonar_data']
        diver_id = event_data['diver_id']
        dive_id = event_data['dive_id']
        inverted_data = invert_dive(session, diver_id, dive_id)
        if compare_with_inverted_data(inverted_data, sonar_data):
            print("End dive sequence: Diver is back at start location.")
            flag = False
            
except KeyboardInterrupt:
    print('Keyboard Interrupt - Exiting')
finally:
    print('Shutting down...end_dive')
    consumer.close()
    cassandra_cluster.shutdown()
