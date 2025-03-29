from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from ..database.manager import DatabaseManager
from ..config.settings import SEARCH_CONFIG

class SearchProcessor:
    def __init__(self):
        self.model = SentenceTransformer(SEARCH_CONFIG['model_name'])
        self.db_manager = DatabaseManager()
        
    def search(self, query, threshold=0.6, limit=10):
        try:
            query_embedding = self.model.encode([query])[0]
            contents = self.db_manager.get_all_contents()
            
            if not contents:
                return {'status': 'error', 'message': 'No content found'}
            
            similarities = []
            for content in contents:
                content_embedding = self.model.encode([content['content']])[0]
                similarity = cosine_similarity([query_embedding], [content_embedding])[0][0]
                similarities.append((content, similarity))
            
            results = sorted(similarities, key=lambda x: x[1], reverse=True)
            filtered_results = [
                {**r[0], 'similarity': float(r[1])} 
                for r in results 
                if r[1] >= threshold
            ][:limit]
            
            return {
                'status': 'success',
                'results': filtered_results,
                'total': len(filtered_results)
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def search_by_category(self, query, category_id, threshold=0.6, limit=10):
        try:
            query_embedding = self.model.encode([query])[0]
            contents = self.db_manager.get_content_by_category(category_id)
            
            if not contents:
                return {'status': 'error', 'message': 'No content found in category'}
            
            similarities = []
            for content in contents:
                content_embedding = self.model.encode([content['content']])[0]
                similarity = cosine_similarity([query_embedding], [content_embedding])[0][0]
                similarities.append((content, similarity))
            
            results = sorted(similarities, key=lambda x: x[1], reverse=True)
            filtered_results = [
                {**r[0], 'similarity': float(r[1])} 
                for r in results 
                if r[1] >= threshold
            ][:limit]
            
            return {
                'status': 'success',
                'results': filtered_results,
                'total': len(filtered_results)
            }
        
        except Exception as e:
            return {'status': 'error', 'message': str(e)}