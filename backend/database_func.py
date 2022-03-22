import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'PANDAS_UI'
TABLES = {}
TABLES['files'] = (
    "CREATE TABLE `files` ("
    "   `file_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `file_name` varchar(255) NOT NULL UNIQUE,"
    "   `version` int(11) NOT NULL,"
    "   PRIMARY KEY (`file_id`))"
)
TABLES['files_version'] = (
    "CREATE TABLE `files_version` ("
    "   `file_version_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `file_id` int(11) NOT NULL,"
    "   `file_version` int(11) NOT NULL,"
    "   `pandas_function` varchar(255) NOT NULL,"
    "   PRIMARY KEY (`file_version_id`),"
    "   FOREIGN KEY (`file_id`) REFERENCES files (`file_id`))"
)

query_insert_file =         ("INSERT INTO files (file_name, version) VALUES (%s, %s)")

query_insert_file_version = ("INSERT INTO files_version (file_id, file_version, pandas_function) VALUES (%s, %s, %s)")

def insert_file(file_name):
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="PANDAS_UI"
    )
    cursor = mydb.cursor()
    cursor.execute(query_insert_file, (file_name, 1))
    cursor.execute(query_insert_file_version, (cursor.lastrowid, 1, 'INIT'))
    mydb.commit()
    cursor.close()
    mydb.close()
    return 'inserted'   

def init_tables():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1")
    cursor = mydb.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS PANDAS_UI")
    cursor.close()

    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="PANDAS_UI"
    )
    cursor = mydb.cursor()
    cursor.execute("DROP TABLE IF EXISTS files_version")
    cursor.execute("DROP TABLE IF EXISTS files")
    for table_name in TABLES:
        cursor.execute(TABLES[table_name])

    cursor.close()
    mydb.close()
    return 'init db\n' 