-- ESTATEWISE INTELLIGENCE DATABASE SCHEMA
-- RUN THIS IN MYSQL WORKBENCH TO INITIALIZE SYSTEM

CREATE DATABASE IF NOT EXISTS estatewise_db;
USE estatewise_db;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. Predictions Table
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    bedrooms INT,
    bathrooms INT,
    floor_area DECIMAL(10,2),
    land_size DECIMAL(10,2),
    subdivision VARCHAR(100),
    build_year INT,
    predicted_price DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 3. Initial Administrative Node
INSERT IGNORE INTO users (username, password, role) 
VALUES ('admin', 'admin123', 'admin');
