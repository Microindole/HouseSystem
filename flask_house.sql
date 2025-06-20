-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: flask_house
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`version_num`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('a13638c5c4d9');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
  CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`landlord_name`) REFERENCES `landlord` (`landlord_name`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `appointment_ibfk_2` FOREIGN KEY (`house_id`) REFERENCES `house_info` (`house_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `appointment_ibfk_3` FOREIGN KEY (`tenant_name`) REFERENCES `tenant` (`tenant_name`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment`
--

LOCK TABLES `appointment` WRITE;
/*!40000 ALTER TABLE `appointment` DISABLE KEYS */;
INSERT INTO `appointment` VALUES (3,28,'sss','qwe','landlord','2025-06-03 10:14:00','已拒绝'),(4,28,'sss','qwe','landlord','2025-06-03 10:25:00','已同意'),(5,28,'sss','qwe','landlord','2025-06-03 10:27:00','已拒绝'),(6,28,'sss','qwe','landlord','2025-06-03 10:31:00','已拒绝');
/*!40000 ALTER TABLE `appointment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `comment_id` int NOT NULL AUTO_INCREMENT,
  `house_id` int NOT NULL COMMENT '房屋的id',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '留言人名字',
  `type` int NOT NULL COMMENT '留言人类型,1:租客，2:房东',
  `desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '留言内容',
  `at` int DEFAULT NULL COMMENT '@哪条留言，前端显示为@谁，选填',
  `time` datetime NOT NULL COMMENT '留言时间',
  PRIMARY KEY (`comment_id`) USING BTREE,
  KEY `house_id` (`house_id`) USING BTREE,
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `house_info` (`house_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=190 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (188,16,'qwe',1,'xxx',NULL,'2025-05-27 13:58:03'),(189,16,'qwe',1,'sb',188,'2025-05-27 13:58:10');
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `complaint`
--

DROP TABLE IF EXISTS `complaint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
  KEY `receiver` (`receiver`) USING BTREE,
  KEY `sender` (`sender`) USING BTREE,
  CONSTRAINT `complaint_ibfk_1` FOREIGN KEY (`handler_username`) REFERENCES `login` (`username`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `complaint_ibfk_2` FOREIGN KEY (`receiver`) REFERENCES `login` (`username`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `complaint_ibfk_3` FOREIGN KEY (`sender`) REFERENCES `login` (`username`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `complaint`
--

LOCK TABLES `complaint` WRITE;
/*!40000 ALTER TABLE `complaint` DISABLE KEYS */;
INSERT INTO `complaint` VALUES (3,'qwe',NULL,'dfg','2025-05-07 02:21:56','投诉','处理中','admin','2025-05-07 02:43:12',1),(4,'qwe','landlord','sss','2025-05-07 02:46:00','投诉','已解决','admin','2025-05-07 02:58:00',1);
/*!40000 ALTER TABLE `complaint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contract_info`
--

DROP TABLE IF EXISTS `contract_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contract_info` (
  `rental_contract_id` int NOT NULL COMMENT '关联的RentalContract订单号 (主键)',
  `contract_document_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '合同示范文本编号 (如 GF—2025—2614)',
  `lease_purpose_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '租赁用途 (合同约定)',
  `rent_payment_frequency` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '租金支付频率 (合同记录)',
  `landlord_bank_account_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '甲方收款账户信息 (合同记录)',
  `other_agreements_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '其他约定事项全文 (合同记录)',
  `handover_checklist_details_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '房屋交割单详细内容或数据 (合同记录)',
  `info_created_at` datetime DEFAULT NULL,
  `info_updated_at` datetime DEFAULT NULL,
  `house_details_text_snapshot` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '房屋坐落、权属、面积、户型、装修及车位等基本情况描述 (合同快照)',
  `deposit_amount_numeric_snapshot` decimal(10,2) DEFAULT NULL COMMENT '押金金额数字快照 (合同记录)',
  `landlord_signature_identifier` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '甲方签名标识 (如用户名或图片URL)',
  `landlord_signature_datetime` datetime DEFAULT NULL COMMENT '甲方签名时间',
  `tenant_signature_identifier` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '乙方签名标识 (如用户名或图片URL)',
  `tenant_signature_datetime` datetime DEFAULT NULL COMMENT '乙方签名时间',
  `landlord_handover_signature_identifier` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '交割单甲方签名标识',
  `landlord_handover_signature_datetime` datetime DEFAULT NULL COMMENT '交割单甲方签名时间',
  `tenant_handover_signature_identifier` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '交割单乙方签名标识',
  `tenant_handover_signature_datetime` datetime DEFAULT NULL COMMENT '交割单乙方签名时间',
  PRIMARY KEY (`rental_contract_id`) USING BTREE,
  CONSTRAINT `contract_info_ibfk_1` FOREIGN KEY (`rental_contract_id`) REFERENCES `rental_contract` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contract_info`
--

LOCK TABLES `contract_info` WRITE;
/*!40000 ALTER TABLE `contract_info` DISABLE KEYS */;
INSERT INTO `contract_info` VALUES (13,'GF—2025—13','居住','月付',NULL,NULL,NULL,'2025-06-01 05:03:25','2025-06-01 14:38:14','房屋坐落于河南省省直辖县级行政区划济源市，人民政府，\n房屋权属：产权清晰，甲方拥有合法出租权，\n建筑面积约未提供平方米，\n户型：1室2厅，\n所在楼层：未提供，\n装修状况：精装，\n配套设施：2345；\n车位信息：无；\n其他描述：房屋状态良好，水电气暖设施齐全，符合正常居住条件。',123456.00,NULL,NULL,'qwe','2025-06-01 14:38:14',NULL,NULL,NULL,NULL),(15,'GF—2025—2614',NULL,'月付',NULL,'',NULL,'2025-05-31 17:46:26','2025-06-01 14:20:13',NULL,NULL,NULL,NULL,'qwe','2025-06-01 14:20:13',NULL,NULL,NULL,NULL),(16,'GF—2025—2614','居住','月付',NULL,NULL,NULL,'2025-06-01 14:24:06','2025-06-01 14:37:28','房屋地址: 福建省三明市三元区莘口镇派出所, 户型: 2室1厅, 装修: 简装.',3000.00,NULL,NULL,'qwe','2025-06-01 14:37:28',NULL,NULL,NULL,NULL),(17,'GF—2025—2614','居住','一次性付清',NULL,NULL,NULL,'2025-06-01 15:26:35','2025-06-01 15:26:35','房屋地址: 湖南省长沙市岳麓区岳麓街道清水路中南大学南校区14栋, 户型: 3室1厅, 装修: 精装.',11111.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(18,'GF—2025—2614','居住','月付',NULL,NULL,NULL,'2025-06-01 15:27:31','2025-06-01 15:27:31','房屋地址: 湖南省长沙市岳麓区岳麓街道清水路中南大学南校区14栋, 户型: 3室1厅, 装修: 精装.',11111.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(25,'GF—2025—2614','居住','一次性付清',NULL,NULL,NULL,'2025-06-01 17:49:49','2025-06-01 17:52:01','房屋地址: 湖南省长沙市岳麓区岳麓街道清水路中南大学南校区14栋, 户型: 3室1厅, 装修: 精装.',11111.00,NULL,NULL,'qwe','2025-06-01 17:52:01',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `contract_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `daily_rent_rate`
--

DROP TABLE IF EXISTS `daily_rent_rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `daily_rent_rate` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `date` date NOT NULL COMMENT '统计日期',
  `total_count` int NOT NULL DEFAULT '0' COMMENT '上架总数（状态为0）',
  `rented_count` int NOT NULL DEFAULT '0' COMMENT '出租数（状态为1）',
  `rent_rate` decimal(5,2) NOT NULL COMMENT '出租率百分比（如 66.67）',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `date` (`date`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `daily_rent_rate`
--

LOCK TABLES `daily_rent_rate` WRITE;
/*!40000 ALTER TABLE `daily_rent_rate` DISABLE KEYS */;
INSERT INTO `daily_rent_rate` VALUES (1,'2025-05-06',6,1,16.67),(2,'2025-05-07',6,3,50.00),(3,'2025-05-10',4,3,75.00),(4,'2025-05-11',4,2,50.00),(5,'2025-05-17',6,6,100.00),(6,'2025-06-01',7,2,28.57);
/*!40000 ALTER TABLE `daily_rent_rate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `house_info`
--

DROP TABLE IF EXISTS `house_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=129 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `house_info`
--

LOCK TABLES `house_info` WRITE;
/*!40000 ALTER TABLE `house_info` DISABLE KEYS */;
INSERT INTO `house_info` VALUES (8,'新房源1','3室2厅','北京市东城区','东直门大街',15000.00,30000.00,'豪华装修','交通便利，配套齐全','static/images/OIP-C (3).jpg'),(9,'东城区豪华三居室','3室1厅','北京市朝阳区','朝阳北路',8000.00,16000.00,'精装修','近地铁，生活便利','static/images/OIP-C (3).jpg'),(10,'海淀区豪华三居室','3室2厅','北京市海淀区','中关村大街',15000.00,30000.00,'豪华装修','学区房，交通便利','static/images/haidian_3room.jpg'),(16,'测试版精修郊区别野','4室2厅','上海市上海市朝阳区','浦东112',50000.00,500000.00,'精装','非常好，详情电话咨询','static/images/20250518212017_6896.jpg_wh860.jpg'),(25,'北京市廉价房','1室2厅','河南省省直辖县级行政区划济源市','人民政府',1234.00,123456.00,'精装','2345','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp/b513dd1a0bdb4947ac04a8cccda45efb.jpg'),(27,'岳麓区简装一居室','2室1厅','福建省三明市三元区','莘口镇派出所',1000.00,3000.00,'简装','离学校近','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp/42761b7341354966a9231985ccd53aae.jpg'),(28,'sss','3室1厅','湖南省长沙市岳麓区','岳麓街道清水路中南大学南校区14栋',114444.00,11111.00,'精装','在学校','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp/9a41f0789f374b2b8fcb66f54787bd92.jpg'),(29,'福田区优质房源1号','3室2厅2卫','广东省深圳市福田区','深圳市福田区建设路173号和谐新村13号楼',9947.00,19894.00,'现代装修，基础设施完善','装修精美，拎包入住','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_0/7c5bbb26c81142ef8d8d7c35b157b511.jpg'),(30,'海淀区温馨公寓2号','3室2厅2卫','北京市海淀区','北京市海淀区文化路849号幸福大厦26号楼',7674.00,15348.00,'精装修，家具家电齐全','楼层好，视野开阔','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_1/33cae1e377414d558e6149cc938952e3.jpg'),(31,'番禺区舒适家园3号','3室2厅1卫','广东省广州市番禺区','广州市番禺区人民路654号温馨广场3号楼',9816.00,19632.00,'豪华装修，家具家电齐全','地铁站旁，交通便利','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_2/5531bd65db6f49a09a75055c27792695.jpg'),(32,'福田区现代公寓4号','5室3厅4卫','广东省深圳市福田区','深圳市福田区胜利路404号温馨广场25号楼',19189.00,38378.00,'豪华装修，家具家电齐全','环境优美，绿化好','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_3/e1590516023c4e8784665044f1f86fe2.jpg'),(33,'朝阳区优质房源5号','1室1厅1卫','北京市朝阳区','北京市朝阳区建设路240号幸福苑9号楼',5687.00,11374.00,'欧式装修，设施新','学区房，教育资源丰富','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_4/ccc8f091125c43e0b76a59df3f7d8eb4.jpg'),(34,'东城区高端住宅6号','2室2厅1卫','北京市东城区','北京市东城区建设路347号和谐公寓16号楼',5633.00,11266.00,'简装修，配套齐全','商务中心，购物便利','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_5/9cc134a6194649e08e29a60a4e236271.jpg'),(35,'拱墅区豪华住宅7号','4室2厅2卫','浙江省杭州市拱墅区','杭州市拱墅区和平路773号温馨新村3号楼',14574.00,29148.00,'现代装修，设施新','采光好，通风佳','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_6/374d525b4b3e4260927e69de090723f5.jpg'),(36,'建邺区优质房源8号','5室3厅4卫','江苏省南京市建邺区','南京市建邺区建设路676号幸福新村10号楼',22096.00,44192.00,'豪华装修，基础设施完善','采光好，通风佳','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_7/e10f763e7a984c229f29b5abdc065040.jpg'),(37,'西湖区优质房源9号','1室1厅1卫','浙江省杭州市西湖区','杭州市西湖区文化路219号温馨小区15号楼',2373.00,4746.00,'简装修，家具家电齐全','环境优美，绿化好','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_8/e6a551e530a746d299f94229d6b6caf0.jpg'),(38,'东城区学区房源10号','5室3厅4卫','北京市东城区','北京市东城区和平路782号阳光广场19号楼',20485.00,40970.00,'欧式装修，家具家电齐全','地铁站旁，交通便利','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_9/298e5db56968479db72b44ae1f65c07e.jpg'),(39,'徐汇区学区房源11号','3室2厅2卫','上海市徐汇区','上海市徐汇区和平路3号美好大厦29号楼',9146.00,18292.00,'中式装修，基础设施完善','采光好，通风佳','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_10/ba1113833e15463782712cb4e2cd06a7.jpg'),(40,'徐汇区学区房源12号','2室2厅1卫','上海市徐汇区','上海市徐汇区文化路624号温馨苑10号楼',7868.00,15736.00,'毛坯房，基础设施完善','装修精美，拎包入住','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_11/435e80beaf884c4b97c0f80704be63e9.jpg'),(41,'海淀区优质房源13号','2室1厅1卫','北京市海淀区','北京市海淀区光明路695号美好小区23号楼',5854.00,11708.00,'精装修，配套齐全','装修精美，拎包入住','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_12/8a29c57871ce4114b6f78d22854df313.jpg'),(42,'南山区舒适家园14号','3室2厅2卫','广东省深圳市南山区','深圳市南山区解放路860号阳光花园24号楼',8493.00,16986.00,'简装修，设施新','楼层好，视野开阔','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_13/d13345e412bd401aa8b3adb0f95cc8d3.jpg'),(43,'黄浦区学区房源15号','3室2厅2卫','上海市黄浦区','上海市黄浦区建设路176号温馨花园21号楼',8633.00,17266.00,'现代装修，基础设施完善','配套设施完善','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_14/a26580e289ea4bc39b3b1e35f1912734.jpg'),(44,'南山区学区房源16号','5室3厅4卫','广东省深圳市南山区','深圳市南山区中山路572号和谐花园20号楼',19880.00,39760.00,'现代装修，家具家电齐全','地铁站旁，交通便利','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_15/f027bcb9c2a9465ca5814ba1e761ce0f.jpg'),(45,'玄武区学区房源17号','3室2厅2卫','江苏省南京市玄武区','南京市玄武区解放路37号和谐小区25号楼',8227.00,16454.00,'毛坯房，配套齐全','配套设施完善','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_16/757c1e7f603d45819f3d16dffb576d95.jpg'),(46,'西湖区阳光花园18号','1室1厅1卫','浙江省杭州市西湖区','杭州市西湖区建设路425号和谐新村12号楼',2994.00,5988.00,'豪华装修，配套齐全','安保严密，居住安全','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_17/14771c9885dd4ef980ebcffd48009c14.jpg'),(47,'东城区精品公寓19号','2室2厅1卫','北京市东城区','北京市东城区解放路254号温馨小区6号楼',4422.00,8844.00,'简装修，基础设施完善','楼层好，视野开阔','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_18/508509eb7829419b9d105b364f7c86fe.jpg'),(48,'西湖区阳光花园20号','2室1厅1卫','浙江省杭州市西湖区','杭州市西湖区人民路44号美好新村24号楼',4779.00,9558.00,'欧式装修，家具家电齐全','地铁站旁，交通便利','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_19/ee6eaa310dd748dabbcb6e6da7a9445c.jpg'),(49,'番禺区优质房源21号','3室2厅2卫','广东省广州市番禺区','广州市番禺区建设路326号阳光小区18号楼',8011.00,16022.00,'欧式装修，基础设施完善','安保严密，居住安全','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_20/475fbee443744ca3aa96378ea4eee8db.jpg'),(50,'白云区学区房源22号','3室2厅2卫','广东省广州市白云区','广州市白云区文化路871号和谐广场17号楼',9748.00,19496.00,'毛坯房，基础设施完善','配套设施完善','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_21/4a253187c5b34ab096ebb67033d866cc.jpg'),(51,'西城区优质房源23号','1室1厅1卫','北京市西城区','北京市西城区和平路985号幸福广场30号楼',3916.00,7832.00,'精装修，设施新','配套设施完善','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_22/c537e58c478742f986a9e5a1a0252066.jpg'),(52,'黄浦区现代公寓24号','2室1厅1卫','上海市黄浦区','上海市黄浦区胜利路78号温馨广场8号楼',6439.00,12878.00,'简装修，基础设施完善','环境优美，绿化好','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_23/83f1ab902b4445a4b5c277bdc8bc38a2.jpg'),(53,'白云区温馨公寓25号','1室1厅1卫','广东省广州市白云区','广州市白云区建设路235号幸福新村4号楼',2137.00,4274.00,'简装修，配套齐全','学区房，教育资源丰富','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_24/6f380ba20a304f0bb5d6103b58b02723.jpg'),(54,'玄武区阳光花园26号','3室2厅1卫','江苏省南京市玄武区','南京市玄武区胜利路972号和谐新村30号楼',6533.00,13066.00,'现代装修，配套齐全','环境优美，绿化好','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_25/5857cc6a843241c19bda9270785d643a.jpg'),(55,'越秀区豪华住宅27号','4室2厅2卫','广东省广州市越秀区','广州市越秀区胜利路305号幸福公寓14号楼',14762.00,29524.00,'中式装修，设施新','环境优美，绿化好','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_26/742afdb1ed1e4db6a23e171ae061120c.jpg'),(56,'黄浦区现代公寓28号','2室2厅1卫','上海市黄浦区','上海市黄浦区中山路224号温馨广场3号楼',5262.00,10524.00,'中式装修，家具家电齐全','装修精美，拎包入住','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_27/4486f57f0ea54398b8631c8b897294d8.jpg'),(57,'徐汇区优质房源29号','2室1厅1卫','上海市徐汇区','上海市徐汇区光明路930号幸福广场11号楼',4595.00,9190.00,'毛坯房，家具家电齐全','环境优美，绿化好','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_28/c284758cf54f4306a3e93ec2a04c4b57.jpg'),(58,'罗湖区现代公寓30号','4室2厅2卫','广东省深圳市罗湖区','深圳市罗湖区建设路70号温馨公寓8号楼',13995.00,27990.00,'中式装修，家具家电齐全','学区房，教育资源丰富','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_29/abf11dd4284a4decbae2bb131293ccb0.jpg'),(59,'福田区现代公寓31号','3室2厅2卫','广东省深圳市福田区','深圳市福田区解放路556号美好广场29号楼',6929.00,13858.00,'中式装修，基础设施完善','地铁站旁，交通便利','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_30/79c364ba6b8d4ab6a1dea1c7f453a035.jpg'),(60,'宝安区现代公寓32号','2室2厅1卫','广东省深圳市宝安区','深圳市宝安区光明路352号温馨小区4号楼',5832.00,11664.00,'精装修，基础设施完善','装修精美，拎包入住','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_31/cc22aa5b61f94c888cfc728f6e494e29.jpg'),(61,'西湖区优质房源33号','1室1厅1卫','浙江省杭州市西湖区','杭州市西湖区文化路161号阳光家园9号楼',5510.00,11020.00,'豪华装修，设施新','商务中心，购物便利','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_32/98047f1dc47741c1a10ffc1bad04f505.jpg'),(62,'宝安区精品公寓34号','5室3厅4卫','广东省深圳市宝安区','深圳市宝安区文化路722号美好大厦27号楼',21539.00,43078.00,'精装修，设施新','采光好，通风佳','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_33/9e1251725f6a47d6b4c5e513f80a5d3d.jpg'),(63,'东城区高端住宅35号','2室2厅1卫','北京市东城区','北京市东城区人民路316号温馨广场7号楼',4684.00,9368.00,'豪华装修，基础设施完善','装修精美，拎包入住','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_34/82ca8926dcf948908b7135ed4aeee414.jpg'),(64,'浦东新区便民公寓36号','1室1厅1卫','上海市浦东新区','上海市浦东新区胜利路326号美好公寓20号楼',5496.00,10992.00,'简装修，家具家电齐全','楼层好，视野开阔','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_35/c8b9c18093d348318ed5b7b7fdf40f12.jpg'),(65,'越秀区现代公寓37号','1室1厅1卫','广东省广州市越秀区','广州市越秀区和平路416号阳光公寓11号楼',4210.00,8420.00,'毛坯房，配套齐全','环境优美，绿化好','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_36/6bc27049c429407fbee9a2df43b0bcfb.jpg'),(66,'番禺区温馨公寓38号','3室2厅2卫','广东省广州市番禺区','广州市番禺区文化路820号和谐家园28号楼',8336.00,16672.00,'精装修，基础设施完善','学区房，教育资源丰富','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_37/052fb89fe2ee49bdba468d323826a74b.jpg'),(67,'西城区温馨公寓39号','4室2厅2卫','北京市西城区','北京市西城区解放路281号和谐新村27号楼',14805.00,29610.00,'现代装修，配套齐全','学区房，教育资源丰富','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_38/a02f1535d32a484683fac80ff0105c66.jpg'),(68,'越秀区高端住宅40号','2室1厅1卫','广东省广州市越秀区','广州市越秀区文化路869号幸福苑25号楼',4766.00,9532.00,'中式装修，基础设施完善','安保严密，居住安全','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_39/805977b70c104ed69741c0d66613752d.jpg'),(69,'宝安区现代公寓41号','1室1厅1卫','广东省深圳市宝安区','深圳市宝安区建设路549号美好花园17号楼',3324.00,6648.00,'现代装修，配套齐全','采光好，通风佳','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_40/bf2a99371d9d49d3a2a5fa057e000eaa.jpg'),(70,'朝阳区精品公寓42号','2室1厅1卫','北京市朝阳区','北京市朝阳区光明路243号阳光小区6号楼',6812.00,13624.00,'豪华装修，家具家电齐全','安保严密，居住安全','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_41/7af3ea19dfd6401b89e31eaacb255402.jpg'),(71,'上城区温馨公寓43号','1室1厅1卫','浙江省杭州市上城区','杭州市上城区文化路528号温馨苑27号楼',2677.00,5354.00,'欧式装修，配套齐全','安保严密，居住安全','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_42/78aba7582c184202836c3251501c3dff.jpg'),(72,'天河区精品公寓44号','4室2厅2卫','广东省广州市天河区','广州市天河区胜利路377号幸福苑2号楼',12343.00,24686.00,'欧式装修，家具家电齐全','装修精美，拎包入住','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_43/c22a7d2763da40f198a9745f3a451a94.jpg'),(73,'南山区高端住宅45号','4室2厅2卫','广东省深圳市南山区','深圳市南山区胜利路873号温馨大厦28号楼',12905.00,25810.00,'毛坯房，配套齐全','地铁站旁，交通便利','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_44/c05eb7abb50f47d8a65eb00a12b12a50.jpg'),(74,'罗湖区精品公寓46号','1室1厅1卫','广东省深圳市罗湖区','深圳市罗湖区解放路451号和谐新村19号楼',4868.00,9736.00,'现代装修，家具家电齐全','学区房，教育资源丰富','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_45/0c5fad23adbb4631b4aa76b230b1a689.jpg'),(75,'朝阳区温馨公寓47号','3室2厅1卫','北京市朝阳区','北京市朝阳区解放路460号温馨花园6号楼',8977.00,17954.00,'精装修，基础设施完善','商务中心，购物便利','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_46/4ac073702f274e4fb98be12ffa033016.jpg'),(76,'白云区精品公寓48号','1室1厅1卫','广东省广州市白云区','广州市白云区胜利路761号幸福公寓23号楼',5481.00,10962.00,'简装修，基础设施完善','配套设施完善','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_47/20198bd6b7cd485494c29e8777ddb16d.jpg'),(77,'拱墅区豪华住宅49号','2室2厅1卫','浙江省杭州市拱墅区','杭州市拱墅区胜利路994号温馨家园7号楼',4115.00,8230.00,'精装修，配套齐全','地铁站旁，交通便利','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_48/b157f991f5bb4b31a3825d1a766fc59e.jpg'),(78,'建邺区温馨公寓50号','2室1厅1卫','江苏省南京市建邺区','南京市建邺区人民路798号温馨公寓26号楼',5926.00,11852.00,'精装修，配套齐全','安保严密，居住安全','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/temp_49/2dd08639473e4b6c852b1f77f6538d31.jpg'),(79,'城阳区典雅庭51号','2室2厅1卫','山东省青岛市城阳区','青岛市城阳区花园路256号典雅家园5号楼26层',3764.00,7826.67,'工业风装修，简单家具，采光充足','地铁站旁，交通便利','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_0/763259767b8040f4b07b52b0e81c8b4c.jpg'),(80,'岳麓区格调府52号','5室4厅3卫','湖南省长沙市岳麓区','长沙市岳麓区振兴街128号格调苑11号楼11层',17003.00,34187.89,'北欧风格装修，家具家电齐全，空调暖气','周边大学多，文化氛围浓','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_1/c04dacf68c394199ba28299201c61565.jpg'),(81,'下城区尊贵苑53号','5室4厅3卫','浙江省杭州市下城区','杭州市下城区团结路402号尊贵花园26号楼23层',23875.00,54842.53,'豪华装修，智能家居，空调暖气','停车位充足，出行方便','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_2/ec3dfb1ad3a84161800e787c79f200cd.jpg'),(82,'典雅园54号','2室2厅1卫','山东省青岛市市南区','青岛市市南区繁荣街488号典雅居48号楼7层',4033.00,7452.40,'简装修，无家具，楼层适中','高层建筑，景观好','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_3/dbe42612e7384209971932d3d406a32f.jpg'),(83,'集美区品质城55号','1室1厅1卫','福建省厦门市集美区','厦门市集美区团结路970号品质阁12号楼13层',3002.00,5524.05,'新中式装修，无家具，临街不吵','公园旁边，空气清新','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_4/f3a3b8b8a0fd43e59eb68b4a55e7d20b.jpg'),(84,'西城区学区墅56号','2室1厅1卫','北京市西城区','北京市西城区友谊路941号学区庭28号楼27层',5423.00,12412.49,'豪华装修，基础设施完善，临街不吵','独立阳台，采光充足','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_5/2151914db9674f9eacd2cbe5a0bda5d4.jpg'),(85,'相城区江景阁57号','4室3厅2卫','江苏省苏州市相城区','苏州市相城区建设路824号江景阁20号楼27层',14109.00,27807.92,'现代装修，无家具，临街不吵','楼层好，视野开阔','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_6/a39c239d32c34b47aa05dfe91d925cd8.jpg'),(86,'福田区雅致岸58号','3室2厅3卫','广东省深圳市福田区','深圳市福田区人民路911号雅致公寓45号楼1层',10632.00,25222.02,'欧式装修，设施新，电梯直达','装修精美，拎包入住','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_7/a519e859e23644cea337c04c334fdf34.jpg'),(87,'宝安区优质里59号','2室1厅1卫','广东省深圳市宝安区','深圳市宝安区学府路191号优质阁42号楼6层',7011.00,14059.51,'日式装修，配套齐全，楼层适中','临近医院，就医方便','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_8/627c3a1cb2d64eeb8c194820aa6aa86d.jpg'),(88,'洪山区雅致居60号','2室1厅2卫','湖北省武汉市洪山区','武汉市洪山区商业街660号雅致轩15号楼13层',4217.00,9291.46,'现代装修，高端家具，空调暖气','学区房，教育资源丰富','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_9/369d1f30c1c04e32a67b3d8ec4ee37f6.jpg'),(89,'上城区学区台61号','4室2厅3卫','浙江省杭州市上城区','杭州市上城区滨江路231号学区家园19号楼9层',12567.00,27207.40,'日式装修，部分家具，采光充足','周边大学多，文化氛围浓','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_10/5a19159e2807432d9af9a67e766f5aa8.jpg'),(90,'江北区格调园62号','4室2厅2卫','重庆市重庆市江北区','重庆市江北区未来街9号格调轩18号楼9层',10730.00,23091.69,'毛坯房，基础设施完善，观景窗','独立阳台，采光充足','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_11/534ccf9d680e47bebf85ce099c8f288e.jpg'),(91,'和平区奢华轩63号','1室1厅2卫','天津市天津市和平区','天津市和平区未来街588号奢华广场28号楼26层',3809.00,9212.37,'工业风装修，智能家居，临街不吵','地铁站旁，交通便利','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_12/3fda74256c8b46c48425b470ecca6c24.jpg'),(92,'天河区尊贵居64号','4室3厅2卫','广东省广州市天河区','广州市天河区建设路450号尊贵城13号楼17层',14602.00,28403.52,'日式装修，拎包入住，采光充足','独立阳台，采光充足','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_13/8e56c4a187ee40b5a8d127c849ca3614.jpg'),(93,'硚口区格调花园65号','2室2厅2卫','湖北省武汉市硚口区','武汉市硚口区中山路922号格调小区38号楼3层',3745.00,7663.65,'美式装修，设施新，通风良好','配套设施完善','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_14/10c8f968177e4e7c9c815f5033756547.jpg'),(94,'天心区典雅里66号','5室3厅4卫','湖南省长沙市天心区','长沙市天心区发展大道392号典雅花园4号楼1层',15700.00,37138.68,'精装修，部分家具，通风良好','环境优美，绿化好','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_15/ff270a9456024945aa7fcd39f3fed0b2.jpg'),(95,'石景山区尊贵公寓67号','1室1厅1卫','北京市石景山区','北京市石景山区花园路836号尊贵轩9号楼2层',4572.00,11262.31,'美式装修，家具家电齐全，空调暖气','新开发区，未来发展好','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_16/fcbc952c4d984863b056d5329160a380.jpg'),(96,'莲湖区温馨岸68号','5室4厅3卫','陕西省西安市莲湖区','西安市莲湖区友谊路23号温馨公寓10号楼20层',19621.00,39524.63,'现代装修，家具家电齐全，空调暖气','停车位充足，出行方便','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_17/198f906bf1174398b0a8448de412a598.jpg'),(97,'大渡口区豪华台69号','2室1厅2卫','重庆市重庆市大渡口区','重庆市大渡口区花园路197号豪华城23号楼9层',5369.00,11738.12,'毛坯房，智能家居，通风良好','地铁站旁，交通便利','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_18/d66559ef2281437b952278bf295b6a46.jpg'),(98,'普陀区静谧住宅70号','3室1厅2卫','上海市普陀区','上海市普陀区滨江路206号静谧花园4号楼20层',10141.00,24931.22,'精装修，智能家居，电梯直达','新开发区，未来发展好','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_19/b14d7cdd97524fb79018dcd1e55a69ab.jpg'),(99,'越秀区优质湾71号','4室2厅2卫','广东省广州市越秀区','广州市越秀区团结路122号优质花园14号楼7层',14261.00,26901.99,'欧式装修，设施新，储物空间大','公园旁边，空气清新','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_20/eb0c9cc298554cdbaa128a1e7fe8de46.jpg'),(100,'姑苏区品质城72号','3室2厅2卫','江苏省苏州市姑苏区','苏州市姑苏区繁荣街861号品质庭46号楼29层',7740.00,17893.77,'欧式装修，无家具，空调暖气','商务中心，购物便利','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_21/2d08a8154d294befbaf9cd9fd4897dd1.jpg'),(101,'思明区温馨里73号','3室1厅2卫','福建省厦门市思明区','厦门市思明区解放路338号温馨家园27号楼14层',6548.00,16046.40,'毛坯房，部分家具，电梯直达','新开发区，未来发展好','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_22/c337acf84d0d4294bdb78ae032f0ac14.jpg'),(102,'碑林区舒适住宅74号','4室2厅2卫','陕西省西安市碑林区','西安市碑林区和平路211号舒适小区28号楼9层',12148.00,25806.09,'北欧风格装修，品牌家电，楼层适中','高层建筑，景观好','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_23/56a7d17c987046ce826870488e45d4f8.jpg'),(103,'南开区奢华墅75号','3室2厅3卫','天津市天津市南开区','天津市南开区繁荣街890号奢华城29号楼17层',6519.00,13207.22,'现代装修，无家具，采光充足','环境优美，绿化好','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_24/d2c71651aa3a425ea82c643d5d6e5109.jpg'),(104,'吴中区品质府76号','1室1厅2卫','江苏省苏州市吴中区','苏州市吴中区文化路65号品质居19号楼12层',2807.00,5185.90,'现代装修，家具家电齐全，通风良好','停车位充足，出行方便','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_25/f653cbe389644ba7ace99b3acc990a38.jpg'),(105,'思明区江景墅77号','1室1厅2卫','福建省厦门市思明区','厦门市思明区文化路952号江景公寓18号楼16层',1582.00,3195.98,'地中海风格装修，简单家具，采光充足','老城区，生活配套成熟','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_26/f8404497cc134de9bbfe8f265ce40477.jpg'),(106,'中山区品质园78号','3室1厅1卫','辽宁省大连市中山区','大连市中山区文化路121号品质轩5号楼10层',5071.00,10215.07,'精装修，品牌家电，储物空间大','高层建筑，景观好','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_27/6fae08633d2c4c2dbcd7aea6d647b1a4.jpg'),(107,'秦淮区舒适湾79号','2室1厅1卫','江苏省南京市秦淮区','南京市秦淮区创新路717号舒适府48号楼14层',5238.00,11063.54,'北欧风格装修，全新家电，楼层适中','24小时保安，安全放心','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_28/14658c7cf6df400c8b9fab25377ccc09.jpg'),(108,'灞桥区宽敞阁80号','4室3厅2卫','陕西省西安市灞桥区','西安市灞桥区创新路951号宽敞花园28号楼4层',12032.00,24658.61,'欧式装修，基础设施完善，储物空间大','社区活动丰富，邻里和谐','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_29/acc1b4c37969407ca33d7cb4076af7cb.jpg'),(109,'西岗区典雅苑81号','2室2厅1卫','辽宁省大连市西岗区','大连市西岗区振兴街472号典雅广场18号楼14层',4939.00,11535.47,'中式装修，家具家电齐全，通风良好','24小时保安，安全放心','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_30/f4156de387954a0a93a80a6db6a5de66.jpg'),(110,'崂山区宽敞台82号','3室2厅2卫','山东省青岛市崂山区','青岛市崂山区解放路224号宽敞轩49号楼1层',6688.00,15957.44,'日式装修，部分家具，楼层适中','商圈中心，生活便利','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_31/1e784ab2822f460aaad6095d2030698d.jpg'),(111,'江汉区静谧城83号','1室1厅1卫','湖北省武汉市江汉区','武汉市江汉区花园路624号静谧苑33号楼6层',2115.00,4028.47,'日式装修，高端家具，观景窗','配套设施完善','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_32/8a40f5970bb541aaaf6658ef18cbdde5.jpg'),(112,'南山区花园家园84号','2室1厅2卫','广东省深圳市南山区','深圳市南山区繁荣街758号花园苑26号楼5层',5873.00,11917.70,'豪华装修，简单家具，噪音小','新开发区，未来发展好','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_33/5e361dfaf7fe48c0989113f591b9c22a.jpg'),(113,'武昌区通透墅85号','5室4厅3卫','湖北省武汉市武昌区','武汉市武昌区中山路815号通透家园32号楼22层',20551.00,38343.89,'豪华装修，家具家电齐全，观景窗','高层建筑，景观好','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_34/d05cf5ff3b3d4df79f7cc89dd6e2df5a.jpg'),(114,'荔湾区私密庭86号','3室1厅2卫','广东省广州市荔湾区','广州市荔湾区解放路381号私密公寓3号楼8层',9964.00,19778.72,'简装修，设施新，楼层适中','独立阳台，采光充足','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_35/a47556a6c3cb41bdb2690bffb0b346ef.jpg'),(115,'吴中区豪华岸87号','3室2厅3卫','江苏省苏州市吴中区','苏州市吴中区繁荣街312号豪华庭23号楼17层',9335.00,17624.89,'精装修，设施新，储物空间大','社区活动丰富，邻里和谐','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_36/d9c28390f9c3400b964047162510f550.jpg'),(116,'思明区雅致公寓88号','3室2厅1卫','福建省厦门市思明区','厦门市思明区未来街645号雅致轩43号楼24层',6887.00,12703.29,'毛坯房，高端家具，临街不吵','物业管理好，服务周到','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_37/1be35ee011af411db51477720289bd43.jpg'),(117,'普陀区豪华庭89号','4室2厅3卫','上海市普陀区','上海市普陀区和平路675号豪华府43号楼12层',15957.00,35304.63,'简装修，家具家电齐全，独立阳台','环境优美，绿化好','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_38/358aebee1d504452ae406a97f2434372.jpg'),(118,'江干区静谧住宅90号','4室3厅2卫','浙江省杭州市江干区','杭州市江干区解放路125号静谧城41号楼28层',13280.00,28893.74,'中式装修，全新家电，独立阳台','楼层好，视野开阔','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_39/b9997592f2284e7096baabf7f3650ad4.jpg'),(119,'青羊区精品湾91号','1室1厅2卫','四川省成都市青羊区','成都市青羊区振兴街523号精品墅18号楼11层',3837.00,7830.45,'毛坯房，家具家电齐全，独立阳台','物业管理好，服务周到','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_40/94545e2241774fa58d613649f745ff04.jpg'),(120,'莲湖区山景墅92号','4室2厅3卫','陕西省西安市莲湖区','西安市莲湖区幸福大道381号山景花园11号楼16层',11642.00,22985.09,'现代装修，部分家具，楼层适中','老城区，生活配套成熟','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_41/d3907897c7b7467db4c3f8ed70142bf5.jpg'),(121,'建邺区雅致湾93号','3室2厅3卫','江苏省南京市建邺区','南京市建邺区友谊路720号雅致苑33号楼16层',9784.00,21375.60,'工业风装修，简单家具，独立阳台','高层建筑，景观好','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_42/74307cf8a9114cad89bf17d574d9dcad.jpg'),(122,'甘井子区湖景园94号','3室2厅2卫','辽宁省大连市甘井子区','大连市甘井子区建设路239号湖景园34号楼24层',5690.00,11578.06,'欧式装修，无家具，电梯直达','学区房，教育资源丰富','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_43/b068208eb858432a88f99e8afaa9bdd2.jpg'),(123,'玄武区典雅阁95号','1室1厅2卫','江苏省南京市玄武区','南京市玄武区解放路497号典雅小区31号楼6层',5136.00,10272.49,'美式装修，高端家具，观景窗','物业管理好，服务周到','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_44/956f80dc4711459ca5f864e92bc429b3.jpg'),(124,'湖里区现代住宅96号','2室2厅1卫','福建省厦门市湖里区','厦门市湖里区团结路692号现代新村16号楼26层',5347.00,10268.03,'日式装修，家具家电齐全，空调暖气','独立阳台，采光充足','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_45/749d6b1f48294585b245c5de57fd3acb.jpg'),(125,'集美区江景里97号','2室1厅2卫','福建省厦门市集美区','厦门市集美区文化路842号江景新村45号楼18层',4434.00,10683.65,'北欧风格装修，设施新，独立阳台','物业管理好，服务周到','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_46/c7772355f3994b04aad9d8f11016c5bb.jpg'),(126,'河北区优质家园98号','4室2厅2卫','天津市天津市河北区','天津市河北区新华路997号优质轩6号楼28层',12747.00,30530.29,'简装修，基础设施完善，通风良好','老城区，生活配套成熟','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_47/a7967736603345bb825bfe9171f20b81.jpg'),(127,'盐田区私密住宅99号','2室1厅1卫','广东省深圳市盐田区','深圳市盐田区友谊路707号私密居9号楼7层',7864.00,16992.60,'工业风装修，基础设施完善，噪音小','公园旁边，空气清新','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_48/aceb816e06be4c87876541fa9e58f8b6.jpg'),(128,'硚口区山景坊100号','2室1厅1卫','湖北省武汉市硚口区','武汉市硚口区滨江路589号山景花园9号楼6层',4241.00,9225.52,'豪华装修，家具家电齐全，楼层适中','停车位充足，出行方便','https://house-system.oss-cn-shenzhen.aliyuncs.com/house_images/batch2_49/8fe21019effc4f6788b7a14c55dab3bb.jpg');
/*!40000 ALTER TABLE `house_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `house_listing_audit`
--

DROP TABLE IF EXISTS `house_listing_audit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
  CONSTRAINT `house_listing_audit_ibfk_1` FOREIGN KEY (`landlord_name`) REFERENCES `landlord` (`landlord_name`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `house_listing_audit_ibfk_2` FOREIGN KEY (`house_id`, `landlord_name`) REFERENCES `house_status` (`house_id`, `landlord_name`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `house_listing_audit`
--

LOCK TABLES `house_listing_audit` WRITE;
/*!40000 ALTER TABLE `house_listing_audit` DISABLE KEYS */;
INSERT INTO `house_listing_audit` VALUES (12,16,'测试版精修郊区别野','房东C',1,NULL,'2025-05-18 21:20:22','2025-05-23 04:06:53'),(17,25,'北京市廉价房','landlord',1,NULL,'2025-05-30 08:59:39','2025-05-30 01:00:05'),(18,25,'北京市廉价房','landlord',1,NULL,'2025-05-30 09:00:32','2025-05-30 01:00:43'),(19,27,'岳麓区简装一居室','landlord',1,NULL,'2025-05-31 15:18:57','2025-05-31 07:19:18'),(20,28,'sss','landlord',1,NULL,'2025-06-01 15:15:53','2025-06-01 07:16:13');
/*!40000 ALTER TABLE `house_listing_audit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `house_status`
--

DROP TABLE IF EXISTS `house_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `house_status` (
  `house_id` int NOT NULL COMMENT '有一个外键指向house_info表',
  `landlord_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` int NOT NULL COMMENT '0为空置，1为出租中，2为装修中',
  `phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '房屋联系方式',
  `update_time` datetime NOT NULL COMMENT '房屋发布时间（之后状态有变化都更新一次时间）',
  PRIMARY KEY (`house_id` DESC,`landlord_name`) USING BTREE,
  UNIQUE KEY `uq_house_landlord` (`house_id`,`landlord_name`) USING BTREE,
  KEY `house_id` (`house_id`) USING BTREE,
  KEY `landlord_name` (`landlord_name`) USING BTREE,
  CONSTRAINT `house_id` FOREIGN KEY (`house_id`) REFERENCES `house_info` (`house_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `house_status_ibfk_1` FOREIGN KEY (`landlord_name`) REFERENCES `landlord` (`landlord_name`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `house_status`
--

LOCK TABLES `house_status` WRITE;
/*!40000 ALTER TABLE `house_status` DISABLE KEYS */;
INSERT INTO `house_status` VALUES (128,'landlord',0,'13800138000','2025-05-29 11:36:49'),(127,'landlord',0,'13800138000','2025-05-30 11:36:47'),(126,'landlord',0,'13800138000','2025-05-28 11:36:45'),(125,'landlord',0,'13800138000','2025-05-07 11:36:43'),(124,'landlord',0,'13800138000','2025-05-21 11:36:40'),(123,'landlord',0,'13800138000','2025-06-01 11:36:39'),(122,'landlord',0,'13800138000','2025-05-05 11:36:37'),(121,'landlord',0,'13800138000','2025-05-18 11:36:35'),(120,'landlord',0,'13800138000','2025-05-27 11:36:33'),(119,'landlord',0,'13800138000','2025-05-15 11:36:30'),(118,'landlord',0,'13800138000','2025-05-14 11:36:29'),(117,'landlord',0,'13800138000','2025-05-11 11:36:27'),(116,'landlord',0,'13800138000','2025-06-02 11:36:24'),(115,'landlord',0,'13800138000','2025-05-31 11:36:22'),(114,'landlord',0,'13800138000','2025-05-25 11:36:19'),(113,'landlord',0,'13800138000','2025-06-02 11:36:18'),(112,'landlord',0,'13800138000','2025-05-23 11:36:15'),(111,'landlord',0,'13800138000','2025-05-10 11:36:13'),(110,'landlord',0,'13800138000','2025-05-17 11:36:11'),(109,'landlord',0,'13800138000','2025-05-08 11:36:10'),(108,'landlord',0,'13800138000','2025-05-24 11:36:07'),(107,'landlord',0,'13800138000','2025-05-10 11:36:06'),(106,'landlord',0,'13800138000','2025-05-10 11:36:03'),(105,'landlord',0,'13800138000','2025-05-07 11:36:01'),(104,'landlord',0,'13800138000','2025-05-29 11:35:58'),(103,'landlord',0,'13800138000','2025-05-26 11:35:55'),(102,'landlord',0,'13800138000','2025-05-15 11:35:53'),(101,'landlord',0,'13800138000','2025-06-01 11:35:49'),(100,'landlord',0,'13800138000','2025-05-17 11:35:46'),(99,'landlord',0,'13800138000','2025-05-30 11:35:45'),(98,'landlord',0,'13800138000','2025-05-14 11:35:43'),(97,'landlord',0,'13800138000','2025-05-26 11:35:40'),(96,'landlord',0,'13800138000','2025-05-13 11:35:38'),(95,'landlord',0,'13800138000','2025-05-21 11:35:34'),(94,'landlord',0,'13800138000','2025-05-13 11:35:32'),(93,'landlord',0,'13800138000','2025-06-02 11:35:30'),(92,'landlord',0,'13800138000','2025-05-07 11:35:27'),(91,'landlord',0,'13800138000','2025-05-24 11:35:24'),(90,'landlord',0,'13800138000','2025-05-05 11:35:22'),(89,'landlord',0,'13800138000','2025-05-25 11:35:20'),(88,'landlord',0,'13800138000','2025-05-17 11:35:18'),(87,'landlord',0,'13800138000','2025-05-07 11:35:15'),(86,'landlord',0,'13800138000','2025-05-19 11:35:12'),(85,'landlord',0,'13800138000','2025-05-21 11:35:10'),(84,'landlord',0,'13800138000','2025-05-28 11:35:08'),(83,'landlord',0,'13800138000','2025-05-09 11:35:05'),(82,'landlord',0,'13800138000','2025-05-26 11:35:04'),(81,'landlord',0,'13800138000','2025-05-28 11:35:01'),(80,'landlord',0,'13800138000','2025-05-27 11:34:58'),(79,'landlord',0,'13800138000','2025-05-17 11:34:55'),(78,'landlord',0,'13800138000','2025-06-03 11:30:22'),(77,'landlord',0,'13800138000','2025-06-03 11:30:19'),(76,'landlord',0,'13800138000','2025-06-03 11:30:15'),(75,'landlord',0,'13800138000','2025-06-03 11:30:11'),(74,'landlord',0,'13800138000','2025-06-03 11:30:09'),(73,'landlord',0,'13800138000','2025-06-03 11:30:06'),(72,'landlord',0,'13800138000','2025-06-03 11:30:03'),(71,'landlord',0,'13800138000','2025-06-03 11:29:59'),(70,'landlord',0,'13800138000','2025-06-03 11:29:56'),(69,'landlord',0,'13800138000','2025-06-03 11:29:52'),(68,'landlord',0,'13800138000','2025-06-03 11:29:50'),(67,'landlord',0,'13800138000','2025-06-03 11:29:47'),(66,'landlord',0,'13800138000','2025-06-03 11:29:43'),(65,'landlord',0,'13800138000','2025-06-03 11:29:39'),(64,'landlord',0,'13800138000','2025-06-03 11:29:36'),(63,'landlord',0,'13800138000','2025-06-03 11:29:33'),(62,'landlord',0,'13800138000','2025-06-03 11:29:29'),(61,'landlord',0,'13800138000','2025-06-03 11:29:27'),(60,'landlord',0,'13800138000','2025-06-03 11:29:23'),(59,'landlord',0,'13800138000','2025-06-03 11:29:21'),(58,'landlord',0,'13800138000','2025-06-03 11:29:18'),(57,'landlord',0,'13800138000','2025-06-03 11:29:14'),(56,'landlord',0,'13800138000','2025-06-03 11:29:11'),(55,'landlord',0,'13800138000','2025-06-03 11:29:08'),(54,'landlord',0,'13800138000','2025-06-03 11:29:06'),(53,'landlord',0,'13800138000','2025-06-03 11:29:02'),(52,'landlord',0,'13800138000','2025-06-03 11:28:59'),(51,'landlord',0,'13800138000','2025-06-03 11:28:56'),(50,'landlord',0,'13800138000','2025-06-03 11:28:53'),(49,'landlord',0,'13800138000','2025-06-03 11:28:49'),(48,'landlord',0,'13800138000','2025-06-03 11:28:46'),(47,'landlord',0,'13800138000','2025-06-03 11:28:42'),(46,'landlord',0,'13800138000','2025-06-03 11:28:38'),(45,'landlord',0,'13800138000','2025-06-03 11:28:35'),(44,'landlord',0,'13800138000','2025-06-03 11:28:32'),(43,'landlord',0,'13800138000','2025-06-03 11:28:30'),(42,'landlord',0,'13800138000','2025-06-03 11:28:27'),(41,'landlord',0,'13800138000','2025-06-03 11:28:23'),(40,'landlord',0,'13800138000','2025-06-03 11:28:20'),(39,'landlord',0,'13800138000','2025-06-03 11:28:17'),(38,'landlord',0,'13800138000','2025-06-03 11:28:13'),(37,'landlord',0,'13800138000','2025-06-03 11:28:11'),(36,'landlord',0,'13800138000','2025-06-03 11:28:08'),(35,'landlord',0,'13800138000','2025-06-03 11:28:06'),(34,'landlord',0,'13800138000','2025-06-03 11:28:03'),(33,'landlord',0,'13800138000','2025-06-03 11:27:59'),(32,'landlord',0,'13800138000','2025-06-03 11:27:57'),(31,'landlord',0,'13800138000','2025-06-03 11:27:54'),(30,'landlord',0,'13800138000','2025-06-03 11:27:52'),(29,'landlord',0,'13800138000','2025-06-03 11:27:49'),(28,'landlord',1,'13850844558','2025-06-01 15:15:51'),(27,'landlord',1,'13850844558','2025-05-31 15:11:22'),(25,'landlord',0,'13850844558','2025-05-30 09:00:28'),(16,'房东C',0,'12345678910','2025-05-18 21:20:18'),(10,'房东C',0,'13800138002','2025-04-18 09:35:14'),(9,'房东B',0,'13800138001','2025-04-18 09:35:14'),(8,'landlord3',0,'13800138004','2025-05-08 10:08:54');
/*!40000 ALTER TABLE `house_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `landlord`
--

DROP TABLE IF EXISTS `landlord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `landlord` (
  `landlord_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '房东用户名',
  `phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '联系电话，与house_status中的phone一致',
  `addr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '房东住址',
  PRIMARY KEY (`landlord_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `landlord`
--

LOCK TABLES `landlord` WRITE;
/*!40000 ALTER TABLE `landlord` DISABLE KEYS */;
INSERT INTO `landlord` VALUES ('landlord','13800138000','我家'),('landlord3','13800138004','北京市东城区'),('房东B','13800138001','北京市朝阳区'),('房东C','13800138002','北京市海淀区');
/*!40000 ALTER TABLE `landlord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login` (
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `type` int NOT NULL COMMENT '0为管理员，1为租客，2为房东',
  PRIMARY KEY (`username`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES ('admin','$argon2id$v=19$m=65536,t=3,p=4$MVawFIgbHw7qY9+X3T7DOA$UB0rwVIVHJtEeG4IybsxOcgt1pbm6DslD1DxitZuKGE',0),('landlord','$argon2id$v=19$m=65536,t=3,p=4$UKnk0bMwdmSdvd78YzPX5Q$qe2mnLBxrWdA5EDeK+mMijqgn0LvPa/rNMYWHYaLSqQ',2),('landlord3','$argon2id$v=19$m=65536,t=3,p=4$s/J1WI0sGVI/wKpXNS/vMA$VGzc+4OcDfC6I9CI8KNTs2D4k5qYQMH8ke3jWyM4rGM',2),('qwe','$argon2id$v=19$m=65536,t=3,p=4$lXJuuT8BBDKgw+6pi54aBQ$4VcJppJ4cwlLOG/dmHEJ5Mw/qCV4lrBM2WnSRr1cdFo',1),('tenant','$argon2id$v=19$m=65536,t=3,p=4$MVawFIgbHw7qY9+X3T7DOA$UB0rwVIVHJtEeG4IybsxOcgt1pbm6DslD1DxitZuKGE',1),('tenant2','$argon2id$v=19$m=65536,t=3,p=4$MVawFIgbHw7qY9+X3T7DOA$UB0rwVIVHJtEeG4IybsxOcgt1pbm6DslD1DxitZuKGE',1),('wer','$argon2id$v=19$m=65536,t=3,p=4$MVawFIgbHw7qY9+X3T7DOA$UB0rwVIVHJtEeG4IybsxOcgt1pbm6DslD1DxitZuKGE',1),('房东B','$argon2id$v=19$m=65536,t=3,p=4$+Cw6DhNOyNt1sZea9O6P7Q$PZBQF+CCo0kg6Udpq+ZZsAT+KcIPt/t20UBfqog+5P0',2),('房东C','$argon2id$v=19$m=65536,t=3,p=4$pJ4QNDbtTzm5Tvxv3ji0mQ$gt3wdbXgYertf2Pp7Rwc6nR6Q6l9nroGFNMW4QhWtvg',2),('租客A','$argon2id$v=19$m=65536,t=3,p=4$MVawFIgbHw7qY9+X3T7DOA$UB0rwVIVHJtEeG4IybsxOcgt1pbm6DslD1DxitZuKGE',1),('租客C','$argon2id$v=19$m=65536,t=3,p=4$MVawFIgbHw7qY9+X3T7DOA$UB0rwVIVHJtEeG4IybsxOcgt1pbm6DslD1DxitZuKGE',1);
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
  CONSTRAINT `message_ibfk_1` FOREIGN KEY (`receiver_username`) REFERENCES `login` (`username`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `message_ibfk_2` FOREIGN KEY (`channel_id`) REFERENCES `private_channel` (`channel_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `message_ibfk_3` FOREIGN KEY (`sender_username`) REFERENCES `login` (`username`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
INSERT INTO `message` VALUES (40,'landlord','qwe','【租房合同】租期：2025-05-30 至 2026-05-30，金额：¥138264.00。请确认合同信息。','2025-05-30 09:38:07',1,10),(41,'landlord','qwe','【租房合同】租期：2025-05-30 至 2026-05-30，金额：¥138264.00。请确认合同信息。','2025-05-30 09:44:18',1,10),(42,'landlord','qwe','你好','2025-05-31 14:33:10',1,10),(43,'landlord','qwe','是是是','2025-05-31 15:21:18',1,11),(44,'landlord','qwe','对对对','2025-05-31 15:21:24',1,10),(45,'qwe','landlord','搜索','2025-05-31 15:21:32',1,10),(46,'qwe','landlord','搜索','2025-05-31 15:21:36',1,11),(47,'landlord','qwe','【租房合同】租期：2025-05-31 至 2025-08-31，金额：¥6000.00。请确认合同信息。','2025-05-31 15:21:56',1,11),(48,'landlord','qwe','【租房合同已发送】房东已向您发送一份租房合同。月租金：¥1000.00，租期：2025-05-31 至 2026-05-31。请前往“我的合同”查看详情并处理。','2025-05-31 17:46:26',1,11),(49,'landlord','qwe','【租房合同已发送】房东已向您发送一份租房合同草案。\n月租金：¥1000.00，租期：2025-06-01 至 2025-08-01。\n押金：¥3000.00。\n请前往\"查看交易历史\"页面查看详情并进行处理。','2025-06-01 14:24:06',1,11),(50,'landlord','qwe','【租房合同已发送】房东已向您发送一份租房合同草案。\n月租金：¥114444.00，租期：2025-06-01 至 2025-09-01。\n押金：¥11111.00。\n请前往\"查看交易历史\"页面查看详情并进行处理。','2025-06-01 15:26:35',1,12),(51,'landlord','qwe','【租房合同已发送】房东已向您发送一份租房合同草案。\n月租金：¥114444.00，租期：2025-06-01 至 2026-06-01。\n押金：¥11111.00。\n请前往\"查看交易历史\"页面查看详情并进行处理。','2025-06-01 15:27:31',1,12),(52,'landlord','qwe','【租房合同已发送】房东已向您发送一份租房合同草案。\n月租金：¥114444.00，租期：2025-06-19 至 2026-06-19。\n押金：¥11111.00。\n请前往\"查看交易历史\"页面查看详情并进行处理。','2025-06-01 17:49:49',1,12);
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `news`
--

DROP TABLE IF EXISTS `news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `news` (
  `id` int NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL COMMENT '新闻发布时间，注意新闻只能新增，(尽量)不能修改',
  `house_id` int NOT NULL COMMENT '房屋id，有一个指向house_info的外键',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '新闻标题（如某某房屋出租了）,一般配对房屋状态变化',
  `desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '新闻内容',
  `landlord_username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '新闻发布者(房东)',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `house_id` (`house_id`) USING BTREE,
  KEY `landlord_username` (`landlord_username`) USING BTREE,
  CONSTRAINT `news_ibfk_3` FOREIGN KEY (`house_id`) REFERENCES `house_info` (`house_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `news_ibfk_4` FOREIGN KEY (`landlord_username`) REFERENCES `login` (`username`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=126 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news`
--

LOCK TABLES `news` WRITE;
/*!40000 ALTER TABLE `news` DISABLE KEYS */;
INSERT INTO `news` VALUES (1,'2025-04-17 21:08:54',8,'东城区新房源出租','豪华装修，交通便利，欢迎预约看房。',NULL),(4,'2025-04-05 15:30:00',10,'海淀区豪华三居室降价','海淀区豪华三居室价格下调，抓紧机会！',NULL),(5,'2025-04-10 09:00:00',9,'东城区单间出租','东城区单间出租，适合单身人士，交通便利。',NULL),(8,'2025-05-18 21:25:48',16,'上海市好房子特价','无敌优势','房东C'),(12,'2025-05-31 12:53:19',25,'sss','sss','landlord'),(13,'2025-05-31 12:58:57',25,'111','111','landlord'),(20,'2025-05-31 13:08:52',25,'111','111','landlord'),(21,'2025-05-31 13:09:11',25,'12345','12345','landlord'),(26,'2025-06-03 11:27:49',29,'新房源上架：福田区优质房源1号','位于深圳市福田区的3室2厅2卫房源现已上架，月租9947.0元','landlord'),(27,'2025-06-03 11:27:52',30,'新房源上架：海淀区温馨公寓2号','位于北京市海淀区的3室2厅2卫房源现已上架，月租7674.0元','landlord'),(28,'2025-06-03 11:27:54',31,'新房源上架：番禺区舒适家园3号','位于广州市番禺区的3室2厅1卫房源现已上架，月租9816.0元','landlord'),(29,'2025-06-03 11:27:57',32,'新房源上架：福田区现代公寓4号','位于深圳市福田区的5室3厅4卫房源现已上架，月租19189.0元','landlord'),(30,'2025-06-03 11:27:59',33,'新房源上架：朝阳区优质房源5号','位于北京市朝阳区的1室1厅1卫房源现已上架，月租5687.0元','landlord'),(31,'2025-06-03 11:28:03',34,'新房源上架：东城区高端住宅6号','位于北京市东城区的2室2厅1卫房源现已上架，月租5633.0元','landlord'),(32,'2025-06-03 11:28:06',35,'新房源上架：拱墅区豪华住宅7号','位于杭州市拱墅区的4室2厅2卫房源现已上架，月租14574.0元','landlord'),(33,'2025-06-03 11:28:08',36,'新房源上架：建邺区优质房源8号','位于南京市建邺区的5室3厅4卫房源现已上架，月租22096.0元','landlord'),(34,'2025-06-03 11:28:11',37,'新房源上架：西湖区优质房源9号','位于杭州市西湖区的1室1厅1卫房源现已上架，月租2373.0元','landlord'),(35,'2025-06-03 11:28:13',38,'新房源上架：东城区学区房源10号','位于北京市东城区的5室3厅4卫房源现已上架，月租20485.0元','landlord'),(36,'2025-06-03 11:28:17',39,'新房源上架：徐汇区学区房源11号','位于上海市徐汇区的3室2厅2卫房源现已上架，月租9146.0元','landlord'),(37,'2025-06-03 11:28:20',40,'新房源上架：徐汇区学区房源12号','位于上海市徐汇区的2室2厅1卫房源现已上架，月租7868.0元','landlord'),(38,'2025-06-03 11:28:23',41,'新房源上架：海淀区优质房源13号','位于北京市海淀区的2室1厅1卫房源现已上架，月租5854.0元','landlord'),(39,'2025-06-03 11:28:27',42,'新房源上架：南山区舒适家园14号','位于深圳市南山区的3室2厅2卫房源现已上架，月租8493.0元','landlord'),(40,'2025-06-03 11:28:30',43,'新房源上架：黄浦区学区房源15号','位于上海市黄浦区的3室2厅2卫房源现已上架，月租8633.0元','landlord'),(41,'2025-06-03 11:28:32',44,'新房源上架：南山区学区房源16号','位于深圳市南山区的5室3厅4卫房源现已上架，月租19880.0元','landlord'),(42,'2025-06-03 11:28:35',45,'新房源上架：玄武区学区房源17号','位于南京市玄武区的3室2厅2卫房源现已上架，月租8227.0元','landlord'),(43,'2025-06-03 11:28:38',46,'新房源上架：西湖区阳光花园18号','位于杭州市西湖区的1室1厅1卫房源现已上架，月租2994.0元','landlord'),(44,'2025-06-03 11:28:42',47,'新房源上架：东城区精品公寓19号','位于北京市东城区的2室2厅1卫房源现已上架，月租4422.0元','landlord'),(45,'2025-06-03 11:28:46',48,'新房源上架：西湖区阳光花园20号','位于杭州市西湖区的2室1厅1卫房源现已上架，月租4779.0元','landlord'),(46,'2025-06-03 11:28:49',49,'新房源上架：番禺区优质房源21号','位于广州市番禺区的3室2厅2卫房源现已上架，月租8011.0元','landlord'),(47,'2025-06-03 11:28:53',50,'新房源上架：白云区学区房源22号','位于广州市白云区的3室2厅2卫房源现已上架，月租9748.0元','landlord'),(48,'2025-06-03 11:28:56',51,'新房源上架：西城区优质房源23号','位于北京市西城区的1室1厅1卫房源现已上架，月租3916.0元','landlord'),(49,'2025-06-03 11:28:59',52,'新房源上架：黄浦区现代公寓24号','位于上海市黄浦区的2室1厅1卫房源现已上架，月租6439.0元','landlord'),(50,'2025-06-03 11:29:02',53,'新房源上架：白云区温馨公寓25号','位于广州市白云区的1室1厅1卫房源现已上架，月租2137.0元','landlord'),(51,'2025-06-03 11:29:06',54,'新房源上架：玄武区阳光花园26号','位于南京市玄武区的3室2厅1卫房源现已上架，月租6533.0元','landlord'),(52,'2025-06-03 11:29:08',55,'新房源上架：越秀区豪华住宅27号','位于广州市越秀区的4室2厅2卫房源现已上架，月租14762.0元','landlord'),(53,'2025-06-03 11:29:11',56,'新房源上架：黄浦区现代公寓28号','位于上海市黄浦区的2室2厅1卫房源现已上架，月租5262.0元','landlord'),(54,'2025-06-03 11:29:14',57,'新房源上架：徐汇区优质房源29号','位于上海市徐汇区的2室1厅1卫房源现已上架，月租4595.0元','landlord'),(55,'2025-06-03 11:29:18',58,'新房源上架：罗湖区现代公寓30号','位于深圳市罗湖区的4室2厅2卫房源现已上架，月租13995.0元','landlord'),(56,'2025-06-03 11:29:21',59,'新房源上架：福田区现代公寓31号','位于深圳市福田区的3室2厅2卫房源现已上架，月租6929.0元','landlord'),(57,'2025-06-03 11:29:23',60,'新房源上架：宝安区现代公寓32号','位于深圳市宝安区的2室2厅1卫房源现已上架，月租5832.0元','landlord'),(58,'2025-06-03 11:29:27',61,'新房源上架：西湖区优质房源33号','位于杭州市西湖区的1室1厅1卫房源现已上架，月租5510.0元','landlord'),(59,'2025-06-03 11:29:29',62,'新房源上架：宝安区精品公寓34号','位于深圳市宝安区的5室3厅4卫房源现已上架，月租21539.0元','landlord'),(60,'2025-06-03 11:29:33',63,'新房源上架：东城区高端住宅35号','位于北京市东城区的2室2厅1卫房源现已上架，月租4684.0元','landlord'),(61,'2025-06-03 11:29:36',64,'新房源上架：浦东新区便民公寓36号','位于上海市浦东新区的1室1厅1卫房源现已上架，月租5496.0元','landlord'),(62,'2025-06-03 11:29:39',65,'新房源上架：越秀区现代公寓37号','位于广州市越秀区的1室1厅1卫房源现已上架，月租4210.0元','landlord'),(63,'2025-06-03 11:29:43',66,'新房源上架：番禺区温馨公寓38号','位于广州市番禺区的3室2厅2卫房源现已上架，月租8336.0元','landlord'),(64,'2025-06-03 11:29:47',67,'新房源上架：西城区温馨公寓39号','位于北京市西城区的4室2厅2卫房源现已上架，月租14805.0元','landlord'),(65,'2025-06-03 11:29:50',68,'新房源上架：越秀区高端住宅40号','位于广州市越秀区的2室1厅1卫房源现已上架，月租4766.0元','landlord'),(66,'2025-06-03 11:29:52',69,'新房源上架：宝安区现代公寓41号','位于深圳市宝安区的1室1厅1卫房源现已上架，月租3324.0元','landlord'),(67,'2025-06-03 11:29:56',70,'新房源上架：朝阳区精品公寓42号','位于北京市朝阳区的2室1厅1卫房源现已上架，月租6812.0元','landlord'),(68,'2025-06-03 11:29:59',71,'新房源上架：上城区温馨公寓43号','位于杭州市上城区的1室1厅1卫房源现已上架，月租2677.0元','landlord'),(69,'2025-06-03 11:30:03',72,'新房源上架：天河区精品公寓44号','位于广州市天河区的4室2厅2卫房源现已上架，月租12343.0元','landlord'),(70,'2025-06-03 11:30:06',73,'新房源上架：南山区高端住宅45号','位于深圳市南山区的4室2厅2卫房源现已上架，月租12905.0元','landlord'),(71,'2025-06-03 11:30:09',74,'新房源上架：罗湖区精品公寓46号','位于深圳市罗湖区的1室1厅1卫房源现已上架，月租4868.0元','landlord'),(72,'2025-06-03 11:30:11',75,'新房源上架：朝阳区温馨公寓47号','位于北京市朝阳区的3室2厅1卫房源现已上架，月租8977.0元','landlord'),(73,'2025-06-03 11:30:15',76,'新房源上架：白云区精品公寓48号','位于广州市白云区的1室1厅1卫房源现已上架，月租5481.0元','landlord'),(74,'2025-06-03 11:30:19',77,'新房源上架：拱墅区豪华住宅49号','位于杭州市拱墅区的2室2厅1卫房源现已上架，月租4115.0元','landlord'),(75,'2025-06-03 11:30:22',78,'新房源上架：建邺区温馨公寓50号','位于南京市建邺区的2室1厅1卫房源现已上架，月租5926.0元','landlord'),(76,'2025-06-03 01:34:55',79,'优质房源推荐：城阳区典雅庭51号','位于青岛市城阳区的2室2厅1卫房源现已上架，月租3764.0元。地铁站旁，交通便利，欢迎看房！','landlord'),(77,'2025-06-01 02:34:58',80,'优质房源推荐：岳麓区格调府52号','位于长沙市岳麓区的5室4厅3卫房源现已上架，月租17003.0元。周边大学多，文化氛围浓，欢迎看房！','landlord'),(78,'2025-05-31 17:35:01',81,'优质房源推荐：下城区尊贵苑53号','位于杭州市下城区的5室4厅3卫房源现已上架，月租23875.0元。停车位充足，出行方便，欢迎看房！','landlord'),(79,'2025-06-02 21:35:04',82,'热门房源：典雅园54号等您来看','位于青岛市市南区的2室2厅1卫房源现已上架，月租4033.0元。高层建筑，景观好，欢迎看房！','landlord'),(80,'2025-05-31 16:35:05',83,'优质房源推荐：集美区品质城55号','位于厦门市集美区的1室1厅1卫房源现已上架，月租3002.0元。公园旁边，空气清新，欢迎看房！','landlord'),(81,'2025-06-01 11:35:08',84,'精选房源：西城区学区墅56号现已发布','位于北京市西城区的2室1厅1卫房源现已上架，月租5423.0元。独立阳台，采光充足，欢迎看房！','landlord'),(82,'2025-05-31 19:35:10',85,'热门房源：相城区江景阁57号等您来看','位于苏州市相城区的4室3厅2卫房源现已上架，月租14109.0元。楼层好，视野开阔，欢迎看房！','landlord'),(83,'2025-05-31 19:35:12',86,'新房源上架：福田区雅致岸58号','位于深圳市福田区的3室2厅3卫房源现已上架，月租10632.0元。装修精美，拎包入住，欢迎看房！','landlord'),(84,'2025-06-01 21:35:15',87,'新房源上架：宝安区优质里59号','位于深圳市宝安区的2室1厅1卫房源现已上架，月租7011.0元。临近医院，就医方便，欢迎看房！','landlord'),(85,'2025-06-03 08:35:18',88,'优质房源推荐：洪山区雅致居60号','位于武汉市洪山区的2室1厅2卫房源现已上架，月租4217.0元。学区房，教育资源丰富，欢迎看房！','landlord'),(86,'2025-06-02 00:35:20',89,'优质房源推荐：上城区学区台61号','位于杭州市上城区的4室2厅3卫房源现已上架，月租12567.0元。周边大学多，文化氛围浓，欢迎看房！','landlord'),(87,'2025-06-02 05:35:22',90,'精选房源：江北区格调园62号现已发布','位于重庆市江北区的4室2厅2卫房源现已上架，月租10730.0元。独立阳台，采光充足，欢迎看房！','landlord'),(88,'2025-06-03 08:35:24',91,'热门房源：和平区奢华轩63号等您来看','位于天津市和平区的1室1厅2卫房源现已上架，月租3809.0元。地铁站旁，交通便利，欢迎看房！','landlord'),(89,'2025-06-02 23:35:27',92,'优质房源推荐：天河区尊贵居64号','位于广州市天河区的4室3厅2卫房源现已上架，月租14602.0元。独立阳台，采光充足，欢迎看房！','landlord'),(90,'2025-06-02 14:35:30',93,'热门房源：硚口区格调花园65号等您来看','位于武汉市硚口区的2室2厅2卫房源现已上架，月租3745.0元。配套设施完善，欢迎看房！','landlord'),(91,'2025-06-01 17:35:32',94,'精选房源：天心区典雅里66号现已发布','位于长沙市天心区的5室3厅4卫房源现已上架，月租15700.0元。环境优美，绿化好，欢迎看房！','landlord'),(92,'2025-06-01 20:35:34',95,'热门房源：石景山区尊贵公寓67号等您来看','位于北京市石景山区的1室1厅1卫房源现已上架，月租4572.0元。新开发区，未来发展好，欢迎看房！','landlord'),(93,'2025-06-02 19:35:38',96,'精选房源：莲湖区温馨岸68号现已发布','位于西安市莲湖区的5室4厅3卫房源现已上架，月租19621.0元。停车位充足，出行方便，欢迎看房！','landlord'),(94,'2025-06-01 05:35:40',97,'精选房源：大渡口区豪华台69号现已发布','位于重庆市大渡口区的2室1厅2卫房源现已上架，月租5369.0元。地铁站旁，交通便利，欢迎看房！','landlord'),(95,'2025-06-01 16:35:43',98,'精选房源：普陀区静谧住宅70号现已发布','位于上海市普陀区的3室1厅2卫房源现已上架，月租10141.0元。新开发区，未来发展好，欢迎看房！','landlord'),(96,'2025-06-03 07:35:45',99,'精选房源：越秀区优质湾71号现已发布','位于广州市越秀区的4室2厅2卫房源现已上架，月租14261.0元。公园旁边，空气清新，欢迎看房！','landlord'),(97,'2025-06-01 14:35:46',100,'热门房源：姑苏区品质城72号等您来看','位于苏州市姑苏区的3室2厅2卫房源现已上架，月租7740.0元。商务中心，购物便利，欢迎看房！','landlord'),(98,'2025-06-01 17:35:49',101,'精选房源：思明区温馨里73号现已发布','位于厦门市思明区的3室1厅2卫房源现已上架，月租6548.0元。新开发区，未来发展好，欢迎看房！','landlord'),(99,'2025-05-31 11:35:53',102,'精选房源：碑林区舒适住宅74号现已发布','位于西安市碑林区的4室2厅2卫房源现已上架，月租12148.0元。高层建筑，景观好，欢迎看房！','landlord'),(100,'2025-06-02 12:35:55',103,'优质房源推荐：南开区奢华墅75号','位于天津市南开区的3室2厅3卫房源现已上架，月租6519.0元。环境优美，绿化好，欢迎看房！','landlord'),(101,'2025-06-03 08:35:58',104,'精选房源：吴中区品质府76号现已发布','位于苏州市吴中区的1室1厅2卫房源现已上架，月租2807.0元。停车位充足，出行方便，欢迎看房！','landlord'),(102,'2025-06-01 00:36:01',105,'热门房源：思明区江景墅77号等您来看','位于厦门市思明区的1室1厅2卫房源现已上架，月租1582.0元。老城区，生活配套成熟，欢迎看房！','landlord'),(103,'2025-06-02 18:36:03',106,'新房源上架：中山区品质园78号','位于大连市中山区的3室1厅1卫房源现已上架，月租5071.0元。高层建筑，景观好，欢迎看房！','landlord'),(104,'2025-06-01 00:36:06',107,'新房源上架：秦淮区舒适湾79号','位于南京市秦淮区的2室1厅1卫房源现已上架，月租5238.0元。24小时保安，安全放心，欢迎看房！','landlord'),(105,'2025-05-31 16:36:07',108,'精选房源：灞桥区宽敞阁80号现已发布','位于西安市灞桥区的4室3厅2卫房源现已上架，月租12032.0元。社区活动丰富，邻里和谐，欢迎看房！','landlord'),(106,'2025-06-02 22:36:10',109,'热门房源：西岗区典雅苑81号等您来看','位于大连市西岗区的2室2厅1卫房源现已上架，月租4939.0元。24小时保安，安全放心，欢迎看房！','landlord'),(107,'2025-06-01 20:36:11',110,'热门房源：崂山区宽敞台82号等您来看','位于青岛市崂山区的3室2厅2卫房源现已上架，月租6688.0元。商圈中心，生活便利，欢迎看房！','landlord'),(108,'2025-06-01 22:36:13',111,'热门房源：江汉区静谧城83号等您来看','位于武汉市江汉区的1室1厅1卫房源现已上架，月租2115.0元。配套设施完善，欢迎看房！','landlord'),(109,'2025-06-01 21:36:15',112,'新房源上架：南山区花园家园84号','位于深圳市南山区的2室1厅2卫房源现已上架，月租5873.0元。新开发区，未来发展好，欢迎看房！','landlord'),(110,'2025-06-02 04:36:18',113,'新房源上架：武昌区通透墅85号','位于武汉市武昌区的5室4厅3卫房源现已上架，月租20551.0元。高层建筑，景观好，欢迎看房！','landlord'),(111,'2025-06-02 17:36:19',114,'新房源上架：荔湾区私密庭86号','位于广州市荔湾区的3室1厅2卫房源现已上架，月租9964.0元。独立阳台，采光充足，欢迎看房！','landlord'),(112,'2025-06-01 02:36:22',115,'优质房源推荐：吴中区豪华岸87号','位于苏州市吴中区的3室2厅3卫房源现已上架，月租9335.0元。社区活动丰富，邻里和谐，欢迎看房！','landlord'),(113,'2025-06-03 10:36:24',116,'精选房源：思明区雅致公寓88号现已发布','位于厦门市思明区的3室2厅1卫房源现已上架，月租6887.0元。物业管理好，服务周到，欢迎看房！','landlord'),(114,'2025-05-31 12:36:27',117,'优质房源推荐：普陀区豪华庭89号','位于上海市普陀区的4室2厅3卫房源现已上架，月租15957.0元。环境优美，绿化好，欢迎看房！','landlord'),(115,'2025-06-01 09:36:29',118,'新房源上架：江干区静谧住宅90号','位于杭州市江干区的4室3厅2卫房源现已上架，月租13280.0元。楼层好，视野开阔，欢迎看房！','landlord'),(116,'2025-06-02 20:36:35',121,'优质房源推荐：建邺区雅致湾93号','位于南京市建邺区的3室2厅3卫房源现已上架，月租9784.0元。高层建筑，景观好，欢迎看房！','landlord'),(117,'2025-06-03 02:36:37',122,'新房源上架：甘井子区湖景园94号','位于大连市甘井子区的3室2厅2卫房源现已上架，月租5690.0元。学区房，教育资源丰富，欢迎看房！','landlord'),(118,'2025-06-02 21:36:39',123,'热门房源：玄武区典雅阁95号等您来看','位于南京市玄武区的1室1厅2卫房源现已上架，月租5136.0元。物业管理好，服务周到，欢迎看房！','landlord'),(119,'2025-06-02 16:36:40',124,'热门房源：湖里区现代住宅96号等您来看','位于厦门市湖里区的2室2厅1卫房源现已上架，月租5347.0元。独立阳台，采光充足，欢迎看房！','landlord'),(120,'2025-05-31 15:36:43',125,'新房源上架：集美区江景里97号','位于厦门市集美区的2室1厅2卫房源现已上架，月租4434.0元。物业管理好，服务周到，欢迎看房！','landlord'),(121,'2025-06-02 21:36:45',126,'优质房源推荐：河北区优质家园98号','位于天津市河北区的4室2厅2卫房源现已上架，月租12747.0元。老城区，生活配套成熟，欢迎看房！','landlord'),(122,'2025-06-01 00:36:47',127,'优质房源推荐：盐田区私密住宅99号','位于深圳市盐田区的2室1厅1卫房源现已上架，月租7864.0元。公园旁边，空气清新，欢迎看房！','landlord'),(123,'2025-05-31 15:36:49',128,'优质房源推荐：硚口区山景坊100号','位于武汉市硚口区的2室1厅1卫房源现已上架，月租4241.0元。停车位充足，出行方便，欢迎看房！','landlord');
/*!40000 ALTER TABLE `news` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operation_log`
--

DROP TABLE IF EXISTS `operation_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operation_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `user_type` tinyint NOT NULL COMMENT '0 管理员, 1 租客, 2 房东',
  `message` text NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operation_log`
--

LOCK TABLES `operation_log` WRITE;
/*!40000 ALTER TABLE `operation_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `operation_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `private_channel`
--

DROP TABLE IF EXISTS `private_channel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
  CONSTRAINT `private_channel_ibfk_1` FOREIGN KEY (`tenant_username`) REFERENCES `login` (`username`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `private_channel_ibfk_2` FOREIGN KEY (`landlord_username`) REFERENCES `login` (`username`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `private_channel_ibfk_3` FOREIGN KEY (`house_id`) REFERENCES `house_info` (`house_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `private_channel`
--

LOCK TABLES `private_channel` WRITE;
/*!40000 ALTER TABLE `private_channel` DISABLE KEYS */;
INSERT INTO `private_channel` VALUES (2,'qwe','房东C',10,'2025-05-05 08:30:26'),(10,'qwe','landlord',25,'2025-05-30 01:37:51'),(11,'qwe','landlord',27,'2025-05-31 07:19:39'),(12,'qwe','landlord',28,'2025-06-01 07:16:42');
/*!40000 ALTER TABLE `private_channel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rental_contract`
--

DROP TABLE IF EXISTS `rental_contract`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rental_contract` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '订单号，主键',
  `channel_id` int NOT NULL COMMENT '关联的私信频道ID',
  `landlord_username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `tenant_username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `total_amount` decimal(10,2) NOT NULL COMMENT '月租金或其他周期性租金总额',
  `status` int NOT NULL COMMENT '0：待签署, 1：已签署待支付, 2：已取消, 3：已撤销, 4：已支付/合同生效, 5：已到期, 6: 已终止/已归还',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `channel_id` (`channel_id`) USING BTREE,
  CONSTRAINT `rental_contract_ibfk_1` FOREIGN KEY (`channel_id`) REFERENCES `private_channel` (`channel_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rental_contract`
--

LOCK TABLES `rental_contract` WRITE;
/*!40000 ALTER TABLE `rental_contract` DISABLE KEYS */;
INSERT INTO `rental_contract` VALUES (13,10,'landlord','qwe','2025-05-30','2026-05-30',138264.00,1,'2025-05-30 01:44:18','2025-05-30 01:45:32'),(15,11,'landlord','qwe','2025-05-31','2026-05-31',1000.00,2,'2025-05-31 17:46:26','2025-06-01 06:20:30'),(16,11,'landlord','qwe','2025-06-01','2025-08-01',1000.00,4,'2025-06-01 14:24:06','2025-06-01 07:01:33'),(17,12,'landlord','qwe','2025-06-01','2025-09-01',114444.00,2,'2025-06-01 15:26:35','2025-06-01 07:27:05'),(18,12,'landlord','qwe','2025-06-01','2026-06-01',114444.00,3,'2025-06-01 15:27:31','2025-06-01 07:27:42'),(19,11,'landlord','qwe','2025-06-02','2026-06-02',1000.00,3,'2025-06-01 07:39:38','2025-06-01 07:40:17'),(20,11,'landlord','qwe','2025-06-02','2026-06-02',1000.00,3,'2025-06-01 07:39:45','2025-06-01 07:39:50'),(21,11,'landlord','qwe','2025-06-02','2026-06-02',1000.00,3,'2025-06-01 07:39:54','2025-06-01 07:40:14'),(22,11,'landlord','qwe','2025-06-02','2026-06-02',1000.00,3,'2025-06-01 07:39:55','2025-06-01 07:40:11'),(23,11,'landlord','qwe','2025-06-02','2026-06-02',1000.00,3,'2025-06-01 07:39:56','2025-06-01 07:40:08'),(24,11,'landlord','qwe','2025-06-02','2026-06-02',1000.00,3,'2025-06-01 07:39:57','2025-06-01 07:40:04'),(25,12,'landlord','qwe','2025-06-19','2026-06-19',114444.00,1,'2025-06-01 17:49:49','2025-06-01 09:52:01');
/*!40000 ALTER TABLE `rental_contract` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repair_request`
--

DROP TABLE IF EXISTS `repair_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repair_request` (
  `id` int NOT NULL AUTO_INCREMENT,
  `house_id` int NOT NULL COMMENT '关联房屋ID',
  `tenant_username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '租客用户名',
  `landlord_username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '房东用户名',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '维修内容描述',
  `request_time` datetime NOT NULL COMMENT '请求发起时间',
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '维修请求状态',
  `handler_notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '房东处理备注',
  `handled_time` datetime DEFAULT NULL COMMENT '房东处理时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `house_id` (`house_id`) USING BTREE,
  KEY `landlord_username` (`landlord_username`) USING BTREE,
  KEY `tenant_username` (`tenant_username`) USING BTREE,
  CONSTRAINT `repair_request_ibfk_1` FOREIGN KEY (`landlord_username`) REFERENCES `login` (`username`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `repair_request_ibfk_2` FOREIGN KEY (`house_id`) REFERENCES `house_info` (`house_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `repair_request_ibfk_3` FOREIGN KEY (`tenant_username`) REFERENCES `login` (`username`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repair_request`
--

LOCK TABLES `repair_request` WRITE;
/*!40000 ALTER TABLE `repair_request` DISABLE KEYS */;
/*!40000 ALTER TABLE `repair_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tenant`
--

DROP TABLE IF EXISTS `tenant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tenant` (
  `tenant_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '租客用户名',
  `phone` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '联系方式',
  `addr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户住址',
  PRIMARY KEY (`tenant_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tenant`
--

LOCK TABLES `tenant` WRITE;
/*!40000 ALTER TABLE `tenant` DISABLE KEYS */;
INSERT INTO `tenant` VALUES ('qwe','13912345678','1232423'),('tenant2','13800138005','北京市东城区'),('wer','13850844558','湖北省恩施土家族苗族自治州恩施市'),('租客A','13800138003','北京市丰台区'),('租客C','13800138004','北京市东城区');
/*!40000 ALTER TABLE `tenant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_email`
--

DROP TABLE IF EXISTS `user_email`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_email`
--

LOCK TABLES `user_email` WRITE;
/*!40000 ALTER TABLE `user_email` DISABLE KEYS */;
INSERT INTO `user_email` VALUES (1,'1513979779@qq.com','landlord'),(3,'1513979779@qq.com','qwe'),(5,'1513979779@qq.com','tenant2'),(7,'1513979779@qq.com','房东B'),(9,'1513979779@qq.com','租客A'),(2,'3225340736@qq.com','landlord3'),(4,'3225340736@qq.com','tenant'),(8,'3225340736@qq.com','房东C'),(10,'3225340736@qq.com','租客C');
/*!40000 ALTER TABLE `user_email` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visit_stats`
--

DROP TABLE IF EXISTS `visit_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `visit_stats` (
  `id` int NOT NULL AUTO_INCREMENT,
  `visit_date` date NOT NULL,
  `unique_visits` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visit_stats`
--

LOCK TABLES `visit_stats` WRITE;
/*!40000 ALTER TABLE `visit_stats` DISABLE KEYS */;
/*!40000 ALTER TABLE `visit_stats` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-04  9:46:00

-- ================================
-- 租客浏览记录功能 - 简化版
-- ================================

-- 1. 创建浏览记录表
DROP TABLE IF EXISTS `browse_history`;
CREATE TABLE `browse_history` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '浏览记录ID',
  `tenant_username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '租客用户名',
  `house_id` int NOT NULL COMMENT '房源ID',
  `browse_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '浏览时间',
  `browse_count` int NOT NULL DEFAULT 1 COMMENT '浏览次数',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uk_tenant_house` (`tenant_username`, `house_id`) USING BTREE,
  INDEX `idx_tenant_time` (`tenant_username`, `browse_time` DESC) USING BTREE,
  INDEX `idx_house_time` (`house_id`, `browse_time` DESC) USING BTREE,
  CONSTRAINT `browse_history_ibfk_1` FOREIGN KEY (`tenant_username`) REFERENCES `tenant` (`tenant_name`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `browse_history_ibfk_2` FOREIGN KEY (`house_id`) REFERENCES `house_info` (`house_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='租客浏览记录表';

-- 2. 创建房源浏览统计表
DROP TABLE IF EXISTS `house_browse_stats`;
CREATE TABLE `house_browse_stats` (
  `house_id` int NOT NULL COMMENT '房源ID',
  `total_views` int NOT NULL DEFAULT 0 COMMENT '总浏览次数',
  `unique_visitors` int NOT NULL DEFAULT 0 COMMENT '独立访客数',
  `last_viewed` datetime NULL COMMENT '最后浏览时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`house_id`) USING BTREE,
  INDEX `idx_total_views` (`total_views` DESC) USING BTREE,
  CONSTRAINT `house_browse_stats_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `house_info` (`house_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='房源浏览统计表';

-- 3. 创建存储过程：记录租客浏览行为
DELIMITER $$
DROP PROCEDURE IF EXISTS `RecordTenantBrowse`$$
CREATE PROCEDURE `RecordTenantBrowse`(
    IN p_tenant_username VARCHAR(100),
    IN p_house_id INT
)
BEGIN
    DECLARE v_user_type INT DEFAULT 0;
    DECLARE v_existing_count INT DEFAULT 0;
    
    -- 声明异常处理
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;
    
    START TRANSACTION;
    
    -- 验证是否为租客用户
    SELECT type INTO v_user_type 
    FROM login 
    WHERE username = p_tenant_username;
    
    -- 只有租客(type=1)才记录浏览历史
    IF v_user_type = 1 THEN
        
        -- 检查是否已有浏览记录
        SELECT browse_count INTO v_existing_count
        FROM browse_history 
        WHERE tenant_username = p_tenant_username 
          AND house_id = p_house_id;
        
        IF v_existing_count > 0 THEN
            -- 更新现有记录
            UPDATE browse_history 
            SET browse_count = browse_count + 1,
                browse_time = NOW()
            WHERE tenant_username = p_tenant_username 
              AND house_id = p_house_id;
        ELSE
            -- 插入新记录
            INSERT INTO browse_history (tenant_username, house_id, browse_time, browse_count) 
            VALUES (p_tenant_username, p_house_id, NOW(), 1);
        END IF;
        
        -- 更新房源统计
        INSERT INTO house_browse_stats (house_id, total_views, unique_visitors, last_viewed)
        VALUES (p_house_id, 1, 1, NOW())
        ON DUPLICATE KEY UPDATE
            total_views = (
                SELECT SUM(browse_count) 
                FROM browse_history 
                WHERE house_id = p_house_id
            ),
            unique_visitors = (
                SELECT COUNT(DISTINCT tenant_username) 
                FROM browse_history 
                WHERE house_id = p_house_id
            ),
            last_viewed = NOW();
            
    END IF;
    
    COMMIT;
END$$
DELIMITER ;

-- 4. 创建查询浏览记录的存储过程（修复版）
DELIMITER $$
DROP PROCEDURE IF EXISTS `GetTenantBrowseHistory`$$
CREATE PROCEDURE `GetTenantBrowseHistory`(
    IN p_tenant_username VARCHAR(100),
    IN p_limit INT
)
BEGIN
    -- 如果没有传入限制数，默认为20
    IF p_limit IS NULL OR p_limit <= 0 THEN
        SET p_limit = 20;
    END IF;
    
    SELECT 
        bh.id,
        bh.house_id,
        hi.house_name,
        hi.region,
        hi.addr,
        hi.price,
        hi.rooms,
        hi.image,
        bh.browse_time,
        bh.browse_count,
        hs.status as house_status,
        CASE 
            WHEN hs.status = 0 THEN '可租'
            WHEN hs.status = 1 THEN '已租'
            WHEN hs.status = 2 THEN '维护中'
            ELSE '未知'
        END as status_text
    FROM browse_history bh
    JOIN house_info hi ON bh.house_id = hi.house_id
    LEFT JOIN house_status hs ON bh.house_id = hs.house_id
    WHERE bh.tenant_username = p_tenant_username
    ORDER BY bh.browse_time DESC
    LIMIT p_limit;
END$$

DROP PROCEDURE IF EXISTS `GetPopularHouses`$$
CREATE PROCEDURE `GetPopularHouses`(
    IN p_limit INT
)
BEGIN
    -- 如果没有传入限制数，默认为10
    IF p_limit IS NULL OR p_limit <= 0 THEN
        SET p_limit = 10;
    END IF;
    
    SELECT 
        hbs.house_id,
        hi.house_name,
        hi.region,
        hi.addr,
        hi.price,
        hi.rooms,
        hi.image,
        hbs.total_views,
        hbs.unique_visitors,
        hbs.last_viewed,
        hs.status
    FROM house_browse_stats hbs
    JOIN house_info hi ON hbs.house_id = hi.house_id
    LEFT JOIN house_status hs ON hbs.house_id = hs.house_id
    WHERE hs.status = 0  -- 只显示可租房源
    ORDER BY hbs.total_views DESC, hbs.unique_visitors DESC
    LIMIT p_limit;
END$$

DROP PROCEDURE IF EXISTS `CleanOldBrowseHistory`$$
CREATE PROCEDURE `CleanOldBrowseHistory`(
    IN p_days INT
)
BEGIN
    -- 如果没有传入天数，默认为90天
    IF p_days IS NULL OR p_days <= 0 THEN
        SET p_days = 90;
    END IF;
    
    -- 删除指定天数前的浏览记录
    DELETE FROM browse_history 
    WHERE browse_time < DATE_SUB(NOW(), INTERVAL p_days DAY);
    
    -- 重新计算统计数据
    UPDATE house_browse_stats hbs
    SET total_views = (
        SELECT IFNULL(SUM(browse_count), 0) 
        FROM browse_history bh 
        WHERE bh.house_id = hbs.house_id
    ),
    unique_visitors = (
        SELECT COUNT(DISTINCT tenant_username) 
        FROM browse_history bh 
        WHERE bh.house_id = hbs.house_id
    );
    
    -- 删除没有浏览记录的统计数据
    DELETE FROM house_browse_stats 
    WHERE total_views = 0;
END$$
DELIMITER ;

-- 6. 创建定时清理事件（可选）
SET GLOBAL event_scheduler = ON;

DROP EVENT IF EXISTS `CleanBrowseHistoryEvent`;
CREATE EVENT `CleanBrowseHistoryEvent`
ON SCHEDULE EVERY 1 WEEK
DO
  CALL CleanOldBrowseHistory(90);

-- 7. 创建视图：热门房源排行
CREATE OR REPLACE VIEW `v_popular_houses` AS
SELECT 
    hi.house_id,
    hi.house_name,
    hi.region,
    hi.addr,
    hi.price,
    hi.rooms,
    hi.image,
    IFNULL(hbs.total_views, 0) as total_views,
    IFNULL(hbs.unique_visitors, 0) as unique_visitors,
    hbs.last_viewed,
    hs.status,
    CASE 
        WHEN hs.status = 0 THEN '可租'
        WHEN hs.status = 1 THEN '已租'
        WHEN hs.status = 2 THEN '维护中'
        ELSE '未知'
    END as status_text
FROM house_info hi
LEFT JOIN house_browse_stats hbs ON hi.house_id = hbs.house_id
LEFT JOIN house_status hs ON hi.house_id = hs.house_id
WHERE hs.status = 0  -- 只显示可租房源
ORDER BY hbs.total_views DESC, hbs.unique_visitors DESC;

-- ================================
-- 使用说明和调用示例
-- ================================

/*
-- 1. 记录浏览行为（在应用层调用）
CALL RecordTenantBrowse('qwe', 28);

-- 2. 获取租客浏览历史
CALL GetTenantBrowseHistory('qwe', 10);

-- 3. 获取热门房源
CALL GetPopularHouses(10);

-- 4. 查看热门房源视图
SELECT * FROM v_popular_houses LIMIT 10;

-- 5. 清理过期浏览记录
CALL CleanOldBrowseHistory(90);
*/

-- 8. 插入示例数据
INSERT INTO browse_history (tenant_username, house_id, browse_time, browse_count) VALUES
('qwe', 28, NOW(), 1),
('qwe', 27, DATE_SUB(NOW(), INTERVAL 1 DAY), 2),
('qwe', 25, DATE_SUB(NOW(), INTERVAL 2 DAY), 1);

-- 更新统计数据
CALL RecordTenantBrowse('qwe', 28);
CALL RecordTenantBrowse('qwe', 27);
CALL RecordTenantBrowse('qwe', 25);
