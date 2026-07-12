"""
Export — download study materials as Markdown, plain text, or JSON.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="Study Assistant — Export",
    page_icon="📤",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from components.styles import inject_styles, hero, empty_state
from services.session_service import load_history, format_timestamp
from utils.export_utils import to_markdown, to_plain_text, to_json

inject_styles()

hero(
    "📤 Export Study Materials",
    "Download your analysis results as Markdown, plain text, or JSON for use anywhere.",
)

sessions = load_history()

if not sessions:
    empty_state(
        "📭",
        "Nothing to export yet",
        "Run an analysis on the <b>Analyze</b> page first,<br>then come back here to export your study pack.",
    )
    st.stop()

# ── Session picker ────────────────────────────────────────────────────────────
session_labels = [
    f"{s.get('topic', 'General')} — {format_timestamp(s.get('timestamp',''))}  [{s['id']}]"
    for s in sessions
]
selected_label = st.selectbox("📂 Select session to export", session_labels)
selected_idx = session_labels.index(selected_label)
session = sessions[selected_idx]
result = session.get("result", {})
ocr_text = session.get("ocr_text", "")
topic = result.get("topic", "General")
difficulty = result.get("difficulty", "Medium")
fname_base = topic.replace(" ", "_").lower()

st.divider()

col1, col2, col3 = st.columns(3, gap="medium")

# ── Markdown ──────────────────────────────────────────────────────────────────
with col1:
    st.markdown(
        "<div class='result-card'>"
        "<div style='font-size:2rem;margin-bottom:0.5rem'>📄</div>"
        "<div style='font-weight:700;font-size:1.05rem;margin-bottom:0.4rem'>Markdown</div>"
        "<div style='color:#94a3b8;font-size:0.83rem;line-height:1.5'>"
        "Perfect for Obsidian, Notion, GitHub, or any Markdown-aware editor. "
        "Includes summary, keywords, questions, concepts, and memory aids."
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    md_content = to_markdown(result, ocr_text, topic, difficulty)
    st.download_button(
        "⬇️ Download .md",
        data=md_content,
        file_name=f"{fname_base}_study_notes.md",
        mime="text/markdown",
        use_container_width=True,
        type="primary",
    )
    with st.expander("Preview"):
        st.text_area("", md_content[:1200] + ("…" if len(md_content) > 1200 else ""), height=200, disabled=True)

# ── Plain text ─────────────────────────────────────────────────────────────────
with col2:
    st.markdown(
        "<div class='result-card'>"
        "<div style='font-size:2rem;margin-bottom:0.5rem'>📝</div>"
        "<div style='font-weight:700;font-size:1.05rem;margin-bottom:0.4rem'>Plain Text</div>"
        "<div style='color:#94a3b8;font-size:0.83rem;line-height:1.5'>"
        "Universal format — readable in any editor, terminal, or email client. "
        "Clean and structured with clear section dividers."
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    txt_content = to_plain_text(result, ocr_text)
    st.download_button(
        "⬇️ Download .txt",
        data=txt_content,
        file_name=f"{fname_base}_study_notes.txt",
        mime="text/plain",
        use_container_width=True,
        type="primary",
    )
    with st.expander("Preview"):
        st.text_area("", txt_content[:1200] + ("…" if len(txt_content) > 1200 else ""), height=200, disabled=True)

# ── JSON ───────────────────────────────────────────────────────────────────────
with col3:
    st.markdown(
        "<div class='result-card'>"
        "<div style='font-size:2rem;margin-bottom:0.5rem'>🗂️</div>"
        "<div style='font-weight:700;font-size:1.05rem;margin-bottom:0.4rem'>JSON</div>"
        "<div style='color:#94a3b8;font-size:0.83rem;line-height:1.5'>"
        "Full structured data — ideal for developers, RAG pipelines, "
        "custom apps, or future database import."
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    json_content = to_json(result, ocr_text)
    st.download_button(
        "⬇️ Download .json",
        data=json_content,
        file_name=f"{fname_base}_study_notes.json",
        mime="application/json",
        use_container_width=True,
        type="primary",
    )
    with st.expander("Preview"):
        st.text_area("", json_content[:1200] + ("…" if len(json_content) > 1200 else ""), height=200, disabled=True)

# ── Bulk export ───────────────────────────────────────────────────────────────
st.divider()
st.markdown("### 📦 Export All Sessions")
if st.button("⬇️ Download All Sessions as JSON", use_container_width=True):
    import json as _json
    all_data = _json.dumps(sessions, ensure_ascii=False, indent=2)
    st.download_button(
        "Click to save",
        data=all_data,
        file_name="all_study_sessions.json",
        mime="application/json",
        use_container_width=True,
    )
