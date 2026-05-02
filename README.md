# Dream Tour

**Upload your vibe. Discover your dream destination.**

Dream Tour is an AI-powered travel recommendation web app for Thailand. Upload any image that captures the experience you want — a misty mountain, a cozy café, a beach at sunset — and the AI will recommend the top 5 matching Thai destinations, complete with local tips, transport info, food recommendations, photos, and Google Maps links.

---

## How It Works

Dream Tour uses a 3-agent AI pipeline:

1. **Vision Agent** (Google Gemini) — Analyzes the uploaded image and extracts 8 Thai vibe keywords: 5 describe mood/atmosphere, 3 describe visible objects or place types.
2. **Search Agent** (Tavily) — Uses those keywords to search real Thai travel reviews, Pantip, and travel blogs. Supports filtering by region or province.
3. **Brain Agent** (Google Gemini) — Reads the search context and keywords, then generates up to 5 ranked place recommendations in structured JSON, each with a description, local insights, transit info, food tips, and an image search keyword.

---

## Features

- **Image-to-destination** — No text input needed; just upload a mood image
- **Unseen Thailand focus** — Surfaces lesser-known gems beyond the usual tourist spots
- **Local knowledge** — Each place card shows what locals say, how to get there, and what to eat
- **Full coverage** — All 77 provinces and 6 regions of Thailand
- **Google Maps integration** — One-click directions for every recommendation
- **Real photos** — Auto-fetched via web search for each place

---

## Tech Stack

| Component | Technology |
|---|---|
| UI | Gradio |
| Vision AI | Google Gemini (`gemini-2.0-flash`) |
| Reasoning AI | Google Gemini (`gemini-2.0-flash`) |
| Web Search | Tavily AI Search |
| Image handling | Pillow |
| Environment | python-dotenv |

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/nontaphatfirm/Dream-Tour
cd Dream-Tour
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

```env
# One or more Gemini API keys, comma-separated (for quota rotation)
GEMINI_API_KEYS=your_gemini_api_key_1,your_gemini_api_key_2

# Tavily API key for web search
TAVILY_API_KEY=your_tavily_api_key_here
```

Get your keys:
- Gemini API key: [Google AI Studio](https://aistudio.google.com/app/apikey)
- Tavily API key: [Tavily](https://app.tavily.com)

### 4. Run the app

```bash
python app.py
```

The app will launch at `http://localhost:7860`.

---

## Project Structure

```
Dream-Tour/
├── app.py                  # Gradio UI and main pipeline
├── requirements.txt
├── .env.example
└── src/
    ├── config.py           # API key loading
    ├── agents/
    │   ├── vision_agent.py # Extracts vibe keywords from image (Gemini)
    │   ├── search_agent.py # Searches Thai travel reviews (Tavily)
    │   └── brain_agent.py  # Generates place recommendations (Gemini)
    └── utils/
        └── prompts.py      # Prompt templates for all agents
```

---

## Usage

1. Open the app in your browser
2. Upload an image that represents the travel vibe you want
3. Optionally filter by **region** or **province**
4. Click **Find Your Dream Places**
5. Browse the top 5 recommended destinations with photos, tips, and maps

---

## Website
- https://huggingface.co/spaces/Sarankorn/Dream_Tour

---
## 👥 Team Members (Developers)

| Profile | Name | Super AI ID | GitHub |
| :---: | :--- | :---: | :--- |
| <img src="https://avatars.githubusercontent.com/khunkhang01" width="50" style="border-radius: 50%;"> | **Khunkhang Butdapheng** | 600409 | [@khunkhang01](https://github.com/khunkhang01) |
| <img src="https://avatars.githubusercontent.com/Sarankorn2547" width="50" style="border-radius: 50%;"> | **Sarankorn Pongatsawachai** | 605562 | [@Sarankorn2547](https://github.com/Sarankorn2547) |
| <img src="https://avatars.githubusercontent.com/nontaphatfirm" width="50" style="border-radius: 50%;"> | **Nontapat Auetrongjit** | 610154 | [@nontaphatfirm](https://github.com/nontaphatfirm) |

## License

[MIT](LICENSE)
