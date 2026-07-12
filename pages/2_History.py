"""
History — browse and revisit past study sessions.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="Study Assistant — History",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from components.styles import (
    inject_styles, hero, empty_state, topic_badge, difficulty_badge,
    keyword_chips, question_list, summary_block, ocr_block, stat_row,
)
from services.session_service import (
    load_history, delete_session, clear_history, format_timestamp,
)

inject_styles()

hero("📖 Study History", "Browse all your past sessions. Click any entry to review its full analysis.")

sessions = load_history()

if not sessions:
    empty_state(
        "📭",
        "No history yet",
        "After running your first analysis on the <b>Analyze</b> page,<br>your sessions will appear here automatically.",
    )
    st.stop()

# ── Toolbar ───────────────────────────────────────────────────────────────────
col_count, col_clear = st.columns([4, 1])
with col_count:
    st.markdown(
        f"<div style='color:#64748b;font-size:0.85rem;padding-top:0.5rem'>"
        f"📚 {len(sessions)} session{'s' if len(sessions) != 1 else ''} saved"
        f"</div>",
        unsafe_allow_html=True,
    )
with col_clear:
    if st.button("🗑️ Clear All", use_container_width=True):
        clear_history()
        st.success("History cleared.")
        st.rerun()

st.divider()

# ── Session list + detail view ────────────────────────────────────────────────
if "selected_session_id" not in st.session_state:
    st.session_state.selected_session_id = None

col_list, col_detail = st.columns([1, 2], gap="large")

with col_list:
    st.markdown("**Sessions**")
    for s in sessions:
        sid = s["id"]
        ts = format_timestamp(s.get("timestamp", ""))
        topic = s.get("topic", "General")
        diff = s.get("difficulty", "Medium")
        mode = s.get("input_mode", "")
        result = s.get("result", {})
        summary_preview = (result.get("summary", "") or "")[:120] + "…"

        is_active = st.session_state.selected_session_id == sid
        border_color = "rgba(99,102,241,0.6)" if is_active else "transparent"

        st.markdown(
            f"""<div class='hist-card' style='border-color:{border_color}'>
                <div class='hist-meta'>
                    {ts} &nbsp;·&nbsp; {"📷" if mode=="Image" else "✏️"} {mode}
                    &nbsp;·&nbsp; {"🟢" if diff=="Easy" else "🟡" if diff=="Medium" else "🔴"} {diff}
                </div>
                <div class='hist-title'>🎯 {topic}</div>
                <div class='hist-preview'>{summary_preview}</div>
            </div>""",
            unsafe_allow_html=True,
        )
        if st.button(f"Open [{sid}]", key=f"open_{sid}", use_container_width=True):
            st.session_state.selected_session_id = sid
            st.rerun()

        btn_col1, btn_col2 = st.columns(2)
        with btn_col2:
            if st.button("🗑️", key=f"del_{sid}", help="Delete session"):
                delete_session(sid)
                if st.session_state.selected_session_id == sid:
                    st.session_state.selected_session_id = None
                st.rerun()

with col_detail:
    sel_id = st.session_state.selected_session_id
    sel = next((s for s in sessions if s["id"] == sel_id), None)

    if sel is None:
        st.markdown(
            "<div style='padding:4rem 2rem;text-align:center;color:#475569'>"
            "<div style='font-size:2.5rem;margin-bottom:1rem'>👈</div>"
            "<div style='font-weight:600;font-size:1rem;color:#64748b'>Select a session to view details</div>"
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        result = sel.get("result", {})
        ocr_text = sel.get("ocr_text", "")

        # Header
        st.markdown(
            f"<div style='margin-bottom:0.5rem'>"
            + topic_badge(result.get("topic", "General"))
            + "&nbsp;&nbsp;"
            + difficulty_badge(result.get("difficulty", "Medium"))
            + "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div style='color:#64748b;font-size:0.8rem;margin-bottom:1rem'>"
            f"📅 {format_timestamp(sel.get('timestamp',''))} &nbsp;·&nbsp; "
            f"📝 {sel.get('summary_length','Medium')} summary &nbsp;·&nbsp; "
            f"❓ {sel.get('num_questions',5)} questions"
            f"</div>",
            unsafe_allow_html=True,
        )

        wc = len(ocr_text.split()) if ocr_text else 0
        stat_row([
            ("📝", f"{wc} words"),
            ("🏷️", f"{len(result.get('keywords',[]))} keywords"),
            ("❓", f"{len(result.get('questions',[]))} questions"),
        ])

        t1, t2, t3, t4 = st.tabs(["📝 Summary", "🏷️ Keywords", "❓ Questions", "📄 OCR Text"])

        with t1:
            summary_block(result.get("summary", ""))
            concepts = result.get("key_concepts", [])
            if concepts:
                st.markdown("<br>**Key Concepts**", unsafe_allow_html=True)
                for c in concepts:
                    with st.expander(f"📌 {c['concept']}"):
                        st.write(c["definition"])
            mnemonics = result.get("mnemonics", [])
            if mnemonics:
                st.markdown("<br>**Memory Aids**", unsafe_allow_html=True)
                for m in mnemonics:
                    st.markdown(
                        f"<div class='mnemonic-box'><div class='label'>Mnemonic</div>{m}</div>",
                        unsafe_allow_html=True,
                    )

        with t2:
            keyword_chips(result.get("keywords", []))

        with t3:
            question_list(result.get("questions", []))

        with t4:
            if ocr_text:
                ocr_block(ocr_text)
            else:
                st.info("No OCR text saved for this session (direct text input).")
