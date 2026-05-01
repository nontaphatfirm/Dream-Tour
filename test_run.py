import os
import json
# นำเข้าฟังก์ชันทั้งหมดที่เราเขียนไว้
from src.agents.vision_agent import extract_vibe
from src.agents.search_agent import get_local_reviews, get_place_image
from src.agents.brain_agent import generate_recommendations

def run_tests():
    print("🚀 เริ่มต้นการทดสอบระบบทีละส่วน...\n")

    # ---------------------------------------------------------
    # 1. ทดสอบ The Eye (Vision Agent)
    # ---------------------------------------------------------
    print("--- [Test 1] Vision Agent ---")
    # หาไฟล์รูปภาพอะไรก็ได้ในเครื่องมา 1 รูปสำหรับเทสต์ (แก้ path ให้ตรง)
    test_image_path = "test_image.jpg"
    
    if not os.path.exists(test_image_path):
        print(f"⚠️ กรุณาหาไฟล์รูปมาใส่ในโปรเจกต์และตั้งชื่อว่า {test_image_path} ก่อนเทสต์")
        return

    try:
        vibe_keywords = extract_vibe(test_image_path)
        print(f"✅ Vibe ที่สกัดได้: {vibe_keywords}\n")
    except Exception as e:
        print(f"❌ Vision Agent พัง! Error: {e}")
        return

    # ---------------------------------------------------------
    # 2. ทดสอบ The Explorer (Search Agent - Text)
    # ---------------------------------------------------------
    print("--- [Test 2] Search Agent (Local Reviews) ---")
    try:
        context = get_local_reviews(vibe_keywords)
        print(f"✅ ดึงข้อมูลจาก Pantip/Web ได้แล้ว! ความยาวข้อความ: {len(context)} ตัวอักษร")
        print(f"ตัวอย่างข้อความ: {context[:150]}...\n")
    except Exception as e:
        print(f"❌ Search Agent พัง! (เช็ก Tavily API Key) Error: {e}")
        return

    # ---------------------------------------------------------
    # 3. ทดสอบ The Brain (Brain Agent)
    # ---------------------------------------------------------
    print("--- [Test 3] Brain Agent (JSON Generator) ---")
    try:
        places_data = generate_recommendations(context)
        if not places_data:
            print("⚠️ Brain Agent ไม่ได้คืนข้อมูลสถานที่ จึงข้ามการทดสอบหารูปภาพ")
            return

        print("✅ คัดกรอง Top 5 และสร้าง JSON สำเร็จ!")
        print(json.dumps(places_data, indent=2, ensure_ascii=False))
        print("\n")
    except Exception as e:
        print(f"❌ Brain Agent พัง! (มักจะพังเพราะ LLM คืนค่ามาไม่ใช่ JSON) Error: {e}")
        return

    # ---------------------------------------------------------
    # 4. ทดสอบ The Explorer (Search Agent - Image)
    # ---------------------------------------------------------
    print("--- [Test 4] Search Agent (Image Fetching) ---")
    try:
        # ทดลองดึงรูปของสถานที่แรกในลิสต์
        first_place_keyword = places_data[0]["search_keyword"]
        img_url = get_place_image(first_place_keyword)
        print(f"✅ หารูปภาพของ '{first_place_keyword}' สำเร็จ!")
        print(f"🔗 URL รูปภาพ: {img_url}\n")
    except Exception as e:
        print(f"❌ ระบบหารูปภาพพัง! Error: {e}")
        return

    print("🎉 ยินดีด้วย! ฟังก์ชันหลังบ้านทำงานเชื่อมต่อกันสมบูรณ์แบบ 100% เตรียมเอาไปเสียบหน้า UI ได้เลย!")

if __name__ == "__main__":
    run_tests()
