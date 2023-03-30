--
-- Table structure for table `houselist`
--

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

DROP TABLE IF EXISTS `houselist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `houselist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(255) NOT NULL DEFAULT '',
  `nickname` varchar(255) NOT NULL DEFAULT '',
  `lastname` varchar(255) NOT NULL DEFAULT '',
  `rotation` tinyint(1) NOT NULL DEFAULT '0',
  `is_admin` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `year` enum('Fr','So','Jr','Sr','SS','RA','Staff','') NOT NULL DEFAULT 'Fr',
  `major` varchar(32) NOT NULL DEFAULT '',
  `address` varchar(50) NOT NULL DEFAULT '',
  `cellphone` varchar(16) NOT NULL DEFAULT '',
  `email` varchar(32) NOT NULL DEFAULT '',
  `membership` enum('s','f','n') NOT NULL DEFAULT 's',
  `native` int(11) DEFAULT '0',
  `birthday` date NOT NULL,
  `gender` enum('m','f','n') NOT NULL DEFAULT 'n',
  `beach` tinyint(1) NOT NULL DEFAULT '0',
  `nomail` tinyint(1) NOT NULL DEFAULT '0',
  `all` tinyint(1) NOT NULL DEFAULT '1',
  `lloydspam` tinyint(1) NOT NULL DEFAULT '1',
  `spam` tinyint(1) NOT NULL DEFAULT '1',
  `nospam` tinyint(1) NOT NULL DEFAULT '1',
  `pastandpresent` tinyint(1) NOT NULL DEFAULT '1',
  `summer` tinyint(1) NOT NULL DEFAULT '0',
  `shirtsize` enum('xs','s','m','l','xl','xxl','xxxl') DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `temp_pass` varchar(255) NOT NULL DEFAULT 'wow',
  `password` varchar(255) DEFAULT '$2b$12$Piw9TTsH9YYbzvt4I1Y39ue/Mdk48dAaJ/nc5qmBznN18DxaUXzGG',
  `bottom5` int(11) DEFAULT NULL,
  `nosucks` int(11) DEFAULT NULL,
  `top5` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=566 DEFAULT CHARSET=latin1 COMMENT='Lloyd House current full- and social-members database';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `houselist`
--

LOCK TABLES `houselist` WRITE;
/*!40000 ALTER TABLE `houselist` DISABLE KEYS */;
INSERT INTO `houselist` VALUES 
    (0,'Lloyd','','Secretary',1,1,'RA','shiet','','','secretary@lloyd.caltech.edu','f',1,'2002-01-21','m',1,0,1,1,1,0,1,1,NULL,'secretary','wow','$2b$12$Piw9TTsH9YYbzvt4I1Y39ue/Mdk48dAaJ/nc5qmBznN18DxaUXzGG',0,1,0),
    (1,'Lloyd','','President',0,1,'RA','','','','president@lloyd.caltech.edu','f',1,'2002-01-21','m',1,0,1,1,1,0,1,1,NULL,'president','wow','$2b$12$Piw9TTsH9YYbzvt4I1Y39ue/Mdk48dAaJ/nc5qmBznN18DxaUXzGG',0,1,0),
    (10,'Jacob','','Morrier',0,0,'RA','','','','jmorrier@caltech.edu','f',1,'0000-00-00','m',1,0,1,1,1,1,1,1,NULL,'ra','wow','$2b$12$Piw9TTsH9YYbzvt4I1Y39ue/Mdk48dAaJ/nc5qmBznN18DxaUXzGG',0,1,0),
    (100,'Gaurav','','Phanse',0,0,'Sr','MechE','207','111-222-3333','gphanse@caltech.edu','f',1,'2001-01-21','m',1,0,1,1,1,1,0,0,'s','gauravphanse','wow','$2b$12$Piw9TTsH9YYbzvt4I1Y39ue/Mdk48dAaJ/nc5qmBznN18DxaUXzGG',0,1,0),
    (200,'Eric','','Amaro',0,0,'Sr','Computer Science','','111222333','eamaro@caltech.edu','f',1,'2001-01-21','m',1,0,1,1,1,1,0,0,'m','ericamaro','wow','$2b$12$Piw9TTsH9YYbzvt4I1Y39ue/Mdk48dAaJ/nc5qmBznN18DxaUXzGG',0,1,0),
    (201,'Joseph','Joe','Cachaldora',0,0,'Sr','Computer Science','','111222333','jcachald@caltech.edu','s',1,'2001-01-21','m',1,0,1,1,1,1,0,0,'m','josephcachaldora','wow','$2b$12$Piw9TTsH9YYbzvt4I1Y39ue/Mdk48dAaJ/nc5qmBznN18DxaUXzGG',0,1,0),
    (300,'Pranav','','Patil',0,0,'Jr','Computer Science','','111222333','ppatil@caltech.edu','f',1,'2002-01-21','m',1,0,1,1,1,1,0,0,'m','pranavpatil','wow','$2b$12$Piw9TTsH9YYbzvt4I1Y39ue/Mdk48dAaJ/nc5qmBznN18DxaUXzGG',0,1,0),
    (302,'Rajeev','','Datta',0,0,'Jr','Computer Science','','111222333','rdatta@caltech.edu','s',1,'2002-01-21','m',1,0,1,1,1,1,0,0,'m','rajeevdatta','wow','$2b$12$Piw9TTsH9YYbzvt4I1Y39ue/Mdk48dAaJ/nc5qmBznN18DxaUXzGG',0,1,0),
    (401,'Isabella','Izzy','Zuniga',0,0,'So','Mech E','','111222333','izuniga@caltech.edu','f',1,'2003-01-21','f',1,0,1,1,1,1,0,0,'m','isabellazuniga','wow','$2b$12$Piw9TTsH9YYbzvt4I1Y39ue/Mdk48dAaJ/nc5qmBznN18DxaUXzGG',0,1,0),
    (402,'Nisha','','Balaji',0,0,'So','Computer Science','','111222333','nbalaji@caltech.edu','f',1,'2003-01-21','f',1,0,1,1,1,1,0,0,'s','nishabalaji','wow','$2b$12$Piw9TTsH9YYbzvt4I1Y39ue/Mdk48dAaJ/nc5qmBznN18DxaUXzGG',0,1,0),
    (500,'Bryan','','Oliveira',0,0,'Fr','Computer Science','','111222333','boliveir@caltech.edu','f',1,'2003-01-21','m',1,0,1,1,1,1,0,0,'m','bryanoliveira','wow','$2b$12$Piw9TTsH9YYbzvt4I1Y39ue/Mdk48dAaJ/nc5qmBznN18DxaUXzGG',0,1,0),
    (502,'Arnauld','','Martinez',0,0,'Fr','Computer Science','','111222333','arnauldmartinez@caltech.edu','f',1,'2003-01-21','m',1,0,1,1,1,1,0,0,'m','arnauldmartinez','wow','$2b$12$Piw9TTsH9YYbzvt4I1Y39ue/Mdk48dAaJ/nc5qmBznN18DxaUXzGG',0,1,0);

/*!40000 ALTER TABLE `houselist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-13  2:06:59

CREATE TABLE qna (
    question_id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    embedding TEXT,
    tokens INT
);

INSERT INTO qna (question, answer) VALUES 
    ("When are quiet hours?", "Quiet hours are after 2AM on Fridays and Saturdays and after midnight otherwise. It's okay to ask your neighbors or people in the hall to be quiet during quiet hours! You can also talk to your LASR and they can take care of it for you."),
    ("How does someone become a social Lloydie?", "You will need to attend a house dinner (where you should be invited by a current Lloydie). There, they will announce you and you need to say you are running for a social. Then, you need to fill out the membership application and will be added to the next member elections. A quorum is needed of one-third of the house, so be sure to convince people to vote!"),
    ("How do I drop my full membership to a social?", "Talk to the secretary (messenger or email secretary@lloyd.caltech.edu). There is no process needed to downgrade a membership, but be aware that to get a membership back, you need to go through member elections again.");