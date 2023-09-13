CREATE DATABASE if not exists ecom_data;
use ecom_data;
DROP TABLE if exists station_data_new;
CREATE TABLE if not exists station_data (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `fecha` date DEFAULT NULL,
 `hora` time DEFAULT NULL,
 `timestamp` INT NOT NULL DEFAULT 0,
 `uploaded` INT NOT NULL DEFAULT 0,
 `tipo` TEXT,
 `microdatos` TEXT,
 PRIMARY KEY (`id`)
);