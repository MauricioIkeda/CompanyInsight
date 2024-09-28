-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: projetounimar
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `positivo`
--

DROP TABLE IF EXISTS `positivo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `positivo` (
  `idPositivo` int NOT NULL AUTO_INCREMENT,
  `titulo_reclamacao` varchar(100) DEFAULT NULL,
  `reclamacao` varchar(3000) DEFAULT NULL,
  `local_reclamacao` varchar(125) DEFAULT NULL,
  `data_reclamacao` varchar(125) DEFAULT NULL,
  `status_reclamacao` varchar(15) DEFAULT NULL,
  `produto_reclamado` varchar(125) DEFAULT NULL,
  `motivo_reclamado` varchar(3000) DEFAULT NULL,
  PRIMARY KEY (`idPositivo`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `positivo`
--

LOCK TABLES `positivo` WRITE;
/*!40000 ALTER TABLE `positivo` DISABLE KEYS */;
INSERT INTO `positivo` VALUES (51,'Smart Lâmpada piscando do nada','Comprei a minha smart lâmpada há pouco tempo pela amazon e ela não para de piscar do nada! Eu quase nem fico no meu quarto para ter queimado a luz e posso garantir que o meu wi-fi não é, pois ela não estava assim,  Foi bem cara, pois comprei o kit com o controle de casa da positivo, espero que vocês resolvam o meu problema.','São Paulo - SP','25/09/2024 às 19:38','Não respondida','lâmpada','None'),(52,'CELULAR COM DEFEITO','Ja mandei mandei o cel para voces e não adiantou de nada não irei manda novamente voces não resolve meu problema quero o valor do celular porque fica nesse tempo sem celular e eu que fico no prejuizo espero que voces resolva o meu problema','Santo Anastácio - SP','25/09/2024 às 15:49','Não respondida','lâmpada','None'),(53,'Lâmpada plw91 Positivo ligando sozinha','É a segunda lâmpada plw91 Positivo que possuo que fica ligando sozinha, e reseta como tivesse sido programada pra isso. A primeira descartei, mas não dá pra ficar jogando dinheiro fora dessa forma. Já procurei soluções, mas vi que outros tem o mesmo problema, e ninguém encontro solução, o que me faz acreditar em defeito de fábrica.','Rio de Janeiro - RJ','25/09/2024 às 12:10','Não respondida','lâmpada','fica ligando sozinha'),(54,'NOTEBOOK 6 MESES NAO FUNCIONA - 30 DIAS PARA CONSERTAR NA GARANTIA','Comprei um NOTEBOOK POSITIVO no dia 30/01/2024 nas LOJA LEBES, expliquei para qual uso seria, os programas que eu usava e qual minha demanda diária. Informei que trabalhaba home office, que precisava do notebook para uma demanda intensa e diária. Comprei um produto de valor mediano, nao era da promoção, nao era o ultimo da loja, nao é nada de graça, comprei este pois fui indicada pelo vendedor, que o produto sararia minhas necessidades. Após 6 meses de uso, o notebook apresenta diversos travamentos, lentidos, nao consigo acesso mais de uma pagina de navegador por vez, tranca e desliga, trava todo e não funciona. Por inumeras vezes passei vergonha em reuniões online, com diversas pessoas de outras Estados, pois nao conseguia apresentar minhas projeções por contra do travamento do notebook. Fui excluida de reuniões gerenciais do cliente a qual represento, por nao conseguir mostrar meus resultados, devido ao travamento do notebook. Ao solicitar a garantia, fui informada que levaria a partir de 30 dias para o conserto, que o produto deveria ser enviado por Correios e etc. A Garantia e atendimento da Positivo nao me deu nenhum auxilio a mais. Se eu trabalho home office, o notebook é meu equipamento primordial de trabalho, como vou ficar 30 dias sem ele? Como vou ficar sem trabalhar 30 dias? Ainda estou pagando o produto, se eu ficar desempregada, pq se eu ficar 30 dias sem trabalhar, eu vou ficar desempregada, como vou pagar o que devo?','Torres - RS','25/09/2024 às 11:13','Não respondida','notebook','apresenta diversos travamentos'),(55,'Lâmpada inteligente da Positivo não fica mais na cor branca','Comprei uma lâmpada inteligente da Positivo e, recentemente, ela parou de funcionar corretamente. Quando tento configurá-la para ficar na cor branca, seja pelo comando de voz via Alexa ou diretamente pelo aplicativo da Positivo, a lâmpada não responde e permanece em outras cores. Já tentei diversas vezes redefinir as configurações, mas o problema persiste. Espero que a Positivo ofereça uma solução rápida para esse defeito, pois a funcionalidade principal da lâmpada está comprometida.','Jundiaí - SP','25/09/2024 às 10:20','Não respondida','lâmpada','ela parou de funcionar corretamente. Quando tento configurá-la para ficar na cor branca, seja pelo comando de voz via Alexa ou diretamente pelo aplicativo'),(56,'Notebook defeituoso','Eu comprei um Notebook positivo vision em 09/05 para o meu pai de 87 anos, ele apresentou problema e foi enviado para manutenção dia 11/06, recebi uma máquina nova dia 17/07, voltamos a utilizar a máquina agora no início de agosto e ela deu o mesmo defeito pelo qual foi substituído. Meu pai só utiliza o notebook para acessar o YouTube e ver e-mails.  Estou frustrada e insatisfeita com o produto.  Quero a devolução do meu dinheiro. Aguardo solução rápida.','Rio de Janeiro - RJ','25/09/2024 às 09:42','Não respondida','notebook','None'),(57,'Lâmpada Smart Wifi parou de funcionar, não liga mais !','Comprei a Lâmpada pela Amazon na loja oficial da Positivo no dia 31/04/24, então não tem nem 6 meses de uso.. A lâmpada funcionava perfeitamente, gostava muito por sinal, mas nos últimos 3 dias a lâmpada começou a apresentar alguns problemas como ligar sozinha em horários aleatórios, eu mesmo acordei em algumas madrugadas por conta dela acender enquanto dormia.. Ontem (24/09) aconteceu de ela acender de madrugada novamente, porém reiniciei aos padrões de fábrica a aparentemente tinha sido resolvido, ela funcionou ao longo do dia e por volta da noite quando estava indo dormir a luz voltou a acender sem o meu comando, tentei reiniciar novamente e ela começou a piscar sem padrão algum, mandava apagar e ela ficava por 30 segundos apagada e voltava a acender e piscar, alterar o brilho sem algum padrão evidente.. Desliguei pelo interruptor e retirei a Lâmpada, ela estava bem quente, até estranhei, por conta disso decidi esperar a noite passar para tentar configurar novamente no dia seguinte (25/09), porém para minha triste notícia a Lâmpada não liga mais, como faz menos de 6 meses de uso, gostaria de acionar a garantia ou de algum suporte que me ajude a resolver o problema','Orlândia - SP','25/09/2024 às 04:10','Resolvido','lâmpada','começou a apresentar alguns problemas como ligar sozinha em horários aleatórios'),(58,'Smart plug parou de funcionar','Olá, tenho um plug da positivo que até hoje de tarde estava funcionando. Agora, pela noite, ele não parou de acender a luz do led e não passa mais a energia. Já tentei em outras tomadas e com outros equipamentos, mas não resolve, é o dispositivo mesmo.','Uberlândia - MG','25/09/2024 às 01:53','Não respondida','lâmpada','não passa mais a energia.'),(59,'Equipamento voltou da garantia com o mesmo defeito','Comprei um tablet da marca VAIO tl10. Necessitei acionar a garantia pois o produto apresentou defeito no sistema operacional e na conexão com o teclado físico. O aparelho retornou da assistência ainda com o mesmo defeito: sem conexão com o teclado físico e com problema no sistema operacional. Não mexeram em nada no produto. Foi e voltou com o mesmo defeito. Não fizeram absolutamente nd. Nem ao mesmo resetaram o aparelho como o próprio procedimento padrão que fora informado que realizam. Completo descaso e desrespeito com o cliente. Meu produto ainda está na garantia. Quero um novo.','Mário Campos - MG','24/09/2024 às 19:13','Respondida','tablet','None');
/*!40000 ALTER TABLE `positivo` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-27 22:30:44
