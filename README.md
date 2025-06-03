# 语音转录 + AI 助手

这是一个整合了语音转录和AI分析的应用程序，支持实时录音、Whisper语音转录和Mistral AI模型分析。

## 🏗️ 项目结构

```
.
├── main.py
├── src/
│   ├── mistral_ai/
│   │   ├── prompts/
│   │   │   ├── recipe_prompt.py # for LLM
│   │   │   └── vision_prompt.py # for VLM
│   │   ├── scripts/
│   │   │   ├── llm_script.txt # LLM reponses history
│   │   │   ├── vlm_script.json # JSON extract from VLM history
│   │   │   └── vlm_script.txt # VLM reponses history
│   │   ├── mistral.py # api and structure
│   │   ├── llm.py
│   │   └── vlm.py
│   ├── transcribe/
│   │   ├── sst.py 
│   │   ├── tts.py
│   │   └── transcription.txt
│   └── utils.py
├── main.py
├── run.sh
└── requirements.txt
```

## 🔧 Installation guide

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables in shell config**:
   ```bash
   export MISTRAL_API_KEY="your_mistral_api_key_here"
   ```

## 🎯 Operation guide

#TODO
