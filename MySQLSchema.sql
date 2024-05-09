
CREATE TABLE IF NOT EXISTS divers (
    diver_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    certification_number VARCHAR(100),
    experience_level VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS dives (
    dive_id INT AUTO_INCREMENT PRIMARY KEY,
    diver_id INT NOT NULL,
    start_timestamp DATETIME,
    end_timestamp DATETIME,
    start_location VARCHAR(255),
    end_location VARCHAR(255),
    FOREIGN KEY (diver_id) REFERENCES divers(diver_id)
);


CREATE TABLE IF NOT EXISTS events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    dive_id INT NOT NULL,
    event_timestamp DATETIME,
    event_type ENUM('start', 'cookie_placement', 'exit_detection'),
    location VARCHAR(255),
    details TEXT,
    FOREIGN KEY (dive_id) REFERENCES dives(dive_id)
);


CREATE TABLE IF NOT EXISTS cookies (
    cookie_id INT AUTO_INCREMENT PRIMARY KEY,
    dive_id INT NOT NULL,
    placement_timestamp DATETIME,
    location VARCHAR(255),
    material TEXT,
    FOREIGN KEY (dive_id) REFERENCES dives(dive_id)
);
