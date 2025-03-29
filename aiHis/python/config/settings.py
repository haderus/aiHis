import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'content.db')

OCR_CONFIG = {
    'use_angle_cls': True,
    'lang': 'ch'
}

VIDEO_CONFIG = {
    'whisper_model': 'base',
    'summarizer_model': 'facebook/bart-large-cnn'
}

TEXT_CONFIG = {
    'classifier_model': 'bert-base-chinese'
}

SEARCH_CONFIG = {
    'model_name': 'shibing624/text2vec-base-chinese',
    'default_threshold': 0.6,
    'default_limit': 10
}