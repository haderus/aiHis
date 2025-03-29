from moviepy.editor import VideoFileClip
import whisper
from transformers import pipeline
import os

class VideoProcessor:
    def __init__(self):
        self.whisper_model = whisper.load_model("base")
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
    def extract_audio(self, video_path):
        try:
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video file not found: {video_path}")
                
            video = VideoFileClip(video_path)
            audio_path = video_path.rsplit('.', 1)[0] + '.mp3'
            video.audio.write_audiofile(audio_path)
            video.close()
            return audio_path
            
        except Exception as e:
            return None
            
    def transcribe_audio(self, audio_path):
        try:
            result = self.whisper_model.transcribe(audio_path)
            return result["text"]
            
        except Exception as e:
            return None
            
    def generate_summary(self, text, max_length=130, min_length=30):
        try:
            summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return summary[0]['summary_text']
            
        except Exception as e:
            return None
    
    def process_video(self, video_path):
        try:
            result = {
                'status': 'success',
                'transcript': '',
                'summary': '',
                'message': ''
            }
            
            audio_path = self.extract_audio(video_path)
            if not audio_path:
                raise Exception("Failed to extract audio")
                
            transcript = self.transcribe_audio(audio_path)
            if not transcript:
                raise Exception("Failed to transcribe audio")
                
            summary = self.generate_summary(transcript)
            if not summary:
                raise Exception("Failed to generate summary")
                
            result['transcript'] = transcript
            result['summary'] = summary
            
            os.remove(audio_path)
            return result
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

def main():
    processor = VideoProcessor()
    result = processor.process_video("test.mp4")
    
    if result['status'] == 'success':
        print("Video Summary:")
        print(result['summary'])
        print("\nFull Transcript:")
        print(result['transcript'])
    else:
        print("Processing Failed:", result['message'])

if __name__ == "__main__":
    main()