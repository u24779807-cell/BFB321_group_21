-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: smart_spaza_shop
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `quantity` int NOT NULL DEFAULT '0',
  `expiry_date` date NOT NULL,
  `annual_demand` decimal(10,0) NOT NULL,
  `ordering_cost` decimal(10,0) NOT NULL,
  `holding_cost` decimal(10,0) NOT NULL,
  `avg_daily_demand` decimal(10,0) NOT NULL,
  `lead_time` int NOT NULL,
  `demand_std_dev` decimal(10,0) NOT NULL,
  `category` varchar(10) NOT NULL,
  `flagged` tinyint(1) NOT NULL DEFAULT '0',
  `flag_reason` varchar(255) DEFAULT NULL,
  `removed` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`product_id`),
  KEY `idx_products_user` (`user_id`),
  KEY `idx_products_expiry` (`expiry_date`),
  CONSTRAINT `fk_products_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `chk_annual_demand` CHECK ((`annual_demand` > 0)),
  CONSTRAINT `chk_avg_daily_demand` CHECK ((`avg_daily_demand` >= 0)),
  CONSTRAINT `chk_category` CHECK ((`category` in (_utf8mb4'A',_utf8mb4'B',_utf8mb4'C'))),
  CONSTRAINT `chk_demand_std_dev` CHECK ((`demand_std_dev` >= 0)),
  CONSTRAINT `chk_holding_cost` CHECK ((`holding_cost` > 0)),
  CONSTRAINT `chk_lead_time` CHECK ((`lead_time` >= 0)),
  CONSTRAINT `chk_ordering_cost` CHECK ((`ordering_cost` > 0)),
  CONSTRAINT `chk_quantity` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,1,'Milk',30,'2026-12-10',1200,45,5,4,2,1,'A',0,NULL,0,'2026-11-22 22:32:06','2026-11-22 22:32:06'),(2,1,'Bread',20,'2026-11-26',900,30,3,3,1,1,'A',0,NULL,0,'2026-11-22 22:32:06','2026-11-22 22:32:06'),(3,1,'Flour',50,'2027-03-15',600,35,4,2,3,1,'B',0,NULL,0,'2026-11-22 22:32:06','2026-11-22 22:32:06'),(4,2,'Iwisa Maize meal',550,'2027-10-26',1000,200,50,10,5,0,'A',0,NULL,0,'2026-11-23 13:58:35','2026-11-23 13:58:35'),(5,2,'beans',750,'2026-12-15',100,20,10,16,1,1,'B',0,NULL,0,'2026-11-23 15:06:00','2026-11-23 15:06:00');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock_movements`
--

DROP TABLE IF EXISTS `stock_movements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stock_movements` (
  `movement_id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `movement_type` enum('IN','OUT','ADJUSTMENT') NOT NULL,
  `quantity_changed` int NOT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `movement_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`movement_id`),
  KEY `idx_movements_product` (`product_id`),
  KEY `idx_movements_date` (`movement_date`),
  CONSTRAINT `fk_movements_products` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`),
  CONSTRAINT `chk_movement_quantity` CHECK ((`quantity_changed` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock_movements`
--

LOCK TABLES `stock_movements` WRITE;
/*!40000 ALTER TABLE `stock_movements` DISABLE KEYS */;
INSERT INTO `stock_movements` VALUES (1,1,'IN',30,'Initial stock received','2026-11-23 00:32:06','2026-11-22 22:32:06'),(2,2,'IN',20,'Initial stock received','2026-11-23 00:32:07','2026-11-22 22:32:07'),(3,3,'IN',50,'Initial stock received','2026-11-23 00:32:07','2026-11-22 22:32:07');
/*!40000 ALTER TABLE `stock_movements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `surname` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Nwayitelo','Sethole','lightsethole@gmail.com','0792487487','NwayiSR_services','SEED_ONLY_NOT_A_LOGIN_PASSWORD','2026-11-22 22:32:06'),(2,'Testing','test','user@gmail.com','0715605665','test@1','scrypt:32768:8:1$XxYkHjXansGuFavz$99eb26a8e0640ae266bf2d7cf1ae0f52ab17c0b790ca6ed1631e5ca3c89023f1c9837c1e86d904a86c9ef2567711d19ce3868c8b5e4afac456e71539d648b8b4','2026-11-23 10:39:04');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-23 21:00:32
