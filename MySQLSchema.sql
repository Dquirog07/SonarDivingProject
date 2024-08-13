
CREATE TABLE IF NOT EXISTS divers (
    diver_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    profile_data JSON
);


CREATE TABLE IF NOT EXISTS dives (
    dive_id INT AUTO_INCREMENT PRIMARY KEY,
    diver_id INT NOT NULL,
    start_timestamp DATETIME,
    end_timestamp DATETIME,
    status ENUM('Active', 'Inactive', 'Completed')
    FOREIGN KEY (diver_id) REFERENCES divers(diver_id)
);

