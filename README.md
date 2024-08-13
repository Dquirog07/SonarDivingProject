Project Idea: Cave Diving Sonar Navigation System

Domain: The proposed application simulates a sonar navigation system designed specifically for cave divers. 

## Overview

This application leverages Kafka for data streaming, MySQL for relational data storage, Cassandra for distributed storage, and Python scripts to manage and manipulate the data. The application consists of several components, each responsible for a specific task in the overall system.

### Components

1. **Projection Service**: 
   - Consumes data from the Kafka topic `sonar_data` and projects it into Cassandra for long-term storage.
   
2. **IoT Controller**:
   - Generates sonar data simulating a dive and streams this data via Kafka to be consumed by other services.

3. **End Dive Service**:
   - Acts as a consumer on the Kafka stream when a dive ends. It collects all the data for the dive from Cassandra, inverts the data, and then makes active comparisons with the data being produced by the IoT controller to determine if the diver is heading back to the start point.

4. **Simulate.py**:
   - A multi-process script that orchestrates the execution of the above services in parallel and terminates them once the simulation is complete.

## Setup Instructions

### Prerequisites

- Docker installed on your system.
- Docker Compose installed.
- Python 3.8 or above installed on your system.
- MySQL and Cassandra Docker images available locally.

### Application Components

#### Step 4: Running the Application

1. **Projection Service**:
   - The `projection-service.py` script consumes the `sonar_data` topic from Kafka and inserts the data into Cassandra.

2. **IoT Controller**:
   - The `Sonar_iot_controller.py` script generates simulated sonar data and streams it to the Kafka topic `sonar_data`.

3. **End Dive Service**:
   - The `end_dive.py` script triggers when a dive ends. It consumes data from Kafka, inverts the sonar readings from Cassandra, and compares the live stream data against these inverted values to determine if the diver is heading back to the start point.

4. **Simulate.py**:
   - The `simulate.py` script orchestrates the entire process by running the IoT controller, projection service, and end dive service in parallel. It monitors the progress and terminates the processes once the simulation is complete.

### Running the Simulation

To run the entire application, simply execute the `simulate.py` script:

```bash
python simulate.py
```

This script will start all required services, run the simulation, and then clean up by terminating the processes.

## Notes

- **Kafka Configuration**: Ensure that Kafka is configured to allow multiple consumers on the same topic.
- **Concurrency**: The `simulate.py` script is designed to run services in parallel. Ensure that your system can handle the concurrent execution of multiple processes.
- **Shutdown**: The `simulate.py` script handles process termination gracefully. Ensure that all processes are properly joined or terminated after the simulation.

## Troubleshooting

- **Connection Issues**: If you encounter connection issues, ensure that all containers are running and accessible via the specified network.
- **Logs**: Check the logs of each Docker container to troubleshoot issues:
  ```bash
  docker logs [container_name]
  ```
