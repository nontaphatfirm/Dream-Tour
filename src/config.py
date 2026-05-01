import os
from dotenv import load_dotenv

load_dotenv()

keys_string = os.getenv("GEMINI_API_KEYS", "")
GEMINI_API_KEYS = [key.strip() for key in keys_string.split(",") if key.strip()]

print(f"✅ โหลด Gemini API Key เข้ามาในระบบแล้ว: {len(GEMINI_API_KEYS)} คีย์")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")