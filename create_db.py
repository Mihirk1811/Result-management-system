import sqlite3

def create_db():
    try:
        con = sqlite3.connect(database="sms.db")
        cur = con.cursor()
        
        # Create student table
        cur.execute("""CREATE TABLE IF NOT EXISTS student(
            roll INTEGER PRIMARY KEY AUTOINCREMENT,
            name text,
            email text,
            gender text,
            dob text,
            contact text,
            admission text,
            course text,
            state text,
            city text,
            pin text,
            address text
        )""")
        
        # Create users table for authentication
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        
        # Insert default admin user
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))
        except sqlite3.IntegrityError:
            pass  # Admin user already exists
        
        con.commit()
        print("Database and tables created successfully!")
        
    except Exception as es:
        print("Error:", str(es))
    finally:
        if 'con' in locals():
            con.close()

if __name__ == "__main__":
    create_db()
