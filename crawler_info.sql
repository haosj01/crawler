/*
 Navicat Premium Data Transfer

 Source Server         : 测试环境
 Source Server Type    : MySQL
 Source Server Version : 50650
 Source Host           : 192.168.110.11:3306
 Source Schema         : crawler_info

 Target Server Type    : MySQL
 Target Server Version : 50650
 File Encoding         : 65001

 Date: 18/12/2020 10:41:21
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for crawler_golden
-- ----------------------------
DROP TABLE IF EXISTS `crawler_golden`;
CREATE TABLE `crawler_golden`  (
  `id` bigint(10) NOT NULL AUTO_INCREMENT,
  `live_id` bigint(20) NOT NULL,
  `tittle` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `live_time` datetime(0) NOT NULL,
  `create_time` datetime(0) NOT NULL,
  `live_date` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `is_choice` int(2) NOT NULL DEFAULT 0,
  `is_data` int(2) NOT NULL DEFAULT 0,
  `is_notice` int(2) NOT NULL DEFAULT 0,
  `up_counts` int(8) NOT NULL DEFAULT 0,
  `down_counts` int(8) NOT NULL DEFAULT 0,
  `type` varchar(8) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `live_id`(`live_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for coin_type
-- ----------------------------
DROP TABLE IF EXISTS `coin_type`;
CREATE TABLE `coin_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Compact;

-- ----------------------------
-- Records of coin_type
-- ----------------------------
INSERT INTO `coin_type` VALUES (1, 'btc');
INSERT INTO `coin_type` VALUES (2, 'eth');
INSERT INTO `coin_type` VALUES (3, 'ltc');
INSERT INTO `coin_type` VALUES (4, 'dot');
INSERT INTO `coin_type` VALUES (5, 'link');
INSERT INTO `coin_type` VALUES (6, 'usdt');
INSERT INTO `coin_type` VALUES (7, 'bchabc');
INSERT INTO `coin_type` VALUES (8, 'xwc');

SET FOREIGN_KEY_CHECKS = 1;

-- ----------------------------
-- Table structure for crawler_coindesk
-- ----------------------------
DROP TABLE IF EXISTS `crawler_coindesk`;
CREATE TABLE `crawler_coindesk`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idxno` bigint(20) NOT NULL,
  `tittle` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `news_time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `create_time` datetime(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idxno`(`idxno`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 93 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;


