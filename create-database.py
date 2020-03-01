from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'acc_league'

TABLES = {}
TABLES['teams'] = (
    "CREATE TABLE `teams` ("
    "  `team_id` varchar(20) NOT NULL,"
    "  `team_name` varchar(16) NOT NULL,"
    "  `matches_won` int(4) NOT NULL,"
    "  `matches_lost` int(4) NOT NULL,"
    "  PRIMARY KEY (`team_id`), UNIQUE KEY `team_name` (`team_name`)"
    ") ENGINE=InnoDB")

TABLES['matches'] = (
    "CREATE TABLE `matches` ("
    "  `match_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `match_date` date NOT NULL,"
    "  `blue_team_id` varchar(20) NOT NULL,"
    "  `orange_team_id` varchar(20) NOT NULL,"
    "  `blue_team_score` int(2) NOT NULL,"
    "  `orange_team_score` int(2) NOT NULL,"
    "  `winner_id` varchar(20) NOT NULL,"
    "  PRIMARY KEY (`match_id`),"
    "  CONSTRAINT `matches_tmfk_1` FOREIGN KEY (`blue_team_id`) "
    "     REFERENCES `teams` (`team_id`)"
    "  CONSTRAINT `matches_tmfk_2` FOREIGN KEY (`orange_team_id`) "
    "     REFERENCES `teams` (`team_id`)"
    "  CONSTRAINT `matches_tmfk_3` FOREIGN KEY (`winner_id`) "
    "     REFERENCES `teams` (`team_id`)"
    ") ENGINE=InnoDB")

cnx = mysql.connector.connect(user='', password='')
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()
