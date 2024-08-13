import subprocess
import signal
import mysql.connector
from uuid import uuid4
from datetime import datetime
import time
import json
import random
import threading


def load_config(file_path='config.json'):
    """ Load configuration from a JSON file. """
    with open(file_path, 'r') as file:
        return json.load(file)

config = load_config()

# commented out, you only need this to test once. May change design in the future
# def setup_mysql():
#     db_config = config['database']
#     connection = mysql.connector.connect(
#         host=db_config['host'],
#         database=db_config['database'],
#         user=db_config['user'],
#         password=db_config['password']
#     )
#     cursor = connection.cursor()

#     name = 'John'
#     diver_id = random.randint(10, 20)
#     dive_id = random.randint(10, 20)
#     profile_data = {'data': 1}
#     profile_data_json = json.dumps(profile_data)
#     start_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     status = 'Active'


#     record = (name, profile_data_json)
#     diver_query = "INSERT INTO divers (name, profile_data) VALUES (%s, %s)"
#     cursor.execute(diver_query, record)
#     diver_id = cursor.lastrowid

#     record = (dive_id, diver_id, start_timestamp, status)
#     dive_query = "INSERT INTO dives (dive_id, diver_id, start_timestamp, status) VALUES (%s, %s, %s, %s)"
#     cursor.execute(dive_query, record)

#     connection.commit()
#     cursor.close()
#     connection.close()
    
#     return diver_id, dive_id

def start_process(script_name):
    return subprocess.Popen(["python", script_name])

def main():
    iot_controller = start_process('Sonar_iot_controller.py')

    projection_service = start_process('projection-service.py')

    flag = True
    active = True

    while flag:
        if random.choice([True, False]): 
            active = False

        if not active:
            time.sleep(1)
            print("Ending dive and processing end dive data...")
            end_dive = subprocess.run(["python", 'end_dive.py'])

            iot_controller.send_signal(signal.SIGTERM)
            projection_service.send_signal(signal.SIGTERM)
            flag = False
        time.sleep(10)




if __name__ == "__main__":
    main()
