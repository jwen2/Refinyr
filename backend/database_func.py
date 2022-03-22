import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'PANDAS_UI'
TABLES = {}
TABLES['files'] = (
    "CREATE TABLE `files` ("
    "   `file_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `file_name` varchar(255) NOT NULL,"
    "   `version` int(11) NOT NULL,"
    "   PRIMARY KEY (`file_id`))"
)
TABLES['files_version'] = (
    "CREATE TABLE `files_version` ("
    "   `file_version_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `file_id` int(11) NOT NULL,"
    "   `file_version` int(11) NOT NULL,"
    "   `function` varchar(255) NOT NULL,"
    "   PRIMARY KEY (`file_version_id`),"
    "   FOREIGN KEY (`file_id`) REFERENCES files (`file_id`))"
)

insert_file = ("INSERT INTO files "
              "(file_name, version) "
              "VALUES ('test', 1)")

insert_file_version = ("INSERT INTO files_version"
                      "(file_id, file_version, function)"  
                      "VALUES (SELECT(file_id FROM files WHERE file_name = %s), %s, %s)")

def insert_file(file_name):
    print('file_name' + file_name)
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="PANDAS_UI"
    )
    file_data = ("test_file", 1)
    file_version_data = ("test_file", 1, 'INIT')
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO files "
              "(file_name, version) "
              "VALUES ('test', 1)")
    # cursor.execute(insert_file, file_data)
    # cursor.execute(insert_file_version, file_version_data)
    mydb.commit()
    cursor.close()
    mydb.close()
    return ''   

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