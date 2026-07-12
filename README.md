# 📚 Smart AI Study Assistant 
Live demo: https://smart-ai-study-assistant.streamlit.app/

**Handwritten Notes → AI Study Pack → Flashcards → Export**

A fully-featured, multi-page Streamlit application that transforms handwritten or typed notes into complete study materials using GLM-OCR (cloud) and Google Gemini.

---

## ✨ What's New in v2

| Feature | v1 | v2 |
|---|---|---|
| Summary / Keywords / Questions | ✅ | ✅ Enhanced |
| Topic detection | ❌ | ✅ |
| Difficulty rating | ❌ | ✅ |
| Key concept definitions | ❌ | ✅ |
| Memory aids / Mnemonics | ❌ | ✅ |
| Flashcard study mode | ❌ | ✅ |
| Session history | ❌ | ✅ |
| Export (MD / TXT / JSON) | ❌ | ✅ |
| Multi-page navigation | ❌ | ✅ |
| Step progress UI | ❌ | ✅ |
| Live word count | ❌ | ✅ |
| Image enhancement toggle | ✅ | ✅ |

---

## 📁 Project Structure

```
smart_ai_study_assistant_v2/
│
├── app.py                        ← Page 1: Analyze (main)
├── requirements.txt
├── .env.example
├── glmocr_config.yaml            ← GLM-OCR MaaS config
│
├── pages/
│   ├── 1_🃏_Flashcards.py        ← Page 2: Interactive flashcards
│   ├── 2_📖_History.py           ← Page 3: Browse past sessions
│   └── 3_📤_Export.py            ← Page 4: Download MD/TXT/JSON
│
├── services/
│   ├── ocr_service.py            ← GLM-OCR cloud client
│   ├── gemini_service.py         ← Enhanced Gemini prompting
│   ├── text_utils.py             ← Text cleaning
│   └── session_service.py        ← History persistence (JSON)
│
├── utils/
│   ├── image_preprocessing.py   ← 5-step image pipeline
│   └── export_utils.py           ← MD / TXT / JSON exporters
│
├── components/
│   └── styles.py                 ← Shared CSS + UI components
│
└── data/
    └── history.json              ← Auto-created on first analysis
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (multi-page) |
| OCR | GLM-OCR via Zhipu MaaS (no GPU!) |
| AI Analysis | Google Gemini 1.5 Flash |
| Image Processing | Pillow, NumPy |
| History Storage | Local JSON file |
| Fonts | Sora, JetBrains Mono, Lora (Google Fonts) |

---

## 🚀 Installation

```bash
# 1. Clone / unzip and enter directory
cd smart_ai_study_assistant_v2

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
cp .env.example .env
# Edit .env and fill in your keys:
#   ZHIPU_API_KEY  → https://open.bigmodel.cn
#   GEMINI_API_KEY → https://aistudio.google.com/app/apikey

# 5. Run
streamlit run app.py
```

---

## 🔑 API Keys

| Key | Where | Cost |
|---|---|---|
| `ZHIPU_API_KEY` | [open.bigmodel.cn](https://open.bigmodel.cn) | Free tier available |
| `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com/app/apikey) | Free tier available |

You can also paste them directly into the sidebar at runtime.

---

## 📖 User Flow

```
Upload Image / Paste Text
         ↓
   GLM-OCR (cloud)  ←  Zhipu AI API
         ↓
   Text Cleaning
         ↓
   Gemini Analysis  ←  Google AI API
         ↓
 ┌───────────────────────────────────┐
 │  Summary · Keywords · Questions   │
 │  Key Concepts · Mnemonics · Topic │
 └───────────────────────────────────┘
         ↓
  Auto-saved to History
         ↓
  Flashcards  →  Export (MD/TXT/JSON)
```

---

## 🔮 Future Enhancements

- [ ] PDF multi-page upload
- [ ] FastAPI backend + React frontend
- [ ] PostgreSQL session storage
- [ ] User accounts / authentication
- [ ] Chatbot tutor mode (ask questions about your notes)
- [ ] Spaced repetition scheduling for flashcards
- [ ] Progress analytics dashboard
- [ ] Multilingual OCR support
- [ ] Fine-tuned education-specific LLM

---

## 🎓 Architecture Notes (for viva/interview)

> The system is split into **four independent layers**: image preprocessing (Pillow), OCR (GLM-OCR cloud API via `glmocr` SDK), AI analysis (Gemini), and persistence (JSON). Each can be swapped independently.

> The Gemini prompt enforces a **strict JSON schema** and returns seven fields: summary, keywords, questions, topic, difficulty, key_concepts, and mnemonics. Defensive parsing recovers from malformed responses.

> Session history uses a **local JSON file** with a 50-entry cap. The architecture is designed to migrate to SQLite or PostgreSQL without changing any service interfaces.

> The multi-page Streamlit structure mirrors how a **FastAPI + React** migration would work: each page becomes an API endpoint + frontend component, with shared service modules unchanged.
