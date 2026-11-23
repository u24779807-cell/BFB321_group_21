
-- Smart Spaza Food Network
-- Database reset script

-- WARNING: This deletes all existing project data.
DROP DATABASE IF EXISTS smart_spaza_shop;

-- Recreate the database
CREATE DATABASE smart_spaza_shop;

USE smart_spaza_shop;

-- Recreate all database tables
SOURCE schema.sql;

-- Insert sample data
SOURCE seed.sql;
