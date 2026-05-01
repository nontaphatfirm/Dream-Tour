import google.generativeai as genai
from src.config import GEMINI_API_KEY
from src.utils.prompts import VISION_PROMPT

# ตั้งค่า API Key
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def extract_vibe(image_path):
    """
    รับรูปภาพจาก Gradio -> ส่งเข้า Gemini -> คืนค่าคีย์เวิร์ด (String)
    """
    # TODO: เขียน Logic อ่านรูปภาพและเรียกใช้ model.generate_content()
    # ส่ง VISION_PROMPT เข้าไปด้วย
    return "ภูเขา, ทะเลหมอก, เงียบสงบ" # Mock return