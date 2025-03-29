import sqlite3
from datetime import datetime
import json
from collections import defaultdict

class ContentManager:
    def __init__(self):
        self.db_path = "d:/aiHis/content.db"
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
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
        conn.close()

    def add_category(self, name, type, parent_id=None):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO categories (name, type, parent_id)
                VALUES (?, ?, ?)
            ''', (name, type, parent_id))
            
            category_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return category_id
        except Exception as e:
            return None

    def categorize_content(self, content_id, categories):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for category_id in categories:
                cursor.execute('''
                    INSERT INTO content_categories (content_id, category_id)
                    VALUES (?, ?)
                ''', (content_id, category_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False

    def get_content_by_category(self, category_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT cr.* FROM content_records cr
            JOIN content_categories cc ON cr.id = cc.content_id
            WHERE cc.category_id = ?
        ''', (category_id,))
        
        results = cursor.fetchall()
        conn.close()
        return results

    def get_content_by_time_range(self, start_date, end_date):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM content_records
            WHERE created_at BETWEEN ? AND ?
        ''', (start_date, end_date))
        
        results = cursor.fetchall()
        conn.close()
        return results

    def get_content_by_source(self, source):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM content_records
            WHERE json_extract(metadata, '$.source') = ?
        ''', (source,))
        
        results = cursor.fetchall()
        conn.close()
        return results

    def get_category_tree(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM categories')
        categories = cursor.fetchall()
        conn.close()
        
        tree = defaultdict(list)
        for cat in categories:
            parent_id = cat[3] if cat[3] else 'root'
            tree[parent_id].append({
                'id': cat[0],
                'name': cat[1],
                'type': cat[2]
            })
        return dict(tree)

def main():
    manager = ContentManager()
    
    source_id = manager.add_category("微信", "source")
    topic_id = manager.add_category("技术", "topic")
    
    test_categories = [source_id, topic_id]
    manager.categorize_content(1, test_categories)
    
    print("Content by category:")
    print(manager.get_content_by_category(source_id))
    
    print("\nCategory tree:")
    print(json.dumps(manager.get_category_tree(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()