import sqlite3
import os

# Path to your SQLite database
DATABASE = 'app.db'

# Initialize database tables if the database does not exist
def init_db():
    # Check if database already exists
    if not os.path.exists(DATABASE):
        print("Database not found! Creating new database...")
        
        # Connect to the database file (this will create the file if it doesn't exist)
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Create the tables if they do not exist
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                contact TEXT NOT NULL,
                phone TEXT NOT NULL,
                time_in_process TEXT NOT NULL,
                cost REAL NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_name TEXT NOT NULL,
                cost REAL NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        ''')

        cursor.execute('''
            CREATE TABLE expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL
            );
        ''')

        # Commit changes and close connection
        conn.commit()
        conn.close()
        print("Database and tables created successfully.")
    else:
        print("Database already exists. Skipping creation.")
