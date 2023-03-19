-- MySQL dump 10.13  Distrib 5.5.62, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: rotation
-- ------------------------------------------------------
-- Server version       5.5.62-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `frosh_id` int(11) NOT NULL,
  `comment` longtext,
  `timestamp` datetime DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=434 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (433,0,21,'jksfjkadngkjsbsf',NULL,NULL);
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;
--
-- Table structure for table `prefrosh`
--

DROP TABLE IF EXISTS `prefrosh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prefrosh` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `lastname` varchar(255) DEFAULT NULL,
  `firstname` varchar(255) DEFAULT NULL,
  `dinner_id` int(11) DEFAULT NULL,
  `photo_url` varchar(255) DEFAULT NULL,
  `assignment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=246 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prefrosh`
--

LOCK TABLES `prefrosh` WRITE;
/*!40000 ALTER TABLE `prefrosh` DISABLE KEYS */;
INSERT INTO `prefrosh` VALUES 
    (1,'Abraham','Tia',7,'img/frosh2022/Tia Abraham.jpg',NULL),
    (2,'Abramson','Cecilia',7,'img/frosh2022/Cecilia Abramson.jpg',NULL),
    (3,'Adams','Sophia',7,'img/frosh2022/Sophia Adams.jpg',NULL),
    (4,'Ahmad','Ali',0,'img/frosh2022/Ali Ahmad.jpg',NULL),
    (5,'Alderete','Jacob',1,'img/frosh2022/Jacob Alderete.jpg',NULL),
    (6,'Alsup','Jena',2,'img/frosh2022/Jena Alsup.jpg',NULL),
    (7,'Alvidrez','Luke',4,'img/frosh2022/Luke Alvidrez.jpg',NULL),
    (8,'Ammawat','Parthorn',0,'img/frosh2022/Parthorn Ammawat.jpg',NULL),
    (9,'Anand','Dharshini',2,'img/frosh2022/Dharshini Anand.jpg',NULL),
    (10,'Anand','Yuvan',3,'img/frosh2022/Yuvan Anand.jpg',NULL),
    (11,'Arbab','Mohammad',2,'img/frosh2022/Mohammad Arbab.jpg',NULL),
    (12,'Arechavala','Mars',5,'img/frosh2022/Mars Arechavala.jpg',NULL),
    (13,'Argandona Vite','Ivan',1,'img/frosh2022/Ivan Argandona Vite.jpg',NULL),
    (14,'Ashby','Alexis',3,'img/frosh2022/Alexis Ashby.jpg',NULL),
    (15,'Atkinson','Miles',0,'img/frosh2022/Maia Atkinson.jpg',NULL),
    (16,'Bachu','Graciela',4,'img/frosh2022/Graciela Bachu.jpg',NULL),
    (17,'Balaji','Aadarsh',7,'img/frosh2022/Aadarsh Balaji.jpg',NULL),
    (18,'Banik','Meher',3,'img/frosh2022/Meher Banik.jpg',NULL),
    (19,'Banuelos ','Sebastian',1,'img/frosh2022/Sebastian Banuelos.jpg',NULL);

/*!40000 ALTER TABLE `prefrosh` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-13  2:15:46
