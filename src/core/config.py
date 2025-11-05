import os
from dotenv import load_dotenv
from pathlib import Path

# грузим .env из корня проекта, даже если запуск идёт из другой папки
ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env", override=True)

class Cfg:
    TG_TOKEN = os.getenv("TG_BOT_TOKEN")
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1")
    LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")
