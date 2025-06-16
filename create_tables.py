import mysql.connector
from mysql.connector import Error

def setup_database():
    try:
        # First connect without database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="181103"
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Read and execute SQL script
            with open('create_tables.sql', 'r') as file:
                # Read the entire script
                sql_script = file.read()
                
                # Split and execute each command
                for command in sql_script.split(';'):
                    if command.strip():
                        cursor.execute(command.strip())
                        connection.commit()
            
            print("Database and tables created successfully!")
            
            # Verify the table exists
            cursor.execute("USE register")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("Available tables:", tables)
            
            # Verify admin user exists
            cursor.execute("SELECT username, role FROM users")
            users = cursor.fetchall()
            print("Existing users:", users)
            
    except Error as e:
        print(f"Error: {e}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    setup_database() 