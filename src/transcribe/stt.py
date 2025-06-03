import os
import queue
import threading
import pyaudio
import wave
import tempfile
import whisper
import torch
from datetime import datetime

# 配置参数集中管理
class Config:
    MODEL_SIZE = "medium"
    OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transcription.txt")

def get_valid_audio_device_info():
    """detect and return valid audio input device info"""
    p = pyaudio.PyAudio()
    try:
        default_device_index = p.get_default_input_device_info()['index']
        device_info = p.get_device_info_by_index(default_device_index)
    except IOError:
        # 没有默认设备，找第一个可用输入设备
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                print(f"\nDefault device not available, using device {i}: {device_info['name']}")
                break
        else:
            p.terminate()
            raise IOError("No valid audio input device found")
    sample_rate = int(device_info['defaultSampleRate'])
    channels = min(1, int(device_info['maxInputChannels']))
    p.terminate()
    return {
        'index': device_info['index'],
        'channels': channels,
        'rate': sample_rate,
        'format': pyaudio.paInt16,
        'name': device_info['name']
    }

# Whisper模型加载，自动CUDA
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"loading model '{Config.MODEL_SIZE}' on {device.upper()} ...")
model = whisper.load_model(Config.MODEL_SIZE, device=device)

class Recorder:
    def __init__(self, device_info):
        self.device_info = device_info
        self.q = queue.Queue()
        self.frames = []
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.recording = threading.Event()

    def start(self):
        self.frames = []
        self.recording.set()
        self.stream = self.p.open(
            format=self.device_info['format'],
            channels=self.device_info['channels'],
            rate=self.device_info['rate'],
            input=True,
            input_device_index=self.device_info['index'],
            frames_per_buffer=1024,
            stream_callback=self.callback
        )
        self.stream.start_stream()
        print(f"🎤 Recording started... (press any key to stop)", end="", flush=True)

    def callback(self, in_data, frame_count, time_info, status):
        if self.recording.is_set():
            self.q.put(in_data)
        return (None, pyaudio.paContinue)

    def stop(self):
        self.recording.clear()
        self.stream.stop_stream()
        self.stream.close()
        # 收集所有帧
        while not self.q.empty():
            self.frames.append(self.q.get())
        self.p.terminate()
        print("⏹️  Recording stopped, processing...")

    def save_wav(self):
        if not self.frames:
            return None
        temp_file = tempfile.mktemp(suffix=".wav")
        with wave.open(temp_file, 'wb') as wf:
            wf.setnchannels(self.device_info['channels'])
            wf.setsampwidth(self.p.get_sample_size(self.device_info['format']))
            wf.setframerate(self.device_info['rate'])
            wf.writeframes(b''.join(self.frames))
        return temp_file

def transcribe_audio(audio_path):
    try:
        result = model.transcribe(audio_path, fp16=(device=="cuda"))
        return result["text"].strip()
    except Exception as e:
        print(f"Transcription error: {e}")
        return ""

def append_to_file(text):
    if text:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(Config.OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {text}\n")
        print(f"✅ Transcription saved to: {Config.OUTPUT_FILE}")

# main function to run the STT process
def run_stt():
    print(f"📝 Transcriptions will be saved to: {Config.OUTPUT_FILE}")
    print("🎙️  Press Enter to start recording, Enter again to stop and transcribe. Ctrl+C to exit.")

    # detect and get valid audio device info
    device_info = get_valid_audio_device_info()
    print(f"Using device: {device_info['name']} (index {device_info['index']}), sample rate: {device_info['rate']}, channels: {device_info['channels']}")

    while True:
        print("Press Enter to start recording...", end="", flush=True)
        input()
        recorder = Recorder(device_info)
        recorder.start()
        input()  # 等待用户再次按Enter
        recorder.stop()
        wav_file = recorder.save_wav()
        if wav_file:
            print("🔄 Transcribing audio...")
            text = transcribe_audio(wav_file)
            if text:
                print(f"📝 Transcription result: {text}")
                append_to_file(text)
            else:
                print("❌ No valid speech detected or transcription failed")
            os.remove(wav_file)
        else:
            print("❌ No audio recorded")
        print("="*50 + "\n📋 Continue recording? (y/n): ")
        choice = input().lower().strip()
        if choice in ['n', 'no', 'q']:
            print("👋 Program stopped")
            break
if __name__ == "__main__":
    run_stt()