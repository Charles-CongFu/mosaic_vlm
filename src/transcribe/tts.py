import pygame
import tempfile
import langdetect
from gtts import gTTS

from src.utils import get_last_text_line

def play_text_to_speech(text, language='en'):
    """
    Convert text to speech and play it using gTTS and pygame.
    """
    tts = gTTS(text=text, lang=language, slow=False)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        tts.save(fp.name)
        temp_path = fp.name
    pygame.mixer.init()
    pygame.mixer.music.load(temp_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def run_tts():
    """
    Run text-to-speech conversion based on the last line of a text file.
    """
    transcription_file = "./src/transcribe/transcription.txt"
    text = get_last_text_line(transcription_file)
    language = langdetect.detect(text) if text else 'en'
    if text:
        play_text_to_speech(text, language)
        print("🎵 Text-to-speech playback completed.")
    else:
        print("No valid text found in transcription file.")

if __name__ == "__main__":
    run_tts()