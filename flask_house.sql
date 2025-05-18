/*
 Navicat Premium Dump SQL

 Source Server         : lqy0584
 Source Server Type    : MySQL
 Source Server Version : 90200 (9.2.0)
 Source Host           : localhost:3306
 Source Schema         : flask_house

 Target Server Type    : MySQL
 Target Server Version : 90200 (9.2.0)
 File Encoding         : 65001

 Date: 18/05/2025 21:37:38
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`version_num`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
BEGIN;
INSERT INTO `alembic_version` (`version_num`) VALUES ('c360c19f3209');
COMMIT;

-- ----------------------------
-- Table structure for appointment
-- ----------------------------
DROP TABLE IF EXISTS `appointment`;
CREATE TABLE `appointment` (
  `appointment_id` int NOT NULL AUTO_INCREMENT COMMENT '预约ID',
  `house_id` int NOT NULL COMMENT '房屋ID',
  `house_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '房屋名称',
  `tenant_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '租客用户名',
  `landlord_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '房东用户名',
  `appointment_time` datetime NOT NULL COMMENT '预约时间',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '申请中' COMMENT '预约状态（申请中/已同意/已拒绝）',
  PRIMARY KEY (`appointment_id`) USING BTREE,
  KEY `house_id` (`house_id`) USING BTREE,
  KEY `tenant_name` (`tenant_name`) USING BTREE,
  KEY `landlord_name` (`landlord_name`) USING BTREE,
  CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`landlord_name`) REFERENCES `landlord` (`landlord_name`) ON DELETE CASCADE,
  CONSTRAINT `appointment_ibfk_2` FOREIGN KEY (`tenant_name`) REFERENCES `tenant` (`tenant_name`) ON DELETE CASCADE,
  CONSTRAINT `appointment_ibfk_3` FOREIGN KEY (`house_id`) REFERENCES `house_info` (`house_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of appointment
-- ----------------------------
BEGIN;
INSERT INTO `appointment` (`appointment_id`, `house_id`, `house_name`, `tenant_name`, `landlord_name`, `appointment_time`, `status`) VALUES (1, 5, '海淀区三居室', 'qwe', 'landlord', '2025-05-24 14:52:00', '已拒绝');
INSERT INTO `appointment` (`appointment_id`, `house_id`, `house_name`, `tenant_name`, `landlord_name`, `appointment_time`, `status`) VALUES (2, 7, '丰台区一居室', 'qwe', 'landlord', '2025-05-16 23:44:00', '申请中');
COMMIT;

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `comment_id` int NOT NULL AUTO_INCREMENT,
  `house_id` int NOT NULL COMMENT '房屋的id',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '留言人名字',
  `type` int NOT NULL COMMENT '留言人类型,1:租客，2:房东',
  `desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '留言内容',
  `at` int DEFAULT NULL COMMENT '@哪条留言，前端显示为@谁，选填',
  `time` datetime NOT NULL COMMENT '留言时间',
  PRIMARY KEY (`comment_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=151 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of comment
-- ----------------------------
BEGIN;
INSERT INTO `comment` (`comment_id`, `house_id`, `username`, `type`, `desc`, `at`, `time`) VALUES (39, 8, '租客7', 1, '这是第7条留言，房东landlord3你好！', NULL, '2025-04-20 17:39:14');
INSERT INTO `comment` (`comment_id`, `house_id`, `username`, `type`, `desc`, `at`, `time`) VALUES (40, 8, '租客8', 1, '这是第8条留言，房东landlord3你好！', NULL, '2025-04-19 17:39:14');
INSERT INTO `comment` (`comment_id`, `house_id`, `username`, `type`, `desc`, `at`, `time`) VALUES (41, 8, '租客9', 1, '这是第9条留言，房东landlord3你好！', NULL, '2025-04-18 17:39:14');
INSERT INTO `comment` (`comment_id`, `house_id`, `username`, `type`, `desc`, `at`, `time`) VALUES (42, 8, '租客10', 1, '这是第10条留言，房东landlord3你好！', NULL, '2025-04-17 17:39:14');
INSERT INTO `comment` (`comment_id`, `house_id`, `username`, `type`, `desc`, `at`, `time`) VALUES (43, 7, '租客1', 1, '这是第1条留言，房东landlord你好！', NULL, '2025-04-26 17:39:14');
INSERT INTO `comment` (`comment_id`, `house_id`, `username`, `type`, `desc`, `at`, `time`) VALUES (44, 7, '租客2', 1, '这是第2条留言，房东landlord你好！', NULL, '2025-04-25 17:39:14');
INSERT INTO `comment` (`comment_id`, `house_id`, `username`, `type`, `desc`, `at`, `time`) VALUES (45, 7, '租客3', 1, '这是第3条留言，房东landlord你好！', NULL, '2025-04-24 17:39:14');
INSERT INTO `comment` (`comment_id`, `house_id`, `username`, `type`, `desc`, `at`, `time`) VALUES (46, 7, '租客4', 1, '这是第4条留言，房东landlord你好！', NULL, '2025-04-23 17:39:14');
INSERT INTO `comment` (`comment_id`, `house_id`, `username`, `type`, `desc`, `at`, `time`) VALUES (47, 7, '租客5', 1, '这是第5条留言，房东landlord你好！', NULL, '2025-04-22 17:39:14');
INSERT INTO `comment` (`comment_id`, `house_id`, `username`, `type`, `desc`, `at`, `time`) VALUES (48, 7, '租客6', 1, '这是第6条留言，房东landlord你好！', NULL, '2025-04-21 17:39:14');
INSERT INTO `comment` (`comment_id`, `house_id`, `username`, `type`, `desc`, `at`, `time`) VALUES (149, 5, 'qwe', 1, 'hhh', NULL, '2025-05-07 10:21:33');
INSERT INTO `comment` (`comment_id`, `house_id`, `username`, `type`, `desc`, `at`, `time`) VALUES (150, 5, 'qwe', 1, 'yes', 149, '2025-05-07 10:21:39');
COMMIT;

-- ----------------------------
-- Table structure for complaint
-- ----------------------------
DROP TABLE IF EXISTS `complaint`;
CREATE TABLE `complaint` (
  `complaint_id` int NOT NULL AUTO_INCREMENT COMMENT '投诉/消息ID',
  `sender` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '发送人用户名（租客/房东/管理员）',
  `receiver` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '接收人用户名（为空表示所有管理员可见）',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '消息/投诉内容',
  `time` datetime NOT NULL COMMENT '发送时间',
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '类型：投诉/反馈',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '处理状态：待处理/处理中/已解决/已关闭',
  `handler_username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '处理人用户名',
  `last_updated_time` datetime NOT NULL COMMENT '最后更新时间',
  `update_seen_by_sender` tinyint(1) NOT NULL COMMENT '发送者是否已查看最新状态更新',
  PRIMARY KEY (`complaint_id`) USING BTREE,
  KEY `handler_username` (`handler_username`) USING BTREE,
  CONSTRAINT `complaint_ibfk_1` FOREIGN KEY (`handler_username`) REFERENCES `login` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of complaint
-- ----------------------------
BEGIN;
INSERT INTO `complaint` (`complaint_id`, `sender`, `receiver`, `content`, `time`, `type`, `status`, `handler_username`, `last_updated_time`, `update_seen_by_sender`) VALUES (3, 'qwe', NULL, 'dfg', '2025-05-07 02:21:56', '投诉', '处理中', 'admin', '2025-05-07 02:43:12', 1);
INSERT INTO `complaint` (`complaint_id`, `sender`, `receiver`, `content`, `time`, `type`, `status`, `handler_username`, `last_updated_time`, `update_seen_by_sender`) VALUES (4, 'qwe', 'landlord', 'sss', '2025-05-07 02:46:00', '投诉', '已解决', 'admin', '2025-05-07 02:58:00', 1);
COMMIT;

-- ----------------------------
-- Table structure for daily_rent_rate
-- ----------------------------
DROP TABLE IF EXISTS `daily_rent_rate`;
CREATE TABLE `daily_rent_rate` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `date` date NOT NULL COMMENT '统计日期',
  `total_count` int NOT NULL DEFAULT '0' COMMENT '上架总数（状态为0）',
  `rented_count` int NOT NULL DEFAULT '0' COMMENT '出租数（状态为1）',
  `rent_rate` decimal(5,2) NOT NULL COMMENT '出租率百分比（如 66.67）',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `date` (`date`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of daily_rent_rate
-- ----------------------------
BEGIN;
INSERT INTO `daily_rent_rate` (`id`, `date`, `total_count`, `rented_count`, `rent_rate`) VALUES (1, '2025-05-06', 6, 1, 16.67);
INSERT INTO `daily_rent_rate` (`id`, `date`, `total_count`, `rented_count`, `rent_rate`) VALUES (2, '2025-05-07', 6, 3, 50.00);
INSERT INTO `daily_rent_rate` (`id`, `date`, `total_count`, `rented_count`, `rent_rate`) VALUES (3, '2025-05-10', 4, 3, 75.00);
INSERT INTO `daily_rent_rate` (`id`, `date`, `total_count`, `rented_count`, `rent_rate`) VALUES (4, '2025-05-11', 4, 2, 50.00);
INSERT INTO `daily_rent_rate` (`id`, `date`, `total_count`, `rented_count`, `rent_rate`) VALUES (5, '2025-05-17', 6, 6, 100.00);
COMMIT;

-- ----------------------------
-- Table structure for house_info
-- ----------------------------
DROP TABLE IF EXISTS `house_info`;
CREATE TABLE `house_info` (
  `house_id` int NOT NULL AUTO_INCREMENT COMMENT '房屋id，自增的，不用填',
  `house_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '房屋名称',
  `rooms` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '房屋户型，如3室1厅',
  `region` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '房屋地区，如北京市海淀区',
  `addr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '具体地址',
  `price` decimal(10,2) NOT NULL COMMENT '房屋价格',
  `deposit` decimal(10,2) DEFAULT NULL COMMENT '押金',
  `situation` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '房屋装修情况',
  `highlight` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '亮点（没有可以不填）',
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '房屋图片',
  PRIMARY KEY (`house_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of house_info
-- ----------------------------
BEGIN;
INSERT INTO `house_info` (`house_id`, `house_name`, `rooms`, `region`, `addr`, `price`, `deposit`, `situation`, `highlight`, `image`) VALUES (5, '海淀区三居室', '3室1厅', '北京市海淀区', '中关村大街1号', 8000.00, 16000.00, '精装修', '交通便利，学区房', 'static/images/haidian_3room.jpg');
INSERT INTO `house_info` (`house_id`, `house_name`, `rooms`, `region`, `addr`, `price`, `deposit`, `situation`, `highlight`, `image`) VALUES (6, '朝阳区两居室', '2室1厅', '北京市朝阳区', '国贸CBD', 12000.00, 24000.00, '豪华装修', '高端社区，配套齐全', 'static/images/chaoyang_2room.jpg');
INSERT INTO `house_info` (`house_id`, `house_name`, `rooms`, `region`, `addr`, `price`, `deposit`, `situation`, `highlight`, `image`) VALUES (7, '丰台区一居室', '1室1厅', '北京市丰台区', '丰台科技园', 5000.00, 10000.00, '简单装修', '价格实惠，交通便利', 'static/images/fengtai_1room.jpg');
INSERT INTO `house_info` (`house_id`, `house_name`, `rooms`, `region`, `addr`, `price`, `deposit`, `situation`, `highlight`, `image`) VALUES (8, '新房源1', '3室2厅', '北京市东城区', '东直门大街', 15000.00, 30000.00, '豪华装修', '交通便利，配套齐全', 'static/images/OIP-C (3).jpg');
INSERT INTO `house_info` (`house_id`, `house_name`, `rooms`, `region`, `addr`, `price`, `deposit`, `situation`, `highlight`, `image`) VALUES (9, '东城区豪华三居室', '3室1厅', '北京市朝阳区', '朝阳北路', 8000.00, 16000.00, '精装修', '近地铁，生活便利', 'static/images/OIP-C (3).jpg');
INSERT INTO `house_info` (`house_id`, `house_name`, `rooms`, `region`, `addr`, `price`, `deposit`, `situation`, `highlight`, `image`) VALUES (10, '海淀区豪华三居室', '3室2厅', '北京市海淀区', '中关村大街', 15000.00, 30000.00, '豪华装修', '学区房，交通便利', 'static/images/haidian_3room.jpg');
INSERT INTO `house_info` (`house_id`, `house_name`, `rooms`, `region`, `addr`, `price`, `deposit`, `situation`, `highlight`, `image`) VALUES (15, '朝阳区精装一居室', '1室1厅', '北京市朝阳区', '朝阳公园南路', 8500.00, 17000.00, '精装修', '公园旁，生活便利', 'static/images/t2.jpg');
INSERT INTO `house_info` (`house_id`, `house_name`, `rooms`, `region`, `addr`, `price`, `deposit`, `situation`, `highlight`, `image`) VALUES (16, '测试版精修郊区别野', '4室2厅', '上海市上海市朝阳区', '浦东112', 50000.00, 500000.00, '精装', '非常好，详情电话咨询', 'static/images/20250518212017_6896.jpg_wh860.jpg');
COMMIT;

-- ----------------------------
-- Table structure for house_listing_audit
-- ----------------------------
DROP TABLE IF EXISTS `house_listing_audit`;
CREATE TABLE `house_listing_audit` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '审核记录ID',
  `house_id` int NOT NULL COMMENT '房源ID',
  `house_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '房源名称',
  `landlord_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '房东名字',
  `audit_status` int NOT NULL DEFAULT '0' COMMENT '审核状态：0-审核中，1-已通过，2-已拒绝',
  `reason` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '拒绝理由',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '申请时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '回复时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `house_id` (`house_id`,`landlord_name`) USING BTREE,
  KEY `landlord_name` (`landlord_name`) USING BTREE,
  CONSTRAINT `house_listing_audit_ibfk_1` FOREIGN KEY (`landlord_name`) REFERENCES `landlord` (`landlord_name`),
  CONSTRAINT `house_listing_audit_ibfk_2` FOREIGN KEY (`house_id`, `landlord_name`) REFERENCES `house_status` (`house_id`, `landlord_name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of house_listing_audit
-- ----------------------------
BEGIN;
INSERT INTO `house_listing_audit` (`id`, `house_id`, `house_name`, `landlord_name`, `audit_status`, `reason`, `create_time`, `update_time`) VALUES (4, 7, '丰台区一居室', 'landlord', 2, '666', '2025-05-11 10:58:16', '2025-05-11 03:13:37');
INSERT INTO `house_listing_audit` (`id`, `house_id`, `house_name`, `landlord_name`, `audit_status`, `reason`, `create_time`, `update_time`) VALUES (5, 6, '朝阳区两居室', 'landlord', 1, NULL, '2025-05-11 10:58:18', '2025-05-11 02:59:34');
INSERT INTO `house_listing_audit` (`id`, `house_id`, `house_name`, `landlord_name`, `audit_status`, `reason`, `create_time`, `update_time`) VALUES (6, 5, '海淀区三居室', 'landlord', 1, NULL, '2025-05-11 10:58:19', '2025-05-11 02:59:02');
INSERT INTO `house_listing_audit` (`id`, `house_id`, `house_name`, `landlord_name`, `audit_status`, `reason`, `create_time`, `update_time`) VALUES (7, 7, '丰台区一居室', 'landlord', 1, NULL, '2025-05-11 13:10:49', '2025-05-11 05:22:59');
INSERT INTO `house_listing_audit` (`id`, `house_id`, `house_name`, `landlord_name`, `audit_status`, `reason`, `create_time`, `update_time`) VALUES (8, 7, '丰台区一居室', 'landlord', 1, NULL, '2025-05-11 17:49:16', '2025-05-11 11:38:46');
INSERT INTO `house_listing_audit` (`id`, `house_id`, `house_name`, `landlord_name`, `audit_status`, `reason`, `create_time`, `update_time`) VALUES (9, 6, '朝阳区两居室', 'landlord', 1, NULL, '2025-05-11 17:49:17', '2025-05-11 09:49:44');
INSERT INTO `house_listing_audit` (`id`, `house_id`, `house_name`, `landlord_name`, `audit_status`, `reason`, `create_time`, `update_time`) VALUES (10, 5, '海淀区三居室', 'landlord', 1, NULL, '2025-05-11 17:49:18', '2025-05-11 09:49:43');
INSERT INTO `house_listing_audit` (`id`, `house_id`, `house_name`, `landlord_name`, `audit_status`, `reason`, `create_time`, `update_time`) VALUES (11, 6, '朝阳区两居室', 'landlord', 0, NULL, '2025-05-11 19:39:42', '2025-05-11 19:39:42');
INSERT INTO `house_listing_audit` (`id`, `house_id`, `house_name`, `landlord_name`, `audit_status`, `reason`, `create_time`, `update_time`) VALUES (12, 16, '测试版精修郊区别野', '房东C', 0, NULL, '2025-05-18 21:20:22', '2025-05-18 21:20:22');
COMMIT;

-- ----------------------------
-- Table structure for house_status
-- ----------------------------
DROP TABLE IF EXISTS `house_status`;
CREATE TABLE `house_status` (
  `house_id` int NOT NULL COMMENT '有一个外键指向house_info表',
  `landlord_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` int NOT NULL COMMENT '0为空置，1为出租中，2为装修中',
  `phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '房屋联系方式',
  `update_time` datetime NOT NULL COMMENT '房屋发布时间（之后状态有变化都更新一次时间）',
  PRIMARY KEY (`house_id` DESC,`landlord_name`) USING BTREE,
  UNIQUE KEY `uq_house_landlord` (`house_id`,`landlord_name`) USING BTREE,
  KEY `house_id` (`house_id`) USING BTREE,
  CONSTRAINT `house_id` FOREIGN KEY (`house_id`) REFERENCES `house_info` (`house_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of house_status
-- ----------------------------
BEGIN;
INSERT INTO `house_status` (`house_id`, `landlord_name`, `status`, `phone`, `update_time`) VALUES (16, '房东C', 4, '12345678910', '2025-05-18 21:20:18');
INSERT INTO `house_status` (`house_id`, `landlord_name`, `status`, `phone`, `update_time`) VALUES (15, 'landlord', 0, '13800138004', '2025-05-17 21:03:21');
INSERT INTO `house_status` (`house_id`, `landlord_name`, `status`, `phone`, `update_time`) VALUES (10, '房东C', 0, '13800138002', '2025-04-18 09:35:14');
INSERT INTO `house_status` (`house_id`, `landlord_name`, `status`, `phone`, `update_time`) VALUES (9, '房东B', 0, '13800138001', '2025-04-18 09:35:14');
INSERT INTO `house_status` (`house_id`, `landlord_name`, `status`, `phone`, `update_time`) VALUES (8, 'landlord3', 0, '13800138004', '2025-05-08 10:08:54');
INSERT INTO `house_status` (`house_id`, `landlord_name`, `status`, `phone`, `update_time`) VALUES (7, 'landlord', 0, '13800138002', '2025-05-11 13:23:20');
INSERT INTO `house_status` (`house_id`, `landlord_name`, `status`, `phone`, `update_time`) VALUES (6, 'landlord', 0, '13800138001', '2025-05-17 21:03:21');
INSERT INTO `house_status` (`house_id`, `landlord_name`, `status`, `phone`, `update_time`) VALUES (5, 'landlord', 0, '13800138000', '2025-05-11 17:40:06');
COMMIT;

-- ----------------------------
-- Table structure for landlord
-- ----------------------------
DROP TABLE IF EXISTS `landlord`;
CREATE TABLE `landlord` (
  `landlord_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '房东用户名',
  `phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '联系电话，与house_status中的phone一致',
  `addr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '房东住址',
  PRIMARY KEY (`landlord_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of landlord
-- ----------------------------
BEGIN;
INSERT INTO `landlord` (`landlord_name`, `phone`, `addr`) VALUES ('landlord', '13800138000', '我家');
INSERT INTO `landlord` (`landlord_name`, `phone`, `addr`) VALUES ('landlord3', '13800138004', '北京市东城区');
INSERT INTO `landlord` (`landlord_name`, `phone`, `addr`) VALUES ('房东B', '13800138001', '北京市朝阳区');
INSERT INTO `landlord` (`landlord_name`, `phone`, `addr`) VALUES ('房东C', '13800138002', '北京市海淀区');
COMMIT;

-- ----------------------------
-- Table structure for login
-- ----------------------------
DROP TABLE IF EXISTS `login`;
CREATE TABLE `login` (
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `type` int NOT NULL COMMENT '0为管理员，1为租客，2为房东',
  PRIMARY KEY (`username`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of login
-- ----------------------------
BEGIN;
INSERT INTO `login` (`username`, `password`, `type`) VALUES ('admin', '$argon2id$v=19$m=65536,t=3,p=4$MVawFIgbHw7qY9+X3T7DOA$UB0rwVIVHJtEeG4IybsxOcgt1pbm6DslD1DxitZuKGE', 0);
INSERT INTO `login` (`username`, `password`, `type`) VALUES ('landlord', '$argon2id$v=19$m=65536,t=3,p=4$UKnk0bMwdmSdvd78YzPX5Q$qe2mnLBxrWdA5EDeK+mMijqgn0LvPa/rNMYWHYaLSqQ', 2);
INSERT INTO `login` (`username`, `password`, `type`) VALUES ('landlord3', '$argon2id$v=19$m=65536,t=3,p=4$s/J1WI0sGVI/wKpXNS/vMA$VGzc+4OcDfC6I9CI8KNTs2D4k5qYQMH8ke3jWyM4rGM', 2);
INSERT INTO `login` (`username`, `password`, `type`) VALUES ('qwe', '$argon2id$v=19$m=65536,t=3,p=4$o225dc9lcq2vp7/QRpM7Uw$cvBXz/2KmGT99o24nRUl+iT63K8mwxBR4DDElg+uJnA', 1);
INSERT INTO `login` (`username`, `password`, `type`) VALUES ('tenant', '$argon2id$v=19$m=65536,t=3,p=4$MVawFIgbHw7qY9+X3T7DOA$UB0rwVIVHJtEeG4IybsxOcgt1pbm6DslD1DxitZuKGE', 1);
INSERT INTO `login` (`username`, `password`, `type`) VALUES ('tenant2', '$argon2id$v=19$m=65536,t=3,p=4$MVawFIgbHw7qY9+X3T7DOA$UB0rwVIVHJtEeG4IybsxOcgt1pbm6DslD1DxitZuKGE', 1);
INSERT INTO `login` (`username`, `password`, `type`) VALUES ('wer', '$argon2id$v=19$m=65536,t=3,p=4$MVawFIgbHw7qY9+X3T7DOA$UB0rwVIVHJtEeG4IybsxOcgt1pbm6DslD1DxitZuKGE', 1);
INSERT INTO `login` (`username`, `password`, `type`) VALUES ('房东B', '$argon2id$v=19$m=65536,t=3,p=4$+Cw6DhNOyNt1sZea9O6P7Q$PZBQF+CCo0kg6Udpq+ZZsAT+KcIPt/t20UBfqog+5P0', 2);
INSERT INTO `login` (`username`, `password`, `type`) VALUES ('房东C', '$argon2id$v=19$m=65536,t=3,p=4$pJ4QNDbtTzm5Tvxv3ji0mQ$gt3wdbXgYertf2Pp7Rwc6nR6Q6l9nroGFNMW4QhWtvg', 2);
INSERT INTO `login` (`username`, `password`, `type`) VALUES ('租客A', '$argon2id$v=19$m=65536,t=3,p=4$MVawFIgbHw7qY9+X3T7DOA$UB0rwVIVHJtEeG4IybsxOcgt1pbm6DslD1DxitZuKGE', 1);
INSERT INTO `login` (`username`, `password`, `type`) VALUES ('租客C', '$argon2id$v=19$m=65536,t=3,p=4$MVawFIgbHw7qY9+X3T7DOA$UB0rwVIVHJtEeG4IybsxOcgt1pbm6DslD1DxitZuKGE', 1);
COMMIT;

-- ----------------------------
-- Table structure for message
-- ----------------------------
DROP TABLE IF EXISTS `message`;
CREATE TABLE `message` (
  `message_id` int NOT NULL AUTO_INCREMENT,
  `sender_username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '发送者用户名',
  `receiver_username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '接收者用户名',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '消息内容',
  `timestamp` datetime NOT NULL COMMENT '发送时间',
  `is_read` tinyint(1) NOT NULL COMMENT '是否已读 (接收者视角)',
  `channel_id` int NOT NULL COMMENT '所属私信频道的ID',
  PRIMARY KEY (`message_id`) USING BTREE,
  KEY `receiver_username` (`receiver_username`) USING BTREE,
  KEY `sender_username` (`sender_username`) USING BTREE,
  KEY `channel_id` (`channel_id`) USING BTREE,
  CONSTRAINT `message_ibfk_1` FOREIGN KEY (`receiver_username`) REFERENCES `login` (`username`),
  CONSTRAINT `message_ibfk_2` FOREIGN KEY (`sender_username`) REFERENCES `login` (`username`),
  CONSTRAINT `message_ibfk_3` FOREIGN KEY (`channel_id`) REFERENCES `private_channel` (`channel_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of message
-- ----------------------------
BEGIN;
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (1, 'qwe', 'landlord', 'ok', '2025-05-05 07:29:58', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (2, 'qwe', 'landlord', 'oka\r\n', '2025-05-05 07:35:21', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (3, 'qwe', 'landlord', 'oka\r\n', '2025-05-05 07:38:01', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (4, 'qwe', 'landlord', 's', '2025-05-05 07:53:00', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (5, 'qwe', 'landlord', '现在呢', '2025-05-05 07:53:51', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (6, 'landlord', 'qwe', '快一点', '2025-05-05 08:12:41', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (7, 'qwe', 'landlord', 'a', '2025-05-05 08:35:40', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (8, 'qwe', 'landlord', 'a', '2025-05-05 08:35:43', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (9, 'qwe', 'landlord', 'a', '2025-05-05 08:35:46', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (10, 'landlord', 'qwe', 'wai', '2025-05-05 17:02:13', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (11, 'qwe', 'landlord', '?', '2025-05-05 17:02:18', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (12, 'qwe', 'landlord', 'a', '2025-05-05 17:08:37', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (13, 'qwe', 'landlord', 'ssssss', '2025-05-05 17:09:42', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (14, 'qwe', 'landlord', 'sssss', '2025-05-05 17:10:00', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (15, 'qwe', 'landlord', 'gsdfghdngd', '2025-05-05 17:10:09', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (16, 'landlord', 'qwe', '行不行啊', '2025-05-05 17:17:28', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (17, 'landlord', 'qwe', '？？？', '2025-05-05 17:18:06', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (18, 'landlord', 'qwe', '我不知道', '2025-05-05 17:18:33', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (19, 'landlord', 'qwe', '欧克', '2025-05-05 17:18:44', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (20, 'qwe', 'landlord', 'cnkcv z,v', '2025-05-05 22:38:13', 1, 3);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (21, 'qwe', 'landlord', 'djvbjdankvkldsava', '2025-05-06 07:58:48', 1, 4);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (23, 'landlord', 'qwe', '【租房合同】租期：2025-05-01 至 2025-05-16，金额：¥0.33。请确认合同信息。', '2025-05-16 16:19:40', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (24, 'landlord', 'qwe', '【租房合同】租期：2025-05-24 至 2025-06-24，金额：¥36000.00。请确认合同信息。', '2025-05-17 02:30:47', 1, 3);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (25, 'tenant2', 'landlord', '你好', '2025-05-17 11:47:22', 1, 5);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (26, 'landlord', 'tenant2', '【租房合同】租期：2025-05-01 至 2026-03-01，金额：¥96000.00。请确认合同信息。', '2025-05-17 12:06:06', 0, 5);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (27, 'landlord', 'tenant2', '【租房合同】租期：2025-05-01 至 2025-11-01，金额：¥64000.00。请确认合同信息。', '2025-05-17 04:17:36', 0, 5);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (28, 'landlord', 'tenant2', '【租房合同】租期：2025-05-01 至 2025-11-01，金额：¥64000.00。请确认合同信息。', '2025-05-17 04:19:48', 0, 5);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (29, 'landlord', 'qwe', '【租房合同】租期：2025-05-01 至 2025-08-01，金额：¥40000.00。请确认合同信息。', '2025-05-17 04:24:06', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (30, 'landlord', 'qwe', '【租房合同】租期：2025-05-01 至 2025-08-01，金额：¥40000.00。请确认合同信息。', '2025-05-17 13:49:41', 1, 1);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (31, 'qwe', 'landlord', '可以出租吗', '2025-05-17 20:19:29', 1, 4);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (32, 'landlord', 'qwe', '【租房合同】租期：2025-05-24 至 2025-10-24，金额：¥35000.00。请确认合同信息。', '2025-05-17 20:20:00', 1, 4);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (33, 'qwe', 'landlord', 'woyao', '2025-05-17 21:04:25', 1, 6);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (34, 'landlord', 'qwe', '【租房合同】租期：2025-05-16 至 2025-06-16，金额：¥25500.00。请确认合同信息。', '2025-05-17 21:05:18', 1, 6);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (35, 'landlord', 'qwe', '【租房合同】租期：2025-05-17 至 2025-06-17，金额：¥25500.00。请确认合同信息。', '2025-05-17 21:06:05', 1, 6);
INSERT INTO `message` (`message_id`, `sender_username`, `receiver_username`, `content`, `timestamp`, `is_read`, `channel_id`) VALUES (36, 'landlord', 'qwe', '【租房合同】租期：2025-03-17 至 2025-04-17，金额：¥36000.00。请确认合同信息。', '2025-05-17 21:21:35', 1, 3);
COMMIT;

-- ----------------------------
-- Table structure for news
-- ----------------------------
DROP TABLE IF EXISTS `news`;
CREATE TABLE `news` (
  `id` int NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL COMMENT '新闻发布时间，注意新闻只能新增，(尽量)不能修改',
  `house_id` int NOT NULL COMMENT '房屋id，有一个指向house_info的外键',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '新闻标题（如某某房屋出租了）,一般配对房屋状态变化',
  `desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '新闻内容',
  `landlord_username` varchar(100) DEFAULT NULL COMMENT '新闻发布者(房东)',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `house_id` (`house_id`) USING BTREE,
  KEY `landlord_username` (`landlord_username`),
  CONSTRAINT `news_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `house_info` (`house_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `news_ibfk_2` FOREIGN KEY (`landlord_username`) REFERENCES `login` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of news
-- ----------------------------
BEGIN;
INSERT INTO `news` (`id`, `time`, `house_id`, `title`, `desc`, `landlord_username`) VALUES (1, '2025-04-17 21:08:54', 8, '东城区新房源出租', '豪华装修，交通便利，欢迎预约看房。', NULL);
INSERT INTO `news` (`id`, `time`, `house_id`, `title`, `desc`, `landlord_username`) VALUES (3, '2025-04-01 10:00:00', 6, '朝阳区精装两居室出租', '朝阳区精装两居室现已出租，欢迎预约看房。', NULL);
INSERT INTO `news` (`id`, `time`, `house_id`, `title`, `desc`, `landlord_username`) VALUES (4, '2025-04-05 15:30:00', 10, '海淀区豪华三居室降价', '海淀区豪华三居室价格下调，抓紧机会！', NULL);
INSERT INTO `news` (`id`, `time`, `house_id`, `title`, `desc`, `landlord_username`) VALUES (5, '2025-04-10 09:00:00', 9, '东城区单间出租', '东城区单间出租，适合单身人士，交通便利。', NULL);
INSERT INTO `news` (`id`, `time`, `house_id`, `title`, `desc`, `landlord_username`) VALUES (6, '2025-04-15 14:00:00', 7, '丰台区整租四居室', '丰台区整租四居室，适合家庭居住，环境优美。', NULL);
INSERT INTO `news` (`id`, `time`, `house_id`, `title`, `desc`, `landlord_username`) VALUES (7, '2025-04-18 11:00:00', 5, '通州区新房源上线', '通州区新房源上线，欢迎咨询详情。', NULL);
INSERT INTO `news` (`id`, `time`, `house_id`, `title`, `desc`, `landlord_username`) VALUES (8, '2025-05-18 21:25:48', 16, '上海市好房子特价', '无敌优势', '房东C');
COMMIT;

-- ----------------------------
-- Table structure for private_channel
-- ----------------------------
DROP TABLE IF EXISTS `private_channel`;
CREATE TABLE `private_channel` (
  `channel_id` int NOT NULL AUTO_INCREMENT,
  `tenant_username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '租客用户名',
  `landlord_username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '房东用户名',
  `house_id` int NOT NULL COMMENT '关联的房屋ID',
  `created_at` datetime NOT NULL COMMENT '频道创建时间',
  PRIMARY KEY (`channel_id`) USING BTREE,
  UNIQUE KEY `uq_tenant_landlord_house` (`tenant_username`,`landlord_username`,`house_id`) USING BTREE,
  KEY `house_id` (`house_id`) USING BTREE,
  KEY `landlord_username` (`landlord_username`) USING BTREE,
  CONSTRAINT `private_channel_ibfk_1` FOREIGN KEY (`landlord_username`) REFERENCES `login` (`username`),
  CONSTRAINT `private_channel_ibfk_2` FOREIGN KEY (`tenant_username`) REFERENCES `login` (`username`),
  CONSTRAINT `private_channel_ibfk_3` FOREIGN KEY (`house_id`) REFERENCES `house_info` (`house_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of private_channel
-- ----------------------------
BEGIN;
INSERT INTO `private_channel` (`channel_id`, `tenant_username`, `landlord_username`, `house_id`, `created_at`) VALUES (1, 'qwe', 'landlord', 5, '2025-05-05 05:17:48');
INSERT INTO `private_channel` (`channel_id`, `tenant_username`, `landlord_username`, `house_id`, `created_at`) VALUES (2, 'qwe', '房东C', 10, '2025-05-05 08:30:26');
INSERT INTO `private_channel` (`channel_id`, `tenant_username`, `landlord_username`, `house_id`, `created_at`) VALUES (3, 'qwe', 'landlord', 6, '2025-05-05 14:38:10');
INSERT INTO `private_channel` (`channel_id`, `tenant_username`, `landlord_username`, `house_id`, `created_at`) VALUES (4, 'qwe', 'landlord', 7, '2025-05-05 23:58:42');
INSERT INTO `private_channel` (`channel_id`, `tenant_username`, `landlord_username`, `house_id`, `created_at`) VALUES (5, 'tenant2', 'landlord', 5, '2025-05-17 03:47:18');
INSERT INTO `private_channel` (`channel_id`, `tenant_username`, `landlord_username`, `house_id`, `created_at`) VALUES (6, 'qwe', 'landlord', 15, '2025-05-17 13:04:18');
COMMIT;

-- ----------------------------
-- Table structure for rental_contract
-- ----------------------------
DROP TABLE IF EXISTS `rental_contract`;
CREATE TABLE `rental_contract` (
  `id` int NOT NULL AUTO_INCREMENT,
  `channel_id` int NOT NULL,
  `landlord_username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `tenant_username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `status` int NOT NULL COMMENT '0：待支付，1：支付成功，2：取消订单,3：撤销订单',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of rental_contract
-- ----------------------------
BEGIN;
INSERT INTO `rental_contract` (`id`, `channel_id`, `landlord_username`, `tenant_username`, `start_date`, `end_date`, `total_amount`, `status`, `created_at`, `updated_at`) VALUES (2, 3, 'landlord', 'qwe', '2025-05-24', '2025-06-24', 36000.00, 3, '2025-05-17 02:30:47', '2025-05-17 13:03:21');
INSERT INTO `rental_contract` (`id`, `channel_id`, `landlord_username`, `tenant_username`, `start_date`, `end_date`, `total_amount`, `status`, `created_at`, `updated_at`) VALUES (5, 5, 'landlord', 'tenant2', '2025-05-01', '2025-11-01', 64000.00, 3, '2025-05-17 04:19:48', '2025-05-17 13:03:21');
INSERT INTO `rental_contract` (`id`, `channel_id`, `landlord_username`, `tenant_username`, `start_date`, `end_date`, `total_amount`, `status`, `created_at`, `updated_at`) VALUES (6, 1, 'landlord', 'qwe', '2025-05-01', '2025-08-01', 40000.00, 3, '2025-05-17 04:24:06', '2025-05-17 13:03:21');
INSERT INTO `rental_contract` (`id`, `channel_id`, `landlord_username`, `tenant_username`, `start_date`, `end_date`, `total_amount`, `status`, `created_at`, `updated_at`) VALUES (7, 1, 'landlord', 'qwe', '2025-05-01', '2025-08-01', 40000.00, 3, '2025-05-17 05:49:41', '2025-05-17 13:03:21');
INSERT INTO `rental_contract` (`id`, `channel_id`, `landlord_username`, `tenant_username`, `start_date`, `end_date`, `total_amount`, `status`, `created_at`, `updated_at`) VALUES (8, 4, 'landlord', 'qwe', '2025-05-24', '2025-10-24', 35000.00, 1, '2025-05-17 12:20:00', '2025-05-17 12:51:24');
INSERT INTO `rental_contract` (`id`, `channel_id`, `landlord_username`, `tenant_username`, `start_date`, `end_date`, `total_amount`, `status`, `created_at`, `updated_at`) VALUES (9, 6, 'landlord', 'qwe', '2025-05-16', '2025-06-16', 25500.00, 3, '2025-05-17 13:05:18', '2025-05-17 13:05:52');
INSERT INTO `rental_contract` (`id`, `channel_id`, `landlord_username`, `tenant_username`, `start_date`, `end_date`, `total_amount`, `status`, `created_at`, `updated_at`) VALUES (10, 6, 'landlord', 'qwe', '2025-05-17', '2025-06-17', 25500.00, 1, '2025-05-17 13:06:05', '2025-05-17 13:07:36');
INSERT INTO `rental_contract` (`id`, `channel_id`, `landlord_username`, `tenant_username`, `start_date`, `end_date`, `total_amount`, `status`, `created_at`, `updated_at`) VALUES (11, 3, 'landlord', 'qwe', '2025-03-17', '2025-04-17', 36000.00, 1, '2025-05-17 13:21:35', '2025-05-17 13:22:30');
COMMIT;

-- ----------------------------
-- Table structure for repair_request
-- ----------------------------
DROP TABLE IF EXISTS `repair_request`;
CREATE TABLE `repair_request` (
  `id` int NOT NULL AUTO_INCREMENT,
  `house_id` int NOT NULL COMMENT '关联房屋ID',
  `tenant_username` varchar(100) NOT NULL COMMENT '租客用户名',
  `landlord_username` varchar(100) NOT NULL COMMENT '房东用户名',
  `content` text NOT NULL COMMENT '维修内容描述',
  `request_time` datetime NOT NULL COMMENT '请求发起时间',
  `status` varchar(50) NOT NULL COMMENT '维修请求状态',
  `handler_notes` text COMMENT '房东处理备注',
  `handled_time` datetime DEFAULT NULL COMMENT '房东处理时间',
  PRIMARY KEY (`id`),
  KEY `house_id` (`house_id`),
  KEY `landlord_username` (`landlord_username`),
  KEY `tenant_username` (`tenant_username`),
  CONSTRAINT `repair_request_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `house_info` (`house_id`) ON DELETE CASCADE,
  CONSTRAINT `repair_request_ibfk_2` FOREIGN KEY (`landlord_username`) REFERENCES `login` (`username`) ON DELETE CASCADE,
  CONSTRAINT `repair_request_ibfk_3` FOREIGN KEY (`tenant_username`) REFERENCES `login` (`username`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of repair_request
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for tenant
-- ----------------------------
DROP TABLE IF EXISTS `tenant`;
CREATE TABLE `tenant` (
  `tenant_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '租客用户名',
  `phone` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '联系方式',
  `addr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户住址',
  PRIMARY KEY (`tenant_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of tenant
-- ----------------------------
BEGIN;
INSERT INTO `tenant` (`tenant_name`, `phone`, `addr`) VALUES ('qwe', '13912345678', '1232423');
INSERT INTO `tenant` (`tenant_name`, `phone`, `addr`) VALUES ('tenant2', '13800138005', '北京市东城区');
INSERT INTO `tenant` (`tenant_name`, `phone`, `addr`) VALUES ('wer', '13850844558', '湖北省恩施土家族苗族自治州恩施市');
INSERT INTO `tenant` (`tenant_name`, `phone`, `addr`) VALUES ('租客A', '13800138003', '北京市丰台区');
INSERT INTO `tenant` (`tenant_name`, `phone`, `addr`) VALUES ('租客C', '13800138004', '北京市东城区');
COMMIT;

-- ----------------------------
-- Table structure for user_email
-- ----------------------------
DROP TABLE IF EXISTS `user_email`;
CREATE TABLE `user_email` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户邮箱',
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联的用户名',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uq_email_username_map` (`email`,`username`) USING BTREE,
  KEY `username` (`username`) USING BTREE,
  KEY `ix_user_email_email` (`email`) USING BTREE,
  CONSTRAINT `user_email_ibfk_1` FOREIGN KEY (`username`) REFERENCES `login` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of user_email
-- ----------------------------
BEGIN;
INSERT INTO `user_email` (`id`, `email`, `username`) VALUES (1, '1513979779@qq.com', 'landlord');
INSERT INTO `user_email` (`id`, `email`, `username`) VALUES (3, '1513979779@qq.com', 'qwe');
INSERT INTO `user_email` (`id`, `email`, `username`) VALUES (5, '1513979779@qq.com', 'tenant2');
INSERT INTO `user_email` (`id`, `email`, `username`) VALUES (7, '1513979779@qq.com', '房东B');
INSERT INTO `user_email` (`id`, `email`, `username`) VALUES (9, '1513979779@qq.com', '租客A');
INSERT INTO `user_email` (`id`, `email`, `username`) VALUES (2, '3225340736@qq.com', 'landlord3');
INSERT INTO `user_email` (`id`, `email`, `username`) VALUES (4, '3225340736@qq.com', 'tenant');
INSERT INTO `user_email` (`id`, `email`, `username`) VALUES (8, '3225340736@qq.com', '房东C');
INSERT INTO `user_email` (`id`, `email`, `username`) VALUES (10, '3225340736@qq.com', '租客C');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
