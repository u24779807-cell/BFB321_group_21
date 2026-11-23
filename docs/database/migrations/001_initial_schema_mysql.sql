-- MySQL 8.0 schema. For local development, app.py creates an equivalent SQLite DB.
CREATE DATABASE IF NOT EXISTS smart_spaza CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE smart_spaza;

CREATE TABLE IF NOT EXISTS users (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(80) NOT NULL,
  surname VARCHAR(80) NOT NULL,
  email VARCHAR(190) NOT NULL UNIQUE,
  phone_number VARCHAR(30) NOT NULL DEFAULT '',
  username VARCHAR(80) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS products (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  quantity INT UNSIGNED NOT NULL,
  expiry_date DATE NOT NULL,
  annual_demand DECIMAL(12,2) NOT NULL,
  ordering_cost DECIMAL(12,2) NOT NULL,
  holding_cost DECIMAL(12,2) NOT NULL,
  avg_daily_demand DECIMAL(12,2) NOT NULL,
  lead_time DECIMAL(10,2) NOT NULL,
  demand_std_dev DECIMAL(10,2) NOT NULL,
  category ENUM('A','B') NOT NULL,
  flagged BOOLEAN NOT NULL DEFAULT FALSE,
  flag_reason VARCHAR(100) NOT NULL DEFAULT '',
  removed BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_products_category (category),
  INDEX idx_products_expiry (expiry_date),
  INDEX idx_products_removed (removed)
) ENGINE=InnoDB;
