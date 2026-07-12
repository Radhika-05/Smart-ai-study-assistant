"""
Smart AI Study Assistant v2
===========================
Main page: Upload & Analyze

Navigation:
  app.py           → Analyze (this page)
  pages/1_...py    → Flashcards
  pages/2_...py    → History
  pages/3_...py    → Export
"""

import os
import sys
import time
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from PIL import Image

# Make project root importable from any page
sys.path.insert(0, str(Path(__file__).parent))

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Study Assistant — Analyze",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.styles import (
    inject_styles, hero, step_progress, stat_row,
    keyword_chips, question_list, summary_block, ocr_block,
    topic_badge, difficulty_badge, empty_state,
)
from services.gemini_service import analyze_text
from services.ocr_service import extract_text_from_image
from services.session_service import save_session
from services.text_utils import clean_text, is_meaningful_text
from utils.image_preprocessing import preprocess_for_ocr

inject_styles()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
        # Load API keys automatically
    zhipu_key = os.getenv("ZHIPU_API_KEY", "")
    gemini_key = os.getenv("GEMINI_API_KEY", "")

    # If deployed on Streamlit Cloud, use Streamlit Secrets
    try:
        if "ZHIPU_API_KEY" in st.secrets:
            zhipu_key = st.secrets["ZHIPU_API_KEY"]

        if "GEMINI_API_KEY" in st.secrets:
            gemini_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        # Running locally without Streamlit Secrets
        pass

    st.divider()
    st.markdown("**📥 Input Mode**")
    input_mode = st.radio(
        "", options=["📷 Upload Image", "✏️ Direct Text"], label_visibility="collapsed"
    )

    st.divider()
    st.markdown("**🎛️ Analysis Settings**")
    summary_length = st.select_slider(
        "Summary depth",
        options=["Short", "Medium", "Detailed"],
        value="Medium",
    )
    num_questions = st.slider("Revision questions", 1, 15, 5)
    if "Upload" in input_mode:
        use_preprocessing = st.toggle("✨ Enhance image for OCR", value=True)

    st.divider()
    st.markdown(
        "<div style='font-size:0.75rem;color:#475569;line-height:1.6'>"
        "GLM-OCR runs on Zhipu cloud — no GPU needed.<br>"
        "Results auto-saved to History."
        "</div>",
        unsafe_allow_html=True,
    )

# ── Hero ──────────────────────────────────────────────────────────────────────
hero(
    "Smart AI Study Assistant",
    "Upload handwritten notes or paste text → GLM-OCR extracts → Gemini generates summaries, keywords, questions & more.",
    "🔬",
)


# ── State helpers ─────────────────────────────────────────────────────────────
def reset_state():
    for key in ["ocr_text", "result", "step"]:
        st.session_state.pop(key, None)


def _word_count(text: str) -> int:
    return len(text.split())


def _read_time(words: int) -> str:
    mins = max(1, round(words / 200))
    return f"{mins} min read"


# ── IMAGE MODE ────────────────────────────────────────────────────────────────
if "Upload" in input_mode:
    step = st.session_state.get("step", 0)
    STEPS = ["Upload", "Extract", "Analyse", "Done"]
    step_progress(STEPS, step)

    st.markdown("<br>", unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drop a photo of your handwritten notes",
        type=["png", "jpg", "jpeg", "webp"],
        help="Supports: handwritten, printed, mixed, scanned documents",
        on_change=reset_state,
    )

    if uploaded:
        try:
            orig = Image.open(uploaded)
        except Exception as e:
            st.error(f"Cannot open image: {e}")
            st.stop()

        col1, col2 = st.columns(2, gap="medium")
        with col1:
            st.markdown("<div class='img-card-label'>Original</div>", unsafe_allow_html=True)
            st.image(orig, use_container_width=True)
        if use_preprocessing:
            proc = preprocess_for_ocr(orig)
            with col2:
                st.markdown("<div class='img-card-label'>Enhanced for OCR</div>", unsafe_allow_html=True)
                st.image(proc, use_container_width=True)
        else:
            proc = orig

        st.markdown("<br>", unsafe_allow_html=True)
        go = st.button(
            "🚀 Run OCR + AI Analysis",
            type="primary",
            use_container_width=True,
            disabled=bool(st.session_state.get("result")),
        )

        if go:
            if not zhipu_key:
                st.error("❌ Zhipu API key missing — add it in the sidebar.")
                st.stop()
            if not gemini_key:
                st.error("❌ Gemini API key missing — add it in the sidebar.")
                st.stop()

            # ── Step 2: OCR ─────────────────────────────────────────────────
            st.session_state["step"] = 1
            with st.spinner("🔍 Extracting text with GLM-OCR..."):
                t0 = time.time()
                try:
                    raw = extract_text_from_image(proc, api_key=zhipu_key)
                except Exception as e:
                    st.error(f"OCR failed: {e}")
                    st.stop()
            ocr_ms = int((time.time() - t0) * 1000)

            if not raw:
                st.warning("⚠️ No text detected. Try enabling enhancement or using a clearer image.")
                st.stop()

            cleaned = clean_text(raw)
            if not is_meaningful_text(cleaned):
                st.warning("⚠️ Extracted text is too short for meaningful analysis.")
                st.stop()

            st.session_state["ocr_text"] = cleaned
            st.session_state["step"] = 2

            # ── Step 3: Gemini ───────────────────────────────────────────────
            with st.spinner("🤖 Analysing with Gemini..."):
                t1 = time.time()
                try:
                    result = analyze_text(
                        cleaned,
                        api_key=gemini_key,
                        summary_length=summary_length,
                        num_questions=num_questions,
                    )
                except Exception as e:
                    st.error(f"Gemini analysis failed: {e}")
                    st.stop()
            ai_ms = int((time.time() - t1) * 1000)

            # ── Save session ─────────────────────────────────────────────────
            save_session(
                result=result,
                ocr_text=cleaned,
                input_mode="Image",
                summary_length=summary_length,
                num_questions=num_questions,
                image_name=uploaded.name,
            )

            st.session_state["result"] = result
            st.session_state["step"] = 3
            st.rerun()

    # ── Display results ───────────────────────────────────────────────────────
    if "result" in st.session_state:
        step_progress(STEPS, 3)
        result = st.session_state["result"]
        ocr_text = st.session_state.get("ocr_text", "")
        wc = _word_count(ocr_text)

        st.success("✅ Analysis complete! Scroll down to explore your study materials.")

        # Meta row
        meta_html = (
            topic_badge(result.get("topic", "General"))
            + "&nbsp;&nbsp;"
            + difficulty_badge(result.get("difficulty", "Medium"))
        )
        st.markdown(f"<div style='margin:0.8rem 0'>{meta_html}</div>", unsafe_allow_html=True)

        stat_row([
            ("📝", f"{wc} words"),
            ("⏱️", _read_time(wc)),
            ("🏷️", f"{len(result.get('keywords', []))} keywords"),
            ("❓", f"{len(result.get('questions', []))} questions"),
        ])

        st.divider()

        # Tabs
        t1, t2, t3, t4, t5 = st.tabs(
            ["📝 Summary", "🏷️ Keywords", "❓ Questions", "🔑 Concepts", "💡 Mnemonics"]
        )

        with t1:
            summary_block(result.get("summary", ""))

        with t2:
            keyword_chips(result.get("keywords", []))

        with t3:
            question_list(result.get("questions", []))

        with t4:
            concepts = result.get("key_concepts", [])
            if concepts:
                for c in concepts:
                    with st.expander(f"📌 {c['concept']}"):
                        st.write(c["definition"])
            else:
                st.info("No key concepts were extracted.")

        with t5:
            mnemonics = result.get("mnemonics", [])
            if mnemonics:
                for m in mnemonics:
                    st.markdown(
                        f"<div class='mnemonic-box'><div class='label'>Memory Aid</div>{m}</div>",
                        unsafe_allow_html=True,
                    )
            else:
                st.info("No specific mnemonics generated for this content.")

        # OCR raw
        with st.expander("🔍 View Extracted OCR Text"):
            ocr_block(ocr_text)

        st.divider()
        st.markdown(
            "<div style='text-align:center;font-size:0.82rem;color:#475569'>"
            "Session saved to History · Head to <b>Flashcards</b> to quiz yourself"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("🔄 Analyse Another Image", use_container_width=True):
            reset_state()
            st.rerun()

    elif not uploaded:
        empty_state(
            "📷",
            "Upload a photo to get started",
            "Take a photo of your handwritten or printed notes and upload it above.<br>GLM-OCR will extract the text and Gemini will build your study pack.",
        )

# ── DIRECT TEXT MODE ──────────────────────────────────────────────────────────
else:
    st.markdown("### ✏️ Paste your notes below")
    text_input = st.text_area(
        "",
        placeholder="Type or paste your study notes here...",
        height=280,
        label_visibility="collapsed",
    )

    wc_live = _word_count(text_input) if text_input.strip() else 0
    if wc_live:
        st.caption(f"{wc_live} words · ~{_read_time(wc_live)}")

    if st.button("🚀 Analyse Text", type="primary", use_container_width=True):
        if not text_input.strip():
            st.error("⚠️ Please enter some notes first.")
            st.stop()
        cleaned = clean_text(text_input)
        if not is_meaningful_text(cleaned):
            st.warning("⚠️ Text too short for analysis. Please add more content.")
            st.stop()
        if not gemini_key:
            st.error("❌ Gemini API key missing — add it in the sidebar.")
            st.stop()

        with st.spinner("🤖 Analysing with Gemini..."):
            try:
                result = analyze_text(
                    cleaned,
                    api_key=gemini_key,
                    summary_length=summary_length,
                    num_questions=num_questions,
                )
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                st.stop()

        save_session(
            result=result,
            ocr_text=cleaned,
            input_mode="Text",
            summary_length=summary_length,
            num_questions=num_questions,
        )
        st.session_state["text_result"] = result
        st.session_state["text_ocr"] = cleaned
        st.rerun()

    if "text_result" in st.session_state:
        result = st.session_state["text_result"]
        ocr_text = st.session_state.get("text_ocr", "")
        st.success("✅ Analysis complete!")

        meta_html = (
            topic_badge(result.get("topic", "General"))
            + "&nbsp;&nbsp;"
            + difficulty_badge(result.get("difficulty", "Medium"))
        )
        st.markdown(f"<div style='margin:0.8rem 0'>{meta_html}</div>", unsafe_allow_html=True)
        wc = _word_count(ocr_text)
        stat_row([
            ("📝", f"{wc} words"),
            ("🏷️", f"{len(result.get('keywords', []))} keywords"),
            ("❓", f"{len(result.get('questions', []))} questions"),
        ])

        st.divider()

        t1, t2, t3, t4, t5 = st.tabs(
            ["📝 Summary", "🏷️ Keywords", "❓ Questions", "🔑 Concepts", "💡 Mnemonics"]
        )
        with t1:
            summary_block(result.get("summary", ""))
        with t2:
            keyword_chips(result.get("keywords", []))
        with t3:
            question_list(result.get("questions", []))
        with t4:
            for c in result.get("key_concepts", []):
                with st.expander(f"📌 {c['concept']}"):
                    st.write(c["definition"])
        with t5:
            for m in result.get("mnemonics", []):
                st.markdown(
                    f"<div class='mnemonic-box'><div class='label'>Memory Aid</div>{m}</div>",
                    unsafe_allow_html=True,
                )

        if st.button("🔄 Analyse New Text"):
            st.session_state.pop("text_result", None)
            st.session_state.pop("text_ocr", None)
            st.rerun()
