import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  allow_local_infile = True
)

mycursor = mydb.cursor()
mycursor.execute("DROP DATABASE IF EXISTS energy")
mycursor.execute("CREATE DATABASE energy")

energy = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="energy",
  allow_local_infile = True

)

mycursor = energy.cursor()

sql_query = "CREATE TABLE `ActualTotalLoad` (`Id` int(11) NOT NULL AUTO_INCREMENT,"
sql_query += "`EntityCreatedAt` DATETIME NOT NULL,"
sql_query +=  "`EntityModifiedAt` DATETIME NOT NULL,"
sql_query +=  "`ActionTaskID` int(11) NOT NULL,"
sql_query +=  "`Status` varchar(255) DEFAULT NULL,"
sql_query +=  "`Year` int(11) NOT NULL,"
sql_query +=  "`Month` int(11) NOT NULL,"
sql_query +=  "`Day` int(11) NOT NULL,"
sql_query +=  "`DateTime` datetime NOT NULL,"
sql_query +=  "`AreaName` varchar(255) NOT NULL,"
sql_query +=  "`UpdateTime` datetime NOT NULL,"
sql_query +=  "`TotalLoadValue` decimal(10,2) DEFAULT NULL,"
sql_query +=  "`AreaTypeCodeId` int(11) NOT NULL,"
sql_query +=  "`AreaCodeId` int(11) NOT NULL,"
sql_query +=  "`ResolutionCodeId` int(11) NOT NULL,"
sql_query +=  "`MapCodeId` int(11) NOT NULL,"
sql_query +=  "`RowHash` varchar(255) DEFAULT NULL,"
sql_query +=  "PRIMARY KEY (`Id`)"
sql_query += ") ENGINE=InnoDB AUTO_INCREMENT=5068442 DEFAULT CHARSET=latin1;"

mycursor.execute(sql_query)

sql_query = "CREATE TABLE `AggregatedGenerationPerType` ("
sql_query += "`Id` int(11) NOT NULL AUTO_INCREMENT,"
sql_query += "`EntityCreatedAt` TIMESTAMP,"
sql_query += "`EntityModifiedAt` DATETIME NOT NULL,"
sql_query += "`ActionTaskID` int(11) NOT NULL,"
sql_query += "`Status` varchar(255) DEFAULT NULL,"
sql_query += "`Year` int(11) NOT NULL,"
sql_query += "`Month` int(11) NOT NULL,"
sql_query += "`Day` int(11) NOT NULL,"
sql_query += "`DateTime` datetime NOT NULL,"
sql_query += "`AreaName` varchar(255) DEFAULT NULL,"
sql_query += "`UpdateTime` datetime NOT NULL,"
sql_query += "`ActualGenerationOutput` decimal(10,2) DEFAULT NULL,"
sql_query += "`ActualConsumption` decimal(10,2) DEFAULT NULL,"
sql_query += "`AreaTypeCodeId` int(11) NOT NULL,"
sql_query += "`AreaCodeId` int(11) NOT NULL,"
sql_query += "`ResolutionCodeId` int(11) NOT NULL,"
sql_query += "`MapCodeId` int(11) NOT NULL,"
sql_query += "`ProductionTypeId` int(11) NOT NULL,"
sql_query += "`RowHash` varchar(255) DEFAULT NULL,"
sql_query += "PRIMARY KEY (`Id`)"
sql_query += ") ENGINE=InnoDB AUTO_INCREMENT=832887359 DEFAULT CHARSET=latin1;"

mycursor.execute(sql_query)

sql_query = "CREATE TABLE `DayAheadTotalLoadForecast` ("
sql_query += "`Id` int(11) NOT NULL AUTO_INCREMENT,"
sql_query += "`EntityCreatedAt` TIMESTAMP,"
sql_query += "`EntityModifiedAt` DATETIME NOT NULL,"
sql_query += "`ActionTaskID` int(11) NOT NULL,"
sql_query += "`Status` varchar(255) DEFAULT NULL,"
sql_query += "`Year` int(11) NOT NULL,"
sql_query += "`Month` int(11) NOT NULL,"
sql_query += "`Day` int(11) NOT NULL,"
sql_query += "`DateTime` datetime NOT NULL,"
sql_query += "`AreaName` varchar(255) DEFAULT NULL,"
sql_query += "`UpdateTime` datetime NOT NULL,"
sql_query += "`TotalLoadValue` decimal(10,2) DEFAULT NULL,"
sql_query += "`AreaTypeCodeId` int(11) NOT NULL,"
sql_query += "`AreaCodeId` int(11) NOT NULL,"
sql_query += "`ResolutionCodeId` int(11) NOT NULL,"
sql_query += "`MapCodeId` int(11) NOT NULL,"
sql_query += "`RowHash` varchar(255) DEFAULT NULL,"
sql_query += "PRIMARY KEY (`Id`)"
sql_query += ") ENGINE=InnoDB AUTO_INCREMENT=33724211 DEFAULT CHARSET=latin1;"

mycursor.execute(sql_query)


sql_query = "CREATE TABLE `users` (`username` varchar(100) NOT NULL,`email` varchar(100) NOT NULL,`password` varchar(100) NOT NULL, `apikey` varchar(14) NOT NULL, `total_quota` int(11), `remaining_quota` int(11), `admin` BOOLEAN, UNIQUE(`email`, `apikey`), UNIQUE KEY `username` (`username`)) ENGINE=MyISAM DEFAULT CHARSET=utf8;"

mycursor.execute(sql_query)

sql_query = "INSERT INTO users (username, email, apikey, total_quota, remaining_quota, password, admin) VALUES ('admin', 'admin@admin.com', '1111-1111-1111', 1000, 1000, 'nimda123', True)"
mycursor.execute(sql_query)

#Here load the data into the database 
#Change the path so mysql can find the csv files


mycursor.execute("LOCK TABLES `ActualTotalLoad` WRITE;")
sql_query = 'LOAD DATA LOCAL INFILE "../tendays/ActualTotalLoad-10days.csv"'
sql_query += "INTO TABLE ActualTotalLoad "
sql_query += "FIELDS TERMINATED BY ';'"
sql_query += "LINES TERMINATED BY '\\n'"
sql_query += "IGNORE 1 ROWS"

mycursor.execute(sql_query)
mycursor.execute("UNLOCK TABLES")

mycursor.execute("LOCK TABLES `AggregatedGenerationPerType` WRITE;")
sql_query = 'LOAD DATA LOCAL INFILE "../tendays/AggregatedGenerationPerType-10days.csv"'
sql_query += "INTO TABLE AggregatedGenerationPerType "
sql_query += "FIELDS TERMINATED BY ';'"
sql_query += "LINES TERMINATED BY '\\n'"
sql_query += "IGNORE 1 ROWS"

mycursor.execute(sql_query)
mycursor.execute("UNLOCK TABLES")

mycursor.execute("LOCK TABLES `DayAheadTotalLoadForecast` WRITE;")
sql_query = 'LOAD DATA LOCAL INFILE "../tendays/DayAheadTotalLoadForecast-10days.csv"' 
sql_query += "INTO TABLE DayAheadTotalLoadForecast "
sql_query += "FIELDS TERMINATED BY ';'"
sql_query += "LINES TERMINATED BY '\\n'"
sql_query += "IGNORE 1 ROWS"

mycursor.execute(sql_query)
mycursor.execute("UNLOCK TABLES")
