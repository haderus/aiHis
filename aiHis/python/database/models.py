import sqlite3
from datetime import datetime

class DatabaseConnection:
    def __init__(self, db_path):
        self.db_path = db_path

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

def init_database(db_path):
    with DatabaseConnection(db_path) as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT,
                category TEXT,
                confidence FLOAT,
                metadata TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                type TEXT,
                parent_id INTEGER,
                FOREIGN KEY (parent_id) REFERENCES categories (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_categories (
                content_id INTEGER,
                category_id INTEGER,
                FOREIGN KEY (content_id) REFERENCES content_records (id),
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        
        conn.commit()