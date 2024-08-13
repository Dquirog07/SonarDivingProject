CREATE KEYSPACE cave_diving WITH replication = {
    'class': 'NetworkTopologyStrategy',
    'datacenter1': 3
};

CREATE TABLE IF NOT EXISTS cave_diving.dive_summary (
    dive_id BIGINT,
    diver_id BIGINT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    summary_data TEXT,
    PRIMARY KEY (diver_id, dive_id)
);

CREATE TABLE IF NOT EXISTS cave_diving.sonar_readings (
    dive_id BIGINT,
    diver_id BIGINT,
    timestamp TIMESTAMP,
    sonar_data BLOB,
    PRIMARY KEY ((diver_id, dive_id), TIMESTAMP)
);
