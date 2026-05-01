import html
import gradio as gr
from src.agents.vision_agent import extract_vibe
from src.agents.search_agent import (
    get_local_reviews,
    get_location_filter,
    get_place_image,
)
from src.agents.brain_agent import generate_recommendations


ZONE_CHOICES = [
    ("ทั้งประเทศ", ""),
    ("ภาคเหนือ", "ภาคเหนือ"),
    ("ภาคกลาง", "ภาคกลาง"),
    ("ภาคตะวันออก", "ภาคตะวันออก"),
    ("ภาคตะวันออกเฉียงเหนือ (อีสาน)", "ภาคตะวันออกเฉียงเหนือ"),
    ("ภาคตะวันตก", "ภาคตะวันตก"),
    ("ภาคใต้", "ภาคใต้"),
]

PROVINCE_CHOICES = [
    ("ทุกจังหวัด", ""),
    ("กระบี่", "กระบี่"), ("กรุงเทพมหานคร", "กรุงเทพมหานคร"),
    ("กาญจนบุรี", "กาญจนบุรี"), ("กาฬสินธุ์", "กาฬสินธุ์"),
    ("กำแพงเพชร", "กำแพงเพชร"), ("ขอนแก่น", "ขอนแก่น"),
    ("จันทบุรี", "จันทบุรี"), ("ฉะเชิงเทรา", "ฉะเชิงเทรา"),
    ("ชลบุรี", "ชลบุรี"), ("ชัยนาท", "ชัยนาท"),
    ("ชัยภูมิ", "ชัยภูมิ"), ("ชุมพร", "ชุมพร"),
    ("เชียงราย", "เชียงราย"), ("เชียงใหม่", "เชียงใหม่"),
    ("ตรัง", "ตรัง"), ("ตราด", "ตราด"), ("ตาก", "ตาก"),
    ("นครนายก", "นครนายก"), ("นครปฐม", "นครปฐม"),
    ("นครพนม", "นครพนม"), ("นครราชสีมา", "นครราชสีมา"),
    ("นครศรีธรรมราช", "นครศรีธรรมราช"), ("นครสวรรค์", "นครสวรรค์"),
    ("นนทบุรี", "นนทบุรี"), ("นราธิวาส", "นราธิวาส"), ("น่าน", "น่าน"),
    ("บึงกาฬ", "บึงกาฬ"), ("บุรีรัมย์", "บุรีรัมย์"),
    ("ปทุมธานี", "ปทุมธานี"), ("ประจวบคีรีขันธ์", "ประจวบคีรีขันธ์"),
    ("ปราจีนบุรี", "ปราจีนบุรี"), ("ปัตตานี", "ปัตตานี"),
    ("พระนครศรีอยุธยา", "พระนครศรีอยุธยา"), ("พะเยา", "พะเยา"),
    ("พังงา", "พังงา"), ("พัทลุง", "พัทลุง"), ("พิจิตร", "พิจิตร"),
    ("พิษณุโลก", "พิษณุโลก"), ("เพชรบุรี", "เพชรบุรี"),
    ("เพชรบูรณ์", "เพชรบูรณ์"), ("แพร่", "แพร่"), ("ภูเก็ต", "ภูเก็ต"),
    ("มหาสารคาม", "มหาสารคาม"), ("มุกดาหาร", "มุกดาหาร"),
    ("แม่ฮ่องสอน", "แม่ฮ่องสอน"), ("ยโสธร", "ยโสธร"), ("ยะลา", "ยะลา"),
    ("ร้อยเอ็ด", "ร้อยเอ็ด"), ("ระนอง", "ระนอง"), ("ระยอง", "ระยอง"),
    ("ราชบุรี", "ราชบุรี"), ("ลพบุรี", "ลพบุรี"), ("ลำปาง", "ลำปาง"),
    ("ลำพูน", "ลำพูน"), ("เลย", "เลย"), ("ศรีสะเกษ", "ศรีสะเกษ"),
    ("สกลนคร", "สกลนคร"), ("สงขลา", "สงขลา"), ("สตูล", "สตูล"),
    ("สมุทรปราการ", "สมุทรปราการ"), ("สมุทรสงคราม", "สมุทรสงคราม"),
    ("สมุทรสาคร", "สมุทรสาคร"), ("สระแก้ว", "สระแก้ว"),
    ("สระบุรี", "สระบุรี"), ("สิงห์บุรี", "สิงห์บุรี"),
    ("สุโขทัย", "สุโขทัย"), ("สุพรรณบุรี", "สุพรรณบุรี"),
    ("สุราษฎร์ธานี", "สุราษฎร์ธานี"), ("สุรินทร์", "สุรินทร์"),
    ("หนองคาย", "หนองคาย"), ("หนองบัวลำภู", "หนองบัวลำภู"),
    ("อ่างทอง", "อ่างทอง"), ("อำนาจเจริญ", "อำนาจเจริญ"),
    ("อุดรธานี", "อุดรธานี"), ("อุตรดิตถ์", "อุตรดิตถ์"),
    ("อุทัยธานี", "อุทัยธานี"), ("อุบลราชธานี", "อุบลราชธานี"),
]


def build_card_html(place: dict, img_url: str) -> str:
    rank = place.get("rank", "")
    name = html.escape(place.get("place_name", ""))
    desc = html.escape(place.get("description", ""))
    locals_say = html.escape(place.get("what_locals_say", ""))
    transit = html.escape(place.get("local_transit", ""))
    maps_query = (place.get("place_name", "") + " ประเทศไทย").replace(" ", "+")
    maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"

    return f"""
<div style="
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  margin-bottom: 20px;
  font-family: 'Sarabun', sans-serif;
">
  <div style="position: relative;">
    <img src="{img_url}"
         style="width:100%; height:190px; object-fit:cover; display:block;"
         onerror="this.src='https://via.placeholder.com/600x190?text=No+Image'">
    <div style="
      position: absolute; top: 12px; left: 12px;
      background: #FF6B35; color: white;
      font-size: 0.82rem; font-weight: 700;
      padding: 3px 12px; border-radius: 20px;
    ">#{rank}</div>
    <a href="{maps_url}" target="_blank" style="
      position: absolute; top: 12px; right: 12px;
      background: white; color: #1a73e8;
      font-size: 0.78rem; font-weight: 600;
      padding: 3px 10px; border-radius: 20px;
      text-decoration: none;
      box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    ">📍 ดูบน Maps</a>
  </div>
  <div style="padding: 16px 18px;">
    <h2 style="margin:0 0 6px; font-size:1.1rem; color:#1a1a2e;">{name}</h2>
    <p style="margin:0 0 12px; color:#555; font-size:0.9rem; line-height:1.6;">{desc}</p>
    <div style="
      background:#FFF3E0; border-left: 4px solid #FF9800;
      border-radius: 4px; padding: 8px 12px; margin-bottom: 8px;
    ">
      <span style="font-size:0.75rem; font-weight:700; color:#E65100;">คนท้องถิ่นบอกว่า</span>
      <p style="margin:3px 0 0; font-size:0.87rem; color:#5D4037;">{locals_say}</p>
    </div>
    <div style="
      background:#E8F5E9; border-left: 4px solid #4CAF50;
      border-radius: 4px; padding: 8px 12px;
    ">
      <span style="font-size:0.75rem; font-weight:700; color:#2E7D32;">การเดินทาง</span>
      <p style="margin:3px 0 0; font-size:0.87rem; color:#1B5E20;">{transit}</p>
    </div>
  </div>
</div>"""


def build_cards_html(places: list) -> str:
    cards = "".join(build_card_html(p, p["img_url"]) for p in places)
    return f'<div style="padding: 4px 0;">{cards}</div>'


def build_map_html(places: list) -> str:
    if not places:
        return ""
    first_place = places[0].get("place_name", "Thailand")
    query = (first_place + " ประเทศไทย").replace(" ", "+")
    return f"""
<div style="margin-top: 4px;">
  <div style="
    font-family:'Sarabun',sans-serif;
    font-size:0.95rem; font-weight:600;
    color:#1a1a2e; margin-bottom:10px;
  ">📍 แผนที่สถานที่อันดับ 1</div>
  <iframe
    src="https://maps.google.com/maps?q={query}&output=embed&hl=th"
    width="100%" height="320"
    style="border:0; border-radius:12px; box-shadow:0 4px 20px rgba(0,0,0,0.10); display:block;"
    allowfullscreen="" loading="lazy"
    referrerpolicy="no-referrer-when-downgrade">
  </iframe>
  <p style="
    font-family:'Sarabun',sans-serif;
    font-size:0.78rem; color:#999;
    margin-top:6px; text-align:center;
  ">กดปุ่ม 📍 ดูบน Maps ในแต่ละการ์ดเพื่อดูตำแหน่งสถานที่นั้น ๆ</p>
</div>"""


def loading_html(message: str) -> str:
    return f"""
<div style="
  text-align:center; padding:60px 20px;
  color:#999; font-size:0.95rem;
  font-family:'Sarabun',sans-serif;
">{message}</div>"""


def process_pipeline(image, zone, province):
    if image is None:
        yield "กรุณาอัปโหลดรูปภาพก่อนนะคะ", "", ""
        return

    yield "กำลังวิเคราะห์ภาพ...", loading_html("รอสักครู่..."), ""
    vibe = extract_vibe(image)
    if not vibe:
        yield "ไม่สามารถวิเคราะห์รูปภาพได้ กรุณาลองใหม่", "", ""
        return

    yield vibe, loading_html("กำลังค้นหาข้อมูลสถานที่จากเว็บ..."), ""
    context = get_local_reviews(vibe, region=zone, province=province)
    target_location, _ = get_location_filter(region=zone, province=province)

    yield vibe, loading_html("AI กำลังคัดเลือกสถานที่ที่เหมาะกับ Vibe ของคุณ..."), ""
    places = generate_recommendations(context, vibe, target_location=target_location)

    if not places:
        yield (
            vibe,
            '<p style="color:#e53935; padding:20px; font-family:Sarabun,sans-serif;">ไม่สามารถสร้างคำแนะนำได้ กรุณาลองใหม่อีกครั้ง</p>',
            "",
        )
        return

    yield vibe, loading_html("กำลังดึงรูปภาพสถานที่..."), ""
    for place in places:
        place["img_url"] = get_place_image(
            place.get("search_keyword", place.get("place_name", ""))
        )

    yield vibe, build_cards_html(places), build_map_html(places)


CSS = """
body { font-family: 'Sarabun', sans-serif; }
#left-col { position: sticky; top: 16px; }
.gradio-container { max-width: 1400px !important; }
"""

with gr.Blocks(theme=gr.themes.Soft(), title="Dream Tour", css=CSS) as demo:
    gr.Markdown("""
# 🌏 Dream Tour — ค้นหาสถานที่ในฝัน
อัปโหลดรูปภาพที่สื่อถึง **บรรยากาศ (Vibe)** ที่คุณอยากไป แล้วให้ AI แนะนำสถานที่ท่องเที่ยว Unseen ในประเทศไทยที่เหมาะกับคุณ
""")

    with gr.Row(equal_height=False):
        # ---- Left panel ----
        with gr.Column(scale=1, min_width=300, elem_id="left-col"):
            image_input = gr.Image(
                type="filepath",
                label="อัปโหลดรูปภาพ Vibe ที่คุณชอบ",
                height=260,
            )
            zone_input = gr.Dropdown(
                choices=ZONE_CHOICES,
                value="",
                label="ภาค (Zone)",
                info="กรองตามภูมิภาคของประเทศไทย",
            )
            province_input = gr.Dropdown(
                choices=PROVINCE_CHOICES,
                value="",
                label="จังหวัด (Province)",
                info="กรองตามจังหวัดที่ต้องการ",
            )
            vibe_output = gr.Textbox(
                label="Vibe Keywords ที่สกัดได้",
                interactive=False,
                placeholder="คีย์เวิร์ดจะปรากฏที่นี่หลังวิเคราะห์รูปภาพ...",
                lines=3,
            )
            submit_btn = gr.Button("ค้นหาสถานที่ในฝัน ✨", variant="primary", size="lg")

        # ---- Right panel ----
        with gr.Column(scale=2):
            gr.Markdown("### Top 5 สถานที่แนะนำ")
            cards_output = gr.HTML()
            map_output = gr.HTML()

    submit_btn.click(
        fn=process_pipeline,
        inputs=[image_input, zone_input, province_input],
        outputs=[vibe_output, cards_output, map_output],
    )

if __name__ == "__main__":
    demo.launch()
