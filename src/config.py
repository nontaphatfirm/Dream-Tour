import os
from dotenv import load_dotenv

# โหลดตัวแปรจากไฟล์ .env
load_dotenv()

# ประกาศตัวแปร Global ให้ไฟล์อื่นเรียกใช้
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")