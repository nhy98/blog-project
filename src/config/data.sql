-- MySQL dump 10.13  Distrib 8.0.26, for Linux (x86_64)
--
-- Host: 10.0.6.86    Database: test_yen
-- ------------------------------------------------------
-- Server version	5.5.5-10.3.31-MariaDB-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Interaction`
--

DROP TABLE IF EXISTS `Interaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Interaction` (
  `InterId` char(36) NOT NULL,
  `UserId` char(36) NOT NULL,
  `PostId` char(36) NOT NULL,
  `CreatedDate` datetime DEFAULT NULL,
  `IsDeleted` int(1) unsigned zerofill NOT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  PRIMARY KEY (`InterId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Interaction`
--

LOCK TABLES `Interaction` WRITE;
/*!40000 ALTER TABLE `Interaction` DISABLE KEYS */;
INSERT INTO `Interaction` VALUES ('39ca64d6-54ea-4189-adcf-c93433b6e8d6','49eac823-bd3a-42af-a23b-4d4f85bd7927','456ba837-2078-416f-b250-18eafc4d0c97','2021-08-14 04:02:47',0,'2021-08-14 04:02:47'),('d60b3ba5-d6c7-4d1f-ad92-ce11677cd4e2','0b913804-f2aa-4744-b5b1-f7bcdd182a11','cc630bbc-aecd-444f-ae54-eb05f993dc33','2021-08-13 18:10:39',1,'2021-08-13 18:10:39');
/*!40000 ALTER TABLE `Interaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Post`
--

DROP TABLE IF EXISTS `Post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Post` (
  `PostId` char(36) NOT NULL,
  `Title` varchar(50) NOT NULL,
  `Content` longtext NOT NULL,
  `UserId` char(36) NOT NULL,
  `CreatedDate` datetime DEFAULT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  PRIMARY KEY (`PostId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Post`
--

LOCK TABLES `Post` WRITE;
/*!40000 ALTER TABLE `Post` DISABLE KEYS */;
INSERT INTO `Post` VALUES ('456ba837-2078-416f-b250-18eafc4d0c97','Title1','ahihihihihihihi','49eac823-bd3a-42af-a23b-4d4f85bd7927','2021-08-14 04:00:19','2021-08-14 04:00:19'),('cc630bbc-aecd-444f-ae54-eb05f993dc33','Yen xinh gai','Yen xinh gai that day hihi. chinh sua lan 1','0b913804-f2aa-4744-b5b1-f7bcdd182a11','2021-08-13 17:42:33','2021-08-13 17:43:55');
/*!40000 ALTER TABLE `Post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User` (
  `UserId` char(36) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Mobile` varchar(20) DEFAULT NULL,
  `Occupation` varchar(50) DEFAULT NULL,
  `AccountType` int(11) DEFAULT NULL,
  `CreatedDate` datetime DEFAULT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  `FbUserId` varchar(20) DEFAULT NULL,
  `Role` int(11) DEFAULT NULL,
  PRIMARY KEY (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES ('0b913804-f2aa-4744-b5b1-f7bcdd182a11','nhyyy.98@gmail.com','Yen Nguyen Hai','0374920522','Student',2,'2021-08-13 15:51:08','2021-08-13 16:57:34',NULL,2),('49eac823-bd3a-42af-a23b-4d4f85bd7927','taxldldpza_1628913022@tfbnw.net','Mary Algafjfhkgeh Qinsen','0123456789','Employee',1,'2021-08-14 03:52:40','2021-08-14 03:59:27','103392085391018',2),('5c171875-cb32-4d7c-8a22-d9e943f44db7','kelroyal9x@gmail.com','Yến NH',NULL,NULL,2,'2021-08-13 17:00:28','2021-08-13 17:22:25','2889814037936535',1);
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-08-15 17:37:06
