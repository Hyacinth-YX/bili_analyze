/*
 Navicat Premium Data Transfer

 Source Server         : dockerhost
 Source Server Type    : MySQL
 Source Server Version : 80019
 Source Host           : localhost:8306
 Source Schema         : bilibili

 Target Server Type    : MySQL
 Target Server Version : 80019
 File Encoding         : 65001

 Date: 04/06/2020 00:26:39
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for aid_hotword
-- ----------------------------
DROP TABLE IF EXISTS `aid_hotword`;
CREATE TABLE `aid_hotword` (
  `aid` int NOT NULL,
  `hotword` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`aid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for aid_tag
-- ----------------------------
DROP TABLE IF EXISTS `aid_tag`;
CREATE TABLE `aid_tag` (
  `aid` int NOT NULL,
  `tagname` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`aid`,`tagname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for follower
-- ----------------------------
DROP TABLE IF EXISTS `follower`;
CREATE TABLE `follower` (
  `time` timestamp NOT NULL,
  `uid` int NOT NULL,
  `follower_num` int DEFAULT NULL,
  PRIMARY KEY (`time`,`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for hotword
-- ----------------------------
DROP TABLE IF EXISTS `hotword`;
CREATE TABLE `hotword` (
  `time` timestamp NOT NULL,
  `rank` int NOT NULL,
  `hotword` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`time`,`rank`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for ip_table
-- ----------------------------
DROP TABLE IF EXISTS `ip_table`;
CREATE TABLE `ip_table` (
  `ip_addr` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip_port` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `server_addr` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `anonymous` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `http_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `speed` decimal(5,3) DEFAULT NULL,
  `conn_time` decimal(5,3) DEFAULT NULL,
  `alive_time` decimal(11,1) DEFAULT NULL,
  `validate_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`ip_addr`,`ip_port`,`http_type`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for userinfo
-- ----------------------------
DROP TABLE IF EXISTS `userinfo`;
CREATE TABLE `userinfo` (
  `uid` int NOT NULL,
  `uname` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for vinfo
-- ----------------------------
DROP TABLE IF EXISTS `vinfo`;
CREATE TABLE `vinfo` (
  `aid` int NOT NULL,
  `bvid` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `uid` int DEFAULT NULL,
  `vname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `area` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cre_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`aid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for vresult
-- ----------------------------
DROP TABLE IF EXISTS `vresult`;
CREATE TABLE `vresult` (
  `timestamp` timestamp NOT NULL,
  `aid` int NOT NULL,
  `view` int DEFAULT NULL,
  `reply` int DEFAULT NULL,
  `coin` int DEFAULT NULL,
  `like` int DEFAULT NULL,
  `dislike` int DEFAULT NULL,
  `favorite` int DEFAULT NULL,
  `danmaku` int DEFAULT NULL,
  PRIMARY KEY (`timestamp`,`aid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
