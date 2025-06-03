from src.transcribe.stt import run_stt
from src.transcribe.tts import run_tts
from src.mistral_ai.llm import run_mistral_llm
from src.mistral_ai.vlm import run_mistral_vlm

if __name__ == "__main__":
    run_stt()
    run_tts()
    run_mistral_llm()
    run_mistral_vlm()