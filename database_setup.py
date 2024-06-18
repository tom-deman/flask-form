import os
import mysql.connector
from dotenv import load_dotenv


load_dotenv()

MYSQL_HOST     = os.getenv( 'MYSQL_HOST'     )
MYSQL_USER     = os.getenv( 'MYSQL_USER'     )
MYSQL_PASSWORD = os.getenv( 'MYSQL_PASSWORD' )
MYSQL_DB       = os.getenv( 'MYSQL_DB'       )


def create_database():
    try:
        connection = mysql.connector.connect(
            host     = MYSQL_HOST,
            user     = MYSQL_USER,
            password = MYSQL_PASSWORD
        )

        cursor = connection.cursor()

        cursor.execute( f"CREATE DATABASE IF NOT EXISTS { MYSQL_DB }" )
        print( f"Database '{ MYSQL_DB }' created successfully" )

        cursor.execute( f"USE { MYSQL_DB }" )

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS forms (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                country VARCHAR(100),
                message TEXT,
                gender ENUM('M', 'F'),
                subject VARCHAR(100)
            )
        """)
        print( "Table 'forms' created successfully" )

        connection.commit()
        cursor.close()
        connection.close()
        print( "Database setup completed successfully" )

    except mysql.connector.Error as err:
        print( f"Error: { err }" )

create_database()