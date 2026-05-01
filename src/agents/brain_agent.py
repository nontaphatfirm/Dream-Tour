import json
from google import genai
from src.config import GEMINI_API_KEYS
from src.utils.prompts import BRAIN_PROMPT

def generate_recommendations(context, vibe_keywords):
    prompt = BRAIN_PROMPT.format(context=context, vibe=vibe_keywords)
    
    for index, key in enumerate(GEMINI_API_KEYS):
        try:
            client = genai.Client(api_key=key)
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
                
            return json.loads(raw_text.strip())
            
        except json.JSONDecodeError as e:
            print(f"❌ [Brain] JSON Error: {e}")
            return []
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "Quota" in error_msg:
                print(f"⚠️ [Brain] Key ที่ {index + 1} หมดโควต้า! กำลังสลับไป Key ถัดไป...")
                continue
            else:
                print(f"❌ [Brain] API Error: {e}")
                return []
                
    print("❌ [Brain] โควต้าหมดเกลี้ยงทุก Key แล้วครับพี่!")
    return []