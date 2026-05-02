from tavily import TavilyClient
from src.config import TAVILY_API_KEY

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


PROVINCE_TO_REGION = {
    "เชียงราย": "ภาคเหนือ",
    "เชียงใหม่": "ภาคเหนือ",
    "น่าน": "ภาคเหนือ",
    "พะเยา": "ภาคเหนือ",
    "แพร่": "ภาคเหนือ",
    "แม่ฮ่องสอน": "ภาคเหนือ",
    "ลำปาง": "ภาคเหนือ",
    "ลำพูน": "ภาคเหนือ",
    "อุตรดิตถ์": "ภาคเหนือ",
    "กำแพงเพชร": "ภาคกลาง",
    "ชัยนาท": "ภาคกลาง",
    "นครนายก": "ภาคกลาง",
    "นครปฐม": "ภาคกลาง",
    "นครสวรรค์": "ภาคกลาง",
    "นนทบุรี": "ภาคกลาง",
    "ปทุมธานี": "ภาคกลาง",
    "พระนครศรีอยุธยา": "ภาคกลาง",
    "พิจิตร": "ภาคกลาง",
    "พิษณุโลก": "ภาคกลาง",
    "เพชรบูรณ์": "ภาคกลาง",
    "ลพบุรี": "ภาคกลาง",
    "สมุทรปราการ": "ภาคกลาง",
    "สมุทรสงคราม": "ภาคกลาง",
    "สมุทรสาคร": "ภาคกลาง",
    "สระบุรี": "ภาคกลาง",
    "สิงห์บุรี": "ภาคกลาง",
    "สุโขทัย": "ภาคกลาง",
    "สุพรรณบุรี": "ภาคกลาง",
    "อ่างทอง": "ภาคกลาง",
    "อุทัยธานี": "ภาคกลาง",
    "กรุงเทพมหานคร": "ภาคกลาง",
    "จันทบุรี": "ภาคตะวันออก",
    "ฉะเชิงเทรา": "ภาคตะวันออก",
    "ชลบุรี": "ภาคตะวันออก",
    "ตราด": "ภาคตะวันออก",
    "ปราจีนบุรี": "ภาคตะวันออก",
    "ระยอง": "ภาคตะวันออก",
    "สระแก้ว": "ภาคตะวันออก",
    "กาฬสินธุ์": "ภาคตะวันออกเฉียงเหนือ",
    "ขอนแก่น": "ภาคตะวันออกเฉียงเหนือ",
    "ชัยภูมิ": "ภาคตะวันออกเฉียงเหนือ",
    "นครพนม": "ภาคตะวันออกเฉียงเหนือ",
    "นครราชสีมา": "ภาคตะวันออกเฉียงเหนือ",
    "บึงกาฬ": "ภาคตะวันออกเฉียงเหนือ",
    "บุรีรัมย์": "ภาคตะวันออกเฉียงเหนือ",
    "มหาสารคาม": "ภาคตะวันออกเฉียงเหนือ",
    "มุกดาหาร": "ภาคตะวันออกเฉียงเหนือ",
    "ยโสธร": "ภาคตะวันออกเฉียงเหนือ",
    "ร้อยเอ็ด": "ภาคตะวันออกเฉียงเหนือ",
    "เลย": "ภาคตะวันออกเฉียงเหนือ",
    "ศรีสะเกษ": "ภาคตะวันออกเฉียงเหนือ",
    "สกลนคร": "ภาคตะวันออกเฉียงเหนือ",
    "สุรินทร์": "ภาคตะวันออกเฉียงเหนือ",
    "หนองคาย": "ภาคตะวันออกเฉียงเหนือ",
    "หนองบัวลำภู": "ภาคตะวันออกเฉียงเหนือ",
    "อำนาจเจริญ": "ภาคตะวันออกเฉียงเหนือ",
    "อุดรธานี": "ภาคตะวันออกเฉียงเหนือ",
    "อุบลราชธานี": "ภาคตะวันออกเฉียงเหนือ",
    "กาญจนบุรี": "ภาคตะวันตก",
    "ตาก": "ภาคตะวันตก",
    "ประจวบคีรีขันธ์": "ภาคตะวันตก",
    "เพชรบุรี": "ภาคตะวันตก",
    "ราชบุรี": "ภาคตะวันตก",
    "กระบี่": "ภาคใต้",
    "ชุมพร": "ภาคใต้",
    "ตรัง": "ภาคใต้",
    "นครศรีธรรมราช": "ภาคใต้",
    "นราธิวาส": "ภาคใต้",
    "ปัตตานี": "ภาคใต้",
    "พังงา": "ภาคใต้",
    "พัทลุง": "ภาคใต้",
    "ภูเก็ต": "ภาคใต้",
    "ยะลา": "ภาคใต้",
    "ระนอง": "ภาคใต้",
    "สงขลา": "ภาคใต้",
    "สตูล": "ภาคใต้",
    "สุราษฎร์ธานี": "ภาคใต้",
}


def _normalize_location_filter(region="", province=""):
    province = str(province or "").strip()
    region = str(region or "").strip()

    if not province:
        return region, None

    expected_region = PROVINCE_TO_REGION.get(province)
    if not expected_region:
        return province, None

    if region and region != expected_region:
        warning = (
            f"เลือกจังหวัด '{province}' ซึ่งอยู่ใน '{expected_region}' "
            f"แต่เลือกภาคเป็น '{region}' ระบบจึงใช้ '{expected_region}' แทน"
        )
        print(f"⚠️ Search Agent Location Warning: {warning}")
        return f"{province} {expected_region}", warning

    return f"{province} {expected_region}", None


def get_location_filter(region="", province=""):
    return _normalize_location_filter(region=region, province=province)


def _split_image_keywords(vibe_keywords):
    keywords = [
        keyword.strip()
        for keyword in str(vibe_keywords).replace("\n", ",").split(",")
        if keyword.strip()
    ]
    return {
        "all": keywords,
        "vibes": keywords[:5],
        "visible_objects": keywords[5:8],
    }


def _compact_terms(terms, limit=None):
    selected_terms = [term for term in terms if term]
    if limit:
        selected_terms = selected_terms[:limit]
    return " ".join(selected_terms)


def _build_review_queries(keyword_groups, location_keyword):
    vibes = keyword_groups["vibes"]
    visible_objects = keyword_groups["visible_objects"]
    all_keywords = keyword_groups["all"]

    location = location_keyword or "ประเทศไทย"
    landscape = vibes[0] if vibes else ""
    mood_terms = _compact_terms(vibes[1:], limit=4)
    object_terms = _compact_terms(visible_objects)
    all_terms = _compact_terms(all_keywords)

    queries = [
        (
            f"สถานที่ท่องเที่ยวไทย {location} รีวิว {landscape} "
            f"{object_terms} {mood_terms}"
        ),
        (
            f"Unseen Thailand {location} {all_terms} "
            "สถานที่จริง บรรยากาศคล้ายรูป"
        ),
        (
            f"รีวิว Pantip ที่เที่ยว {location} {landscape} "
            f"{object_terms} {mood_terms}"
        ),
    ]

    cleaned_queries = []
    seen = set()
    for query in queries:
        clean_query = " ".join(query.split())
        if clean_query and clean_query not in seen:
            cleaned_queries.append(clean_query)
            seen.add(clean_query)
    return cleaned_queries


def _format_context(
    keyword_groups,
    queries,
    results,
    target_location,
    location_warning=None,
):
    if not results:
        return "ไม่พบข้อมูลที่ตรงกับ Vibe นี้"

    header = [
        "TARGET_LOCATION: " + (target_location or "ประเทศไทย"),
        "IMAGE_KEYWORDS: " + ", ".join(keyword_groups["all"]),
        "VIBE_KEYWORDS: " + ", ".join(keyword_groups["vibes"]),
        "VISIBLE_OBJECT_OR_PLACE_KEYWORDS: "
        + ", ".join(keyword_groups["visible_objects"]),
        "LOCATION_WARNING: " + location_warning if location_warning else "",
        "SEARCH_QUERIES:",
        *[f"- {query}" for query in queries],
        "",
        "SEARCH_RESULTS:",
    ]

    result_blocks = []
    for index, item in enumerate(results, start=1):
        title = item.get("title", "").strip()
        url = item.get("url", "").strip()
        content = item.get("content", "").strip()
        if not content:
            continue

        result_blocks.append(
            "\n".join(
                [
                    f"[{index}] {title}",
                    f"URL: {url}",
                    content,
                ]
            ).strip()
        )

    if not result_blocks:
        return "ไม่พบข้อมูลที่ตรงกับ Vibe นี้"

    return "\n".join(header) + "\n\n---\n\n" + "\n\n---\n\n".join(result_blocks)


def get_local_reviews(vibe_keywords, region="", province=""):
    """
    รับคีย์เวิร์ด + ภาค/จังหวัด -> ค้นหา Pantip/เว็บไทย ด้วย Tavily -> คืนค่า Text (Context)
    """
    try:
        location_keyword, location_warning = _normalize_location_filter(
            region=region,
            province=province,
        )
        keyword_groups = _split_image_keywords(vibe_keywords)
        queries = _build_review_queries(keyword_groups, location_keyword)

        all_results = []
        seen_urls = set()

        for query in queries:
            response = tavily_client.search(
                query=query,
                search_depth="advanced",
                max_results=4
            )

            for item in response.get("results", []):
                url = item.get("url", "")
                title = item.get("title", "")
                dedupe_key = url or title
                if dedupe_key in seen_urls:
                    continue
                seen_urls.add(dedupe_key)
                all_results.append(item)

        return _format_context(
            keyword_groups,
            queries,
            all_results[:8],
            target_location=location_keyword,
            location_warning=location_warning,
        )

    except Exception as e:
        print(f"❌ Search Agent (Reviews) Error: {e}")
        return ""

def get_place_image(search_keyword):
    """
    รับชื่อสถานที่ -> ค้นหารูปภาพด้วย Tavily -> คืนค่า URL รูปภาพ
    """
    try:
        query = f"{search_keyword} Thailand travel destination landscape real photo"
        response = tavily_client.search(
            query=query,
            search_depth="basic",
            include_images=True,
            max_results=5
        )
        
        images = response.get("images", [])
        
        valid_images = [
            img for img in images 
            if isinstance(img, str) and img.startswith("http")
        ]
        
        if valid_images:
            return valid_images[0] 
        else:
            return "https://placehold.co/600x190/eeeeee/999999?text=No+Image+Found"

    except Exception as e:
        print(f"❌ Search Agent (Image) Error: {e}")
        return "https://placehold.co/600x190/ffcccc/cc0000?text=API+Limit+Reached"
