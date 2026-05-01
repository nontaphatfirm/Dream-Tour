from tavily import TavilyClient
from src.config import TAVILY_API_KEY

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

def get_local_reviews(vibe_keywords, region="", province=""):
    """
    รับคีย์เวิร์ด + ภาค/จังหวัด -> ค้นหา Pantip/เว็บไทย ด้วย Tavily -> คืนค่า Text (Context)
    """
    try:
        location_keyword = f"{province} {region}".strip()
        
        if location_keyword:
            query = f"สถานที่ท่องเที่ยว Unseen {location_keyword} รีวิว {vibe_keywords}"
        else:
            query = f"สถานที่ท่องเที่ยว Unseen ประเทศไทย รีวิว {vibe_keywords}"
            
        response = tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=4
        )
        
        results = response.get("results", [])
        context = "\n\n---\n\n".join([item["content"] for item in results])
        
        if not context.strip():
            return "ไม่พบข้อมูลที่ตรงกับ Vibe นี้"
            
        return context

    except Exception as e:
        print(f"❌ Search Agent (Reviews) Error: {e}")
        return ""

def get_place_image(search_keyword):
    """
    รับชื่อสถานที่ -> ค้นหารูปภาพด้วย Tavily -> คืนค่า URL รูปภาพ
    """
    try:
        response = tavily_client.search(
            query=search_keyword,
            search_depth="basic",
            include_images=True,
            max_results=1
        )
        
        images = response.get("images", [])
        
        if images and len(images) > 0:
            return images[0]
        else:
            return "https://via.placeholder.com/600x400?text=No+Image+Available"

    except Exception as e:
        print(f"❌ Search Agent (Image) Error: {e}")
        return "https://via.placeholder.com/600x400?text=API+Limit+Reached"