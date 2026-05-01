from tavily import TavilyClient
from src.config import TAVILY_API_KEY

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

def get_local_reviews(vibe_keywords):
    """
    รับคีย์เวิร์ด -> ค้นหา Pantip/เว็บไทย ด้วย Tavily -> คืนค่า Text (Context)
    """
    # TODO: เขียน Logic สร้าง query เช่น "สถานที่ท่องเที่ยว Unseen ประเทศไทย Pantip {vibe_keywords}"
    # ใช้ tavily_client.search(query, search_depth="advanced")
    return "ข้อมูลรีวิวสถานที่เที่ยวจาก Pantip..." # Mock return

def get_place_image(search_keyword):
    """
    รับชื่อสถานที่ -> ค้นหารูปภาพด้วย Tavily -> คืนค่า URL รูปภาพ
    """
    # TODO: ใช้ tavily_client.search(search_keyword, include_images=True)
    # คืนค่า image URL ใบแรกที่เจอ หรือ placeholder ถ้าไม่เจอ
    return "https://via.placeholder.com/600x400" # Mock return