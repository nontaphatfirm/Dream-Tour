import json
from google import genai
from src.config import GEMINI_API_KEY
from src.utils.prompts import BRAIN_PROMPT

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_recommendations(context):
    """
    รับ Context จาก Tavily -> ส่งเข้า Gemini ให้จัด JSON Top 5
    """
    prompt = BRAIN_PROMPT.format(context=context)
    
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        
        raw_text = response.text.strip()
        
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:]
            
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        clean_text = raw_text.strip()
        
        places_data = json.loads(clean_text)
        
        return places_data
        
    except json.JSONDecodeError as e:
        print(f"❌ Brain Agent (JSON Decode Error): {e}")
        print(f"📄 Raw Text ที่มีปัญหา:\n{raw_text}")
        return []
        
    except Exception as e:
        print(f"❌ Brain Agent (API Error): {e}")
        return []