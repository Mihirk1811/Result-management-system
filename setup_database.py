import mysql.connector
from mysql.connector import Error
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def verify_connection(host, user, password, database=None):
    try:
        if database:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
        else:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def drop_and_recreate_table(cursor):
    try:
        # Drop the table if it exists
        cursor.execute("DROP TABLE IF EXISTS users")
        print("Dropped existing users table.")
        
        # Create the table fresh
        create_users_table = """
        CREATE TABLE users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100),
            role ENUM('admin', 'teacher', 'student') DEFAULT 'student',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_users_table)
        print("Created fresh users table.")
        return True
    except Error as e:
        print(f"Error in drop_and_recreate_table: {e}")
        return False

def setup_database():
    clear_screen()
    # Database configuration
    HOST = "localhost"
    USER = "root"
    PASSWORD = "181103"
    DATABASE = "register"
    
    try:
        print("="*50)
        print("Starting database setup...")
        print("="*50)
        
        # Step 1: Connect to MySQL server
        print("\nStep 1: Connecting to MySQL server...")
        connection = verify_connection(HOST, USER, PASSWORD)
        if not connection:
            input("\nFailed to connect to MySQL server. Check if MySQL is running and credentials are correct.")
            return
        print("✓ Successfully connected to MySQL server.")
        
        cursor = connection.cursor(buffered=True)
        
        # Step 2: Drop database if exists and create new
        print("\nStep 2: Recreating database...")
        cursor.execute(f"DROP DATABASE IF EXISTS {DATABASE}")
        cursor.execute(f"CREATE DATABASE {DATABASE}")
        print(f"✓ Database '{DATABASE}' recreated successfully.")
        
        # Step 3: Switch to the database
        print(f"\nStep 3: Switching to database '{DATABASE}'...")
        cursor.execute(f"USE {DATABASE}")
        print(f"✓ Now using database '{DATABASE}'")
        
        # Step 4: Create users table
        print("\nStep 4: Creating users table...")
        if not drop_and_recreate_table(cursor):
            print("Failed to create users table.")
            return
        print("✓ Users table created successfully.")
        
        # Step 5: Verify table exists
        print("\nStep 5: Verifying table creation...")
        cursor.execute("SHOW TABLES LIKE 'users'")
        if cursor.fetchone():
            print("✓ Users table verified successfully.")
        else:
            print("Error: Users table was not created properly.")
            return
        
        # Step 6: Insert default admin user
        print("\nStep 6: Creating default admin user...")
        insert_admin = """
        INSERT INTO users (username, password, email, role) 
        VALUES ('admin', 'admin123', 'admin@school.com', 'admin')
        """
        cursor.execute(insert_admin)
        connection.commit()
        print("✓ Admin user created successfully.")
        
        # Step 7: Verify admin user
        print("\nStep 7: Verifying admin user...")
        cursor.execute("SELECT username, role FROM users WHERE username='admin'")
        admin_user = cursor.fetchone()
        if admin_user:
            print(f"✓ Admin user verified. Username: {admin_user[0]}, Role: {admin_user[1]}")
        else:
            print("Error: Admin user was not created properly.")
            return
        
        print("\n" + "="*50)
        print("Database setup completed successfully!")
        print("="*50)
        print("\nYou can now log in with:")
        print("Username: admin")
        print("Password: admin123")
        
        # Final verification
        print("\nFinal Database Status:")
        cursor.execute("SHOW TABLES")
        print("\nTables in database:")
        for table in cursor.fetchall():
            print(f"- {table[0]}")
        
        cursor.execute("SELECT id, username, role FROM users")
        print("\nUsers in database:")
        for user in cursor.fetchall():
            print(f"- ID: {user[0]}, Username: {user[1]}, Role: {user[2]}")
        
    except Error as e:
        print(f"\nError during setup: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure MySQL server is running")
        print("2. Verify your MySQL password is correct")
        print("3. Ensure you have proper permissions")
        print("4. Check if port 3306 is not blocked")
    
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("\nMySQL connection closed.")
    
    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    setup_database() 