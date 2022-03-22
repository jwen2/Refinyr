import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'PANDAS_UI'
TABLES = {}
TABLES['files'] = (
    "CREATE TABLE `files` ("
    "   `file_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `file_name` varchar(255) NOT NULL,"
    "   `version` int(11) NOT NULL,"
    "   PRIMARY KEY (`file_id`)"
)
TABLES['files_version'] = (
    "CREATE TABLE `files_version` ("
    "   `file_version_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `file_id` int(11) NOT NULL,"
    "   `file_version` int(11) NOT NULL,"
    "   `function` varchar(255) NOT NULL,"
    "   FOREIGN KEY (`file_id`) REFERENCES files (`file_id`)"
)

insert_file = ("INSERT INTO files "
              "(file_name, version) "
              "VALUES (%s, %d)")

insert_file_version = ("INSERT INTO files_version"
                      "(file_name)"  
)

def insert_file(file_data):
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="PANDAS_UI"
    )
    cursor = mydb.cursor()
    cursor.execute(insert_file, file_data)
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
        try:
            cursor.execute(TABLES[table_name])
        except mysql.connector.Error as err:
            print(err.msg)

    # cursor.execute("CREATE TABLE IF NOT EXISTS files (file_id INTEGER, file_name VARCHAR(255), version INTEGER, PRIMARY KEY (id))")
    # cursor.execute("CREATE TABLE IF NOT EXISTS files_version (file_version_id INTEGER, file_name VARCHAR(255), FOREIGN KEY (file_name) REFERENCES files (file_name), version INTEGER, function_applied VARCHAR(255))")
    cursor.close()
    mydb.close()
    return 'init db\n' 