import PIL.Image
from google import genai
from src.config import GEMINI_API_KEYS
from src.utils.prompts import VISION_PROMPT

def extract_vibe(image_path):
    try:
        img = PIL.Image.open(image_path)
    except Exception as e:
        print(f"❌ โหลดรูปไม่สำเร็จ: {e}")
        return "ธรรมชาติ, พักผ่อน"

    for index, key in enumerate(GEMINI_API_KEYS):
        try:
            client = genai.Client(api_key=key)
            response = client.models.generate_content(
                model="gemini-3-flash-preview", 
                contents=[VISION_PROMPT, img]
            )
            return response.text.strip()
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "Quota" in error_msg:
                print(f"⚠️ [Vision] Key ที่ {index + 1} หมดโควต้า! กำลังสลับไป Key ถัดไป...")
                continue
            else:
                print(f"❌ Vision Agent Error: {e}")
                return "ธรรมชาติ, พักผ่อน, จุดชมวิว"
                
    # ถ้าหลุดลูปมาถึงตรงนี้ แปลว่าโควต้าหมดเกลี้ยงทั้ง 4 Keys
    print("❌ [Vision] โควต้าหมดเกลี้ยงทุก Key แล้วครับพี่!")
    return "ธรรมชาติ, พักผ่อน, จุดชมวิว"