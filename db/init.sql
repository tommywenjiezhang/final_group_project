create database calculatorApp;
use calculatorApp;

DROP TABLE IF EXISTS `User`;

CREATE TABLE `User` (
  `UserID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(25) DEFAULT NULL,
  `username` varchar(90) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `phone` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`UserID`)
);

CREATE TABLE `Dataset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NOT NULL,
  `title` varchar(30),
  `description` varchar(255),
  `user_id` int(11) not null,
  PRIMARY KEY(`id`),
  FOREIGN KEY (`user_id`) REFERENCES User(`UserID`)
);


INSERT INTO `User` VALUES (1,'Tommy Zhang','tommyzhang','Love28200828','tommywenjiezhang@gmail.com',8482478883);