import mysql.connector
from mysql.connector import Error

def setup_database():
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Read and execute SQL script
            with open('setup_mysql.sql', 'r') as file:
                sql_commands = file.read().split(';')
                
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
            
            connection.commit()
            print("Database setup completed successfully!")
            
    except Error as e:
        print(f"Error: {e}")
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    setup_database() 