from paddleocr import PaddleOCR
from ..config.settings import OCR_CONFIG

class OCRProcessor:
    def __init__(self):
        self.ocr = PaddleOCR(**OCR_CONFIG)
    
    def process_image(self, image_path):
        try:
            result = self.ocr.ocr(image_path, cls=True)
            return self._format_result(result)
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _format_result(self, result):
        if not result:
            return {'status': 'error', 'message': 'No text detected'}
            
        return {
            'status': 'success',
            'text': '\n'.join([line[1][0] for line in result[0]]),
            'details': [
                {'text': line[1][0], 'confidence': line[1][1], 'position': line[0]}
                for line in result[0]
            ]
        }