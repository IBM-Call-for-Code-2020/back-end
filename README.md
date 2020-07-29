# back-end
Back-end of Team Ithaca in IBM Call-For-Code Global 2020

# Carbon Tax Bot Url
https://ibm.pinot.studio/chat

# Web Platform Url
https://co2bot.run.goorm.io/

# BlockChain block explorer Url
https://baobab.scope.klaytn.com/account/0xa87C2C7C63d407D9f7A9b634aF75378FB6D2Aab1?tabId=txList


# DB Table
CREATE TABLE `USER_INFO` (
  `Idx` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `Userid` varchar(50) NOT NULL,
  `UserType` varchar(20) NOT NULL,
  `UserName` varchar(50) DEFAULT NULL,
  `Continent` varchar(50) DEFAULT NULL,
  `Country` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Idx`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

CREATE TABLE `CARBON_LOG` (
  `Idx` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `Userid` varchar(32) NOT NULL,
  `Amount` int(11) NOT NULL,
  `Insert_Dt` datetime DEFAULT NULL,
  PRIMARY KEY (`Idx`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8;

CREATE TABLE `PENALTY_INFO` (
  `Idx` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `Userid` varchar(50) NOT NULL,
  `Insert_Dt` datetime DEFAULT NULL,
  `Remarks` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Idx`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
