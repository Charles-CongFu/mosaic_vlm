from src.mistral_ai.mistral import Mistralmodel
from src.mistral_ai.prompts.recipe_prompt import system_prompt, example, assistant_prompt
from src.utils import get_last_text_line

def run_mistral_llm():
    client = Mistralmodel()

    transcribed_text = get_last_text_line("./src/transcribe/transcription.txt")

    subtasks = client.chat_with_text(transcribed_text, system_prompt=system_prompt, example=example, assistant_prompt=assistant_prompt)
    print(f"🤖 LLM Response:")
    print(">>> Subtask list：\n", subtasks)
    # Save LLM results
    with open("./src/mistral_ai/scripts/llm_script.txt", "a", encoding="utf-8") as f:
        f.write(str(subtasks))

if __name__ == "__main__":
    run_mistral_llm()