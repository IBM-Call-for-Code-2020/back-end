# back-end
Back-end of Team Ithaca in IBM Call-For-Code Global 2020

# Carbon Tax Bot Url (Front-End using AI and Blockchain)
https://ibm.pinot.studio/chat

# IBM Watson Assistant Apply (IBM Service)
https://web-chat.global.assistant.watson.cloud.ibm.com/preview.html?region=au-syd&integrationID=ade5378b-18c8-4579-9e3c-a1d1e756dc86&serviceInstanceID=45e4a82e-f647-4a5c-866b-69fae0086057

# IoT Device Technology
- Development Environment : Arduino IDE  
- Iot Device Board : Arduino UNO R3  
- Co Measure Sensor : MQ-7  

# BlockChain block explorer Url
https://baobab.scope.klaytn.com/account/0xa87C2C7C63d407D9f7A9b634aF75378FB6D2Aab1?tabId=txList

# Web Platform Url (The Carbon Tax Web Platform)
https://co2bot.run.goorm.io/

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
