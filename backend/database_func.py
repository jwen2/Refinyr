import mysql.connector

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
    cursor.execute("DROP TABLE IF EXISTS files")
    cursor.execute("DROP TABLE IF EXISTS files_version")
    cursor.execute("CREATE TABLE IF NOT EXISTS files (file_name VARCHAR(255), PRIMARY KEY (file_name), version INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS files_version (file_name VARCHAR(255), FOREIGN KEY (file_name) REFERENCES files (file_name), version INTEGER, function_applied VARCHAR(255))")
    cursor.close()
    return 'init db'