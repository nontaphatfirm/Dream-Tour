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
    ("All regions", ""),
    ("Northern region", "ภาคเหนือ"),
    ("Central region", "ภาคกลาง"),
    ("Eastern region", "ภาคตะวันออก"),
    ("Northeastern region (Isaan)", "ภาคตะวันออกเฉียงเหนือ"),
    ("Western region", "ภาคตะวันตก"),
    ("Southern region", "ภาคใต้"),
]

PROVINCE_CHOICES = [
    ("All provinces", ""),
    ("Krabi", "กระบี่"), ("Bangkok", "กรุงเทพมหานคร"),
    ("Kanchanaburi", "กาญจนบุรี"), ("Kalasin", "กาฬสินธุ์"),
    ("Kamphaeng Phet", "กำแพงเพชร"), ("Khon Kaen", "ขอนแก่น"),
    ("Chanthaburi", "จันทบุรี"), ("Chachoengsao", "ฉะเชิงเทรา"),
    ("Chonburi", "ชลบุรี"), ("Chai Nat", "ชัยนาท"),
    ("Chaiyaphum", "ชัยภูมิ"), ("Chumphon", "ชุมพร"),
    ("Chiang Rai", "เชียงราย"), ("Chiang Mai", "เชียงใหม่"),
    ("Trang", "ตรัง"), ("Trat", "ตราด"), ("Tak", "ตาก"),
    ("Nakhon Nayok", "นครนายก"), ("Nakhon Pathom", "นครปฐม"),
    ("Nakhon Phanom", "นครพนม"), ("Nakhon Ratchasima", "นครราชสีมา"),
    ("Nakhon Si Thammarat", "นครศรีธรรมราช"), ("Nakhon Sawan", "นครสวรรค์"),
    ("Nonthaburi", "นนทบุรี"), ("Narathiwat", "นราธิวาส"), ("Nan", "น่าน"),
    ("Bueng Kan", "บึงกาฬ"), ("Buriram", "บุรีรัมย์"),
    ("Pathum Thani", "ปทุมธานี"), ("Prachuap Khiri Khan", "ประจวบคีรีขันธ์"),
    ("Prachinburi", "ปราจีนบุรี"), ("Pattani", "ปัตตานี"),
    ("Phra Nakhon Si Ayutthaya", "พระนครศรีอยุธยา"), ("Phayao", "พะเยา"),
    ("Phang Nga", "พังงา"), ("Phatthalung", "พัทลุง"), ("Phichit", "พิจิตร"),
    ("Phitsanulok", "พิษณุโลก"), ("Phetchaburi", "เพชรบุรี"),
    ("Phetchabun", "เพชรบูรณ์"), ("Phrae", "แพร่"), ("Phuket", "ภูเก็ต"),
    ("Maha Sarakham", "มหาสารคาม"), ("Mukdahan", "มุกดาหาร"),
    ("Mae Hong Son", "แม่ฮ่องสอน"), ("Yasothon", "ยโสธร"), ("Yala", "ยะลา"),
    ("Roi Et", "ร้อยเอ็ด"), ("Ranong", "ระนอง"), ("Rayong", "ระยอง"),
    ("Ratchaburi", "ราชบุรี"), ("Lopburi", "ลพบุรี"), ("Lampang", "ลำปาง"),
    ("Lamphun", "ลำพูน"), ("Loei", "เลย"), ("Sisaket", "ศรีสะเกษ"),
    ("Sakon Nakhon", "สกลนคร"), ("Songkhla", "สงขลา"), ("Satun", "สตูล"),
    ("Samut Prakan", "สมุทรปราการ"), ("Samut Songkhram", "สมุทรสงคราม"),
    ("Samut Sakhon", "สมุทรสาคร"), ("Sa Kaeo", "สระแก้ว"),
    ("Saraburi", "สระบุรี"), ("Sing Buri", "สิงห์บุรี"),
    ("Sukhothai", "สุโขทัย"), ("Suphan Buri", "สุพรรณบุรี"),
    ("Surat Thani", "สุราษฎร์ธานี"), ("Surin", "สุรินทร์"),
    ("Nong Khai", "หนองคาย"), ("Nong Bua Lamphu", "หนองบัวลำภู"),
    ("Ang Thong", "อ่างทอง"), ("Amnat Charoen", "อำนาจเจริญ"),
    ("Udon Thani", "อุดรธานี"), ("Uttaradit", "อุตรดิตถ์"),
    ("Uthai Thani", "อุทัยธานี"), ("Ubon Ratchathani", "อุบลราชธานี"),
]


def build_card_html(place: dict, img_url: str) -> str:
    rank = place.get("rank", "")
    name = html.escape(place.get("place_name", ""))
    desc = html.escape(place.get("description", ""))
    locals_say = html.escape(place.get("what_locals_say", ""))
    transit = html.escape(place.get("local_transit", ""))
    food = html.escape(place.get("recommended_food", ""))
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
    ">📍 View on Maps</a>
  </div>
  <div style="padding: 16px 18px;">
    <h2 style="margin:0 0 6px; font-size:1.1rem; color:#1a1a2e;">{name}</h2>
    <p style="margin:0 0 12px; color:#555; font-size:0.9rem; line-height:1.6;">{desc}</p>
    <div style="
      background:#FFF3E0; border-left: 4px solid #FF9800;
      border-radius: 4px; padding: 8px 12px; margin-bottom: 8px;
    ">
      <span style="font-size:0.75rem; font-weight:700; color:#E65100;">Locals say</span>
      <p style="margin:3px 0 0; font-size:0.87rem; color:#5D4037;">{locals_say}</p>
    </div>
    <div style="
      background:#E8F5E9; border-left: 4px solid #4CAF50;
      border-radius: 4px; padding: 8px 12px; margin-bottom: 8px;
    ">
      <span style="font-size:0.75rem; font-weight:700; color:#2E7D32;">Transportation</span>
      <p style="margin:3px 0 0; font-size:0.87rem; color:#1B5E20;">{transit}</p>
    </div>
    <div style="
      background:#F3E5F5; border-left: 4px solid #9C27B0;
      border-radius: 4px; padding: 8px 12px; margin-bottom: 8px;
    ">
      <span style="font-size:0.75rem; font-weight:700; color:#7B1FA2;">Recommended Food</span>
      <p style="margin:3px 0 0; font-size:0.87rem; color:#4A148C;">{food}</p>
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
    color:white; margin-bottom:10px;
  ">📍 Map of the top place</div>
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
  ">Click the 📍 View on Maps button in each card to see the location of that place.</p>
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
        yield "Please upload an image first.", "", ""
        return

    yield "Analyzing image...", loading_html("Please wait..."), ""
    vibe = extract_vibe(image)
    if not vibe:
        yield "Unable to analyze the image. Please try again.", "", ""
        return

    yield vibe, loading_html("Searching for place information from the web..."), ""
    context = get_local_reviews(vibe, region=zone, province=province)
    target_location, _ = get_location_filter(region=zone, province=province)

    yield vibe, loading_html("AI is selecting places that match your Vibe..."), ""
    places = generate_recommendations(context, vibe, target_location=target_location)

    if not places:
        yield (
            vibe,
            '<p style="color:#e53935; padding:20px; font-family:Sarabun,sans-serif;">Unable to generate recommendations. Please try again.</p>',
            "",
        )
        return

    yield vibe, loading_html("Fetching place images..."), ""
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
# 🌏 Dream Tour — Find Your Dream Destination
Upload an image that represents the **Vibe** you want to experience, and let AI recommend unseen tourist spots in Thailand that suit you.
""")

    with gr.Row(equal_height=False):
        # ---- Left panel ----
        with gr.Column(scale=1, min_width=300, elem_id="left-col"):
            image_input = gr.Image(
                type="filepath",
                label="Upload an image of the Vibe you like",
                height=260,
            )
            zone_input = gr.Dropdown(
                choices=ZONE_CHOICES,
                value="",
                label="Region (Zone)",
                info="Filter by region of Thailand",
            )
            province_input = gr.Dropdown(
                choices=PROVINCE_CHOICES,
                value="",
                label="Province",
                info="Filter by desired province",
            )
            vibe_output = gr.Textbox(
                label="Extracted Vibe Keywords",
                interactive=False,
                placeholder="Keywords will appear here after analyzing the image...",
                lines=3,
            )
            submit_btn = gr.Button("Find Your Dream Places ✨", variant="primary", size="lg")

        # ---- Right panel ----
        with gr.Column(scale=2, elem_id="right-col"):
            gr.Markdown("### Top 5 Recommended Places")
            cards_output = gr.HTML()
            map_output = gr.HTML()

    submit_btn.click(
        fn=process_pipeline,
        inputs=[image_input, zone_input, province_input],
        outputs=[vibe_output, cards_output, map_output],
    )

if __name__ == "__main__":
    demo.launch()
