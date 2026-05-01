import PIL.Image
from google import genai
from src.config import GEMINI_API_KEY
from src.utils.prompts import VISION_PROMPT

client = genai.Client(api_key=GEMINI_API_KEY)

def extract_vibe(image_path):
    try:
        img = PIL.Image.open(image_path)
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=[VISION_PROMPT, img]
        )
        
        return response.text.strip()
        
    except Exception as e:
        print(f"❌ Vision Agent Error: {e}")
        return "ธรรมชาติ, พักผ่อน, จุดชมวิว"