import mysql.connector
import random
import time
import json
from datetime import datetime

# Load configuration from the JSON file
def load_config(file_path='config.json'):
    with open(file_path, 'r') as file:
        return json.load(file)

config = load_config()

# Create a database connection
def create_connection():
    db_config = config['database']
    return mysql.connector.connect(user=db_config['user'],
                                   password=db_config['password'],
                                   host=db_config['host'],
                                   database=db_config['database'],
                                   auth_plugin='mysql_native_password')

# Insert a reading into the MySQL database
def insert_reading(cursor, dive_id, depth, sound_profile):
    query = ("INSERT INTO sonar_readings "
             "(dive_id, timestamp, depth, sound_profile) "
             "VALUES (%s, %s, %s, %s)")
    data = (dive_id, datetime.now(), depth, sound_profile)
    cursor.execute(query, data)

# Generate a random sound profile for simulation
def generate_sound_profile():
    return random.randbytes(20)  # Generates a random binary sound profile

# Main simulation loop
def simulate_dives():
    connection = create_connection()
    cursor = connection.cursor()
    current_dive_id = 1  # Starting dive ID
    try:
        while True:
            print("Dive started, dive ID:", current_dive_id)
            for _ in range(100):  # Generate data for 100 iterations
                depth = random.uniform(0, 100)  # Depth in meters
                sound_profile = generate_sound_profile()
                insert_reading(cursor, current_dive_id, depth, sound_profile)
                time.sleep(config['settings']['read_interval_seconds'])
            current_dive_id += 1  # Increment dive ID for the next dive
            if input("Start another dive? (y/n): ").lower() != 'y':
                break
        connection.commit()
    except Exception as e:
        print("An error occurred:", e)
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    simulate_dives()
