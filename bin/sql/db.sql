CREATE TABLE `mercati` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `sigla` varchar(40) DEFAULT NULL,
  `nome` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `stock` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `sigla` varchar(40) DEFAULT NULL,
  `nome` varchar(60) DEFAULT NULL,
  `mercato` int NOT NULL,
  `bookvalue` float DEFAULT NULL,
  `targetlowprice` float DEFAULT NULL,
  `targetmedianprice` float DEFAULT NULL,
  `targetmeanprice` float DEFAULT NULL,
  `targethighprice` float DEFAULT NULL,
  `trailingeps` float DEFAULT NULL,
  `forwardeps` float DEFAULT NULL,
  `dividendrate` float DEFAULT NULL,
  `currentprice` float DEFAULT NULL,
  `returnonequity` float DEFAULT NULL,
  `pegratio` float DEFAULT NULL,
  `revenuegrowth` float DEFAULT NULL,
  `revenuequarterlygrowth` float DEFAULT NULL,
  `earningsgrowth` float DEFAULT NULL,
  `earningsquarterlygrowth` float DEFAULT NULL,
  `trailingpe` float DEFAULT NULL,
  `forwardpe` float DEFAULT NULL,
  `upd_datetime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `stock_history` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `sigla` varchar(40) DEFAULT NULL,
  `nome` varchar(60) DEFAULT NULL,
  `mercato` int NOT NULL,
  `bookvalue` float DEFAULT NULL,
  `targetlowprice` float DEFAULT NULL,
  `targetmedianprice` float DEFAULT NULL,
  `targetmeanprice` float DEFAULT NULL,
  `targethighprice` float DEFAULT NULL,
  `trailingeps` float DEFAULT NULL,
  `forwardeps` float DEFAULT NULL,
  `dividendrate` float DEFAULT NULL,
  `currentprice` float DEFAULT NULL,
  `returnonequity` float DEFAULT NULL,
  `pegratio` float DEFAULT NULL,
  `revenuegrowth` float DEFAULT NULL,
  `revenuequarterlygrowth` float DEFAULT NULL,
  `earningsgrowth` float DEFAULT NULL,
  `earningsquarterlygrowth` float DEFAULT NULL,
  `trailingpe` float DEFAULT NULL,
  `forwardpe` float DEFAULT NULL,
  `hit_datetime` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
