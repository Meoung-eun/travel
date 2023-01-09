-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: jejudo
-- ------------------------------------------------------
-- Server version	8.0.18

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
-- Table structure for table `tour`
--

DROP TABLE IF EXISTS `tour`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tour` (
  `area` text,
  `indoor(out)` text,
  `tour_site` text,
  `explain` text,
  `elec_charger` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tour`
--

LOCK TABLES `tour` WRITE;
/*!40000 ALTER TABLE `tour` DISABLE KEYS */;
INSERT INTO `tour` VALUES ('성산','실내','만장굴','춥다고 느낄정도로 시원하며 작은 석순과 유석을 볼 수 있어 멋있습니다.','x'),('성산','실내','아쿠아플라넷',' 다양한 물고기들이 있고 상어와 가오리가 지나가는 걸 꼭 보세요.','o'),('성산','실외','비자림','안개가 몽환적이며 색다른 분위기와 피톤치드 공기를 마실 수 있습니다.','o'),('성산','실외','성산일출봉',' 제주의 명소 중 대표적인 랜드마크이며 풍광과 아름다운 경치를 볼 수 있습니다.','o'),('성산','실외','섭지코지',' 성산일출봉 풍경을 바라볼 수 있고 자연경관이 좋고 산책하기 좋습니다.','o'),('고산','실내','아르떼뮤지엄',' 현대영상기술로 인한 시각적으로 풍부한 경험을 할 수 있습니다.','x'),('고산','실내','피규어뮤지엄','액션피규어와 실물크기의 영화캐릭터들의 대형 피규어가 있습니다.','o'),('고산','실내','오설록 티 뮤지엄',' 녹차밭을 구경할 수 있고 다양한 먹거리가 있습니다.','x'),('고산','실내','애월더선셋카페','애월해수욕장이 보여서 힐링할 수있는 공간입니다.','x'),('고산','실외','금악오름','연못을 품은 신비로운 서쪽 언덕입니다.','x'),('서귀포','실내','테디베어박물관',' 아이가 있다면 추천하며 움직이고 소리나는 인형들을 구경할 수 있습니다.','o'),('서귀포','실내','더클리프 카페',' 즐거운 음악과 함께 해변을 바라볼 수 있는 곳입니다.','x'),('서귀포','실외','요트투어','더운여름에 요트로 바다를 달려보세요. 시원하고 힐링할 수 있습니다.','x'),('서귀포','실외','카멜리아힐',' 사계절 내내 예쁜 식물들과 꽃을 볼 수있고 산책하기 좋은 곳입니다.','x'),('서귀포','실외','용머리해안',' 물때에 맞춰 가야하며 풍화작용으로 깎여나간 절벽과 부서지는 파도소리는 예술입니다.','x'),('제주','실내','사진놀이터',' 다양한 사진들을 찍을 수 있는 멋진 공간입니다.','x'),('제주','실내','모이소',' 없는 거 빼고 다 있는 제주도 소품샵입니다.','x'),('제주','실내','델문도카페',' 함덕해수욕장이 눈앞에 있고 인증샷을 건질 수 있습니다.','x'),('제주','실내','피규어 뮤지엄',' 마블 / 디씨 / 디즈니 등 다양한 히어로 피규어를 볼 수 있습니다.','x'),('제주','실외','한라수목원',' 공항근처이며 가볍게 산책하기 좋습니다.','o'),('제주','실외','한담해안산책로',' 제주의 매력이 보이는 해안산책로입니다.','x');
/*!40000 ALTER TABLE `tour` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-01-09 19:04:45
