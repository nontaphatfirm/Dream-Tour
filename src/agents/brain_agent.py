import json
import google.generativeai as genai
from src.config import GEMINI_API_KEY
from src.utils.prompts import BRAIN_PROMPT

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

def generate_recommendations(context):
    """
    รับ Context จาก Tavily -> ส่งเข้า Gemini ให้จัด JSON Top 5
    """
    prompt = BRAIN_PROMPT.format(context=context)
    
    # TODO: เรียกใช้ model.generate_content(prompt)
    # TODO: จัดการคลีนข้อความ (ลบ ```json ออก) และแปลงเป็น Python List ด้วย json.loads()
    
    # Mock return
    return [
        {
            "rank": 1,
            "place_name": "ม่อนแจ่ม, เชียงใหม่",
            "description": "วิวภูเขาสวยงาม",
            "what_locals_say": "ทางขึ้นชัน ระวังรถติด",
            "local_transit": "เหมารถแดงจากตัวเมือง",
            "search_keyword": "Mon Jam Chiang Mai"
        }
    ]