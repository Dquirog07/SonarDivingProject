CREATE KEYSPACE cave_diving WITH replication = {
    'class': 'NetworkTopologyStrategy',
    'datacenter1': 3
};

CREATE TABLE cave_diving.dives (
    dive_id UUID PRIMARY KEY,
    diver_id UUID,
    start_timestamp TIMESTAMP,
    end_timestamp TIMESTAMP,
    start_location TEXT,
    end_location TEXT
);

CREATE TABLE cave_diving.events (
    dive_id UUID,
    event_timestamp TIMESTAMP,
    event_type TEXT,
    location TEXT,
    details TEXT,
    PRIMARY KEY (dive_id, event_timestamp)
) WITH CLUSTERING ORDER BY (event_timestamp DESC);

CREATE TABLE cave_diving.cookies (
    dive_id UUID,
    cookie_id UUID PRIMARY KEY,
    placement_timestamp TIMESTAMP,
    location TEXT,
    material TEXT
);
