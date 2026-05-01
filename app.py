import html
import gradio as gr
from src.agents.vision_agent import extract_vibe
from src.agents.search_agent import get_local_reviews, get_place_image
from src.agents.brain_agent import generate_recommendations


def build_card_html(place: dict, img_url: str) -> str:
    rank = place.get("rank", "")
    name = html.escape(place.get("place_name", ""))
    desc = html.escape(place.get("description", ""))
    locals_say = html.escape(place.get("what_locals_say", ""))
    transit = html.escape(place.get("local_transit", ""))

    return f"""
<div style="
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,0.10);
  margin-bottom: 24px;
  font-family: 'Sarabun', sans-serif;
">
  <div style="position: relative;">
    <img src="{img_url}"
         style="width:100%; height:220px; object-fit:cover; display:block;"
         onerror="this.src='https://via.placeholder.com/600x220?text=No+Image'">
    <div style="
      position: absolute; top: 14px; left: 14px;
      background: #FF6B35;
      color: white;
      font-size: 0.85rem;
      font-weight: 700;
      padding: 4px 14px;
      border-radius: 20px;
    ">#{rank}</div>
  </div>
  <div style="padding: 18px 20px;">
    <h2 style="margin:0 0 8px; font-size:1.2rem; color:#1a1a2e;">{name}</h2>
    <p style="margin:0 0 14px; color:#555; font-size:0.95rem; line-height:1.6;">{desc}</p>
    <div style="
      background:#FFF3E0;
      border-left: 4px solid #FF9800;
      border-radius: 4px;
      padding: 10px 14px;
      margin-bottom: 10px;
    ">
      <span style="font-size:0.8rem; font-weight:700; color:#E65100;">คนท้องถิ่นบอกว่า</span>
      <p style="margin:4px 0 0; font-size:0.9rem; color:#5D4037;">{locals_say}</p>
    </div>
    <div style="
      background:#E8F5E9;
      border-left: 4px solid #4CAF50;
      border-radius: 4px;
      padding: 10px 14px;
    ">
      <span style="font-size:0.8rem; font-weight:700; color:#2E7D32;">การเดินทาง</span>
      <p style="margin:4px 0 0; font-size:0.9rem; color:#1B5E20;">{transit}</p>
    </div>
  </div>
</div>"""


def build_cards_html(places: list) -> str:
    cards = "".join(build_card_html(p, p["img_url"]) for p in places)
    return f'<div style="max-width:720px; margin:0 auto; padding:10px 0;">{cards}</div>'


def loading_html(message: str) -> str:
    return f'<div style="text-align:center; padding:40px; color:#888; font-size:1rem;">{message}</div>'


def process_pipeline(image):
    if image is None:
        yield "กรุณาอัปโหลดรูปภาพก่อนนะคะ", ""
        return

    yield "กำลังวิเคราะห์ภาพ...", ""
    vibe = extract_vibe(image)
    if not vibe:
        yield "ไม่สามารถวิเคราะห์รูปภาพได้ กรุณาลองใหม่", ""
        return

    yield vibe, loading_html("กำลังค้นหาข้อมูลสถานที่จากเว็บ...")
    context = get_local_reviews(vibe)

    yield vibe, loading_html("AI กำลังคัดเลือกสถานที่ที่เหมาะกับ Vibe ของคุณ...")
    places = generate_recommendations(context)

    if not places:
        yield vibe, '<p style="color:#e53935; padding:20px;">ไม่สามารถสร้างคำแนะนำได้ กรุณาลองใหม่อีกครั้ง</p>'
        return

    yield vibe, loading_html("กำลังดึงรูปภาพสถานที่...")
    for place in places:
        place["img_url"] = get_place_image(place.get("search_keyword", place.get("place_name", "")))

    yield vibe, build_cards_html(places)


with gr.Blocks(theme=gr.themes.Soft(), title="Dream Tour") as demo:
    gr.Markdown("""
# 🌏 Dream Tour — ค้นหาสถานที่ในฝัน
อัปโหลดรูปภาพที่สื่อถึง **บรรยากาศ (Vibe)** ที่คุณอยากไป แล้วให้ AI แนะนำสถานที่ท่องเที่ยว Unseen ในประเทศไทยที่เหมาะกับคุณ
""")

    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(
                type="filepath",
                label="อัปโหลดรูปภาพ Vibe ที่คุณชอบ",
                height=300,
            )
            submit_btn = gr.Button("ค้นหาสถานที่ในฝัน ✨", variant="primary", size="lg")

    vibe_output = gr.Textbox(
        label="Vibe Keywords ที่สกัดได้",
        interactive=False,
        placeholder="คีย์เวิร์ดจะปรากฏที่นี่หลังวิเคราะห์รูปภาพ...",
    )
    cards_output = gr.HTML(label="Top 5 สถานที่แนะนำ")

    submit_btn.click(
        fn=process_pipeline,
        inputs=[image_input],
        outputs=[vibe_output, cards_output],
    )

if __name__ == "__main__":
    demo.launch()
