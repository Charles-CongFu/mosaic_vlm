import json
import re
from src.mistral_ai.mistral import Mistralmodel
from src.mistral_ai.prompts.vision_prompt import system_prompt, example, assistant_prompt, user_prompt

def extract_json(text):
    """extract all JSON objects from the current VLM response"""
    json_blocks = []
    # match ```json ... ``` 或 {...}
    for match in re.finditer(r"```json\s*({[\s\S]*?})\s*```|({[\s\S]*?})", text):
        json_str = match.group(1) or match.group(2)
        try:
            json_blocks.append(json.loads(json_str))
        except Exception as e:
            print(f"JSON parse error: {e}")
    return json_blocks

def run_mistral_vlm():
    """Run Mistral Vision Language Model (VLM) for image analysis"""
    client = Mistralmodel()
    local_image = input("📂 input local image path: ").strip()

    vision_resp = client.chat_with_vision(user_prompt, local_image, system_prompt=system_prompt, example=example, assistant_prompt=assistant_prompt)
    print(f"🤖 VLM Response:")
    print(">>> Vision response：\n", vision_resp)
    # save VLM results
    with open("./src/mistral_ai/scripts/vlm_script.txt", "a", encoding="utf-8") as f:  # append模式
        f.write(str(vision_resp) + "\n")
    # extract JSON objects from the response
    json_obj = extract_json(str(vision_resp))
    if json_obj:
        with open("./src/mistral_ai/scripts/vlm_script.json", "w", encoding="utf-8") as jf:
            json.dump(json_obj, jf, ensure_ascii=False, indent=2)
        print("✅ Saved as JSON: ./src/mistral_ai/scripts/vlm_script.json")
    else:
        print("❌ No valid JSON content found")