import sqlite3
from transformers import pipeline
import pandas as pd
import json
from datetime import datetime

class TextProcessor:
    def __init__(self):
        self.classifier = pipeline("text-classification", model="bert-base-chinese")
        self.db_path = "d:/aiHis/content.db"
        self.init_database()
        
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
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
        conn.commit()
        conn.close()
        
    def classify_text(self, text):
        result = self.classifier(text)
        return {
            'category': result[0]['label'],
            'confidence': result[0]['score']
        }
        
    def store_content(self, content, metadata=None):
        try:
            classification = self.classify_text(content)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO content_records 
                (content, category, confidence, metadata, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                content,
                classification['category'],
                classification['confidence'],
                json.dumps(metadata) if metadata else None,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            record_id = cursor.lastrowid
            conn.close()
            
            return {
                'status': 'success',
                'record_id': record_id,
                'classification': classification
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def search_content(self, category=None, confidence_threshold=0.5):
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = "SELECT * FROM content_records WHERE confidence >= ?"
            params = [confidence_threshold]
            
            if category:
                query += " AND category = ?"
                params.append(category)
                
            df = pd.read_sql_query(query, conn, params=params)
            conn.close()
            
            return df.to_dict('records')
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_content_by_id(self, record_id):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM content_records WHERE id = ?", (record_id,))
            record = cursor.fetchone()
            conn.close()
            
            if record:
                return {
                    'id': record[0],
                    'content': record[1],
                    'category': record[2],
                    'confidence': record[3],
                    'metadata': json.loads(record[4]) if record[4] else None,
                    'created_at': record[5]
                }
            return None
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

def main():
    processor = TextProcessor()
    
    test_content = "这是一段测试文本，用于演示文本分类和存储功能。"
    test_metadata = {
        'source': 'test',
        'author': 'system'
    }
    
    store_result = processor.store_content(test_content, test_metadata)
    if store_result['status'] == 'success':
        print("Content stored with ID:", store_result['record_id'])
        print("Classification:", store_result['classification'])
        
        search_results = processor.search_content()
        print("\nAll stored contents:")
        for result in search_results:
            print(f"ID: {result['id']}, Category: {result['category']}")

if __name__ == "__main__":
    main()