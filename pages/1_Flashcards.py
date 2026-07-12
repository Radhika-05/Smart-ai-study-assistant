"""
Flashcards — interactive flip-card study mode.
Reads from the most recent session saved to History.
"""

import sys
import random
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="Study Assistant — Flashcards",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from components.styles import inject_styles, hero, empty_state
from services.session_service import load_history

inject_styles()

# ── Extra card CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
.fc-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1rem; }
.fc-wrap { background: linear-gradient(135deg, #161c2d, #1d1040); border: 1px solid #2e3a55;
           border-radius: 16px; padding: 1.8rem 1.5rem; text-align: center; cursor: pointer;
           transition: all 0.25s; min-height: 160px; display: flex; flex-direction: column;
           align-items: center; justify-content: center; gap: 0.5rem; }
.fc-wrap:hover { transform: translateY(-3px); border-color: rgba(99,102,241,0.55);
                 box-shadow: 0 8px 30px rgba(0,0,0,0.4); }
.fc-type { font-size: 0.68rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #64748b; }
.fc-text { font-size: 1rem; font-weight: 600; color: #e2e8f0; line-height: 1.45; }
.fc-icon { font-size: 1.6rem; }
.q-reveal-box { background: linear-gradient(135deg, #0f2a1a, #1a0f30); border: 1px solid rgba(16,185,129,0.4);
                border-radius: 12px; padding: 1.2rem 1.4rem; margin-top: 0.6rem;
                font-size: 0.9rem; color: #a7f3d0; line-height: 1.6; }
.score-bar { background: #0f1420; border: 1px solid #232b42; border-radius: 12px; padding: 1.2rem 1.5rem;
             display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem; }
</style>
""", unsafe_allow_html=True)

hero("🃏 Flashcards", "Quiz yourself on keywords and revision questions from your latest study session.")

# ── Load latest session ───────────────────────────────────────────────────────
history = load_history()

if not history:
    empty_state(
        "📚",
        "No study sessions yet",
        "Head back to <b>Analyze</b>, upload your notes, and run an analysis.<br>Your flashcards will appear here automatically.",
    )
    st.stop()

# Session picker
session_labels = [
    f"{s.get('topic', 'General')} — {s.get('timestamp', '')[:10]}  [{s['id']}]"
    for s in history
]

selected_label = st.selectbox(
    "📂 Select session",
    session_labels,
    index=0,
    help="Choose which study session to practise",
)
selected_idx = session_labels.index(selected_label)
session = history[selected_idx]
result = session.get("result", {})

keywords = result.get("keywords", [])
questions = result.get("questions", [])
concepts = result.get("key_concepts", [])

if not keywords and not questions:
    st.warning("This session has no keywords or questions to practice.")
    st.stop()

# ── Mode selector ─────────────────────────────────────────────────────────────
st.divider()
col_l, col_r = st.columns([1, 2])
with col_l:
    mode = st.radio(
        "**Study mode**",
        ["🏷️ Keywords", "❓ Questions", "🔑 Concepts"],
        horizontal=False,
    )

with col_r:
    if "shuffle" not in st.session_state:
        st.session_state.shuffle = False
    st.session_state.shuffle = st.toggle("🔀 Shuffle cards", st.session_state.shuffle)

st.divider()

# ── Card states ───────────────────────────────────────────────────────────────
if "card_idx" not in st.session_state:
    st.session_state.card_idx = 0
if "revealed" not in st.session_state:
    st.session_state.revealed = set()
if "score_known" not in st.session_state:
    st.session_state.score_known = 0
if "score_unsure" not in st.session_state:
    st.session_state.score_unsure = 0
if "fc_order" not in st.session_state:
    st.session_state.fc_order = None


def reset_cards(items):
    st.session_state.card_idx = 0
    st.session_state.revealed = set()
    st.session_state.score_known = 0
    st.session_state.score_unsure = 0
    order = list(range(len(items)))
    if st.session_state.shuffle:
        random.shuffle(order)
    st.session_state.fc_order = order


# ── KEYWORDS MODE ─────────────────────────────────────────────────────────────
if "Keywords" in mode:
    items = keywords
    if not items:
        st.info("No keywords in this session.")
        st.stop()
    if st.session_state.fc_order is None or len(st.session_state.fc_order) != len(items):
        reset_cards(items)

    order = st.session_state.fc_order
    idx = st.session_state.card_idx
    total = len(order)
    progress = idx / total if total else 0

    # Score bar
    k = st.session_state.score_known
    u = st.session_state.score_unsure
    st.markdown(
        f"<div class='score-bar'>"
        f"<span style='color:#6ee7b7;font-weight:700'>✓ {k} known</span>"
        f"<span style='color:#94a3b8'>Card {min(idx+1, total)} / {total}</span>"
        f"<span style='color:#fda4af;font-weight:700'>{u} review</span>"
        f"</div>",
        unsafe_allow_html=True,
    )
    st.progress(progress)

    if idx < total:
        kw = items[order[idx]]
        st.markdown(
            f"<div class='fc-wrap'>"
            f"<div class='fc-icon'>🏷️</div>"
            f"<div class='fc-type'>Keyword</div>"
            f"<div class='fc-text'>{kw}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ I know this", use_container_width=True, type="primary"):
                st.session_state.score_known += 1
                st.session_state.card_idx += 1
                st.rerun()
        with c2:
            if st.button("🔁 Need review", use_container_width=True):
                st.session_state.score_unsure += 1
                st.session_state.card_idx += 1
                st.rerun()
    else:
        st.success(f"🎉 Done! You knew **{k}/{total}** keywords.")
        if st.button("🔄 Restart", use_container_width=True):
            reset_cards(items)
            st.rerun()

# ── QUESTIONS MODE ────────────────────────────────────────────────────────────
elif "Questions" in mode:
    items = questions
    if not items:
        st.info("No questions in this session.")
        st.stop()
    if st.session_state.fc_order is None or len(st.session_state.fc_order) != len(items):
        reset_cards(items)

    order = st.session_state.fc_order
    idx = st.session_state.card_idx
    total = len(order)

    st.progress(idx / total if total else 0)
    st.caption(f"Question {min(idx+1, total)} of {total}")

    if idx < total:
        q = items[order[idx]]
        st.markdown(
            f"<div class='fc-wrap' style='min-height:200px'>"
            f"<div class='fc-icon'>❓</div>"
            f"<div class='fc-type'>Revision Question</div>"
            f"<div class='fc-text'>{q}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

        key = f"rev_{order[idx]}"
        is_revealed = key in st.session_state.revealed

        if not is_revealed:
            if st.button("💭 Write your answer, then reveal", use_container_width=True):
                st.session_state.revealed.add(key)
                st.rerun()
            st.text_area("Your answer (optional — just for practice)", height=100, key=f"ans_{idx}")
        else:
            st.markdown(
                "<div class='q-reveal-box'>✅ Great — check your answer against your notes "
                "or the summary tab to verify your understanding.</div>",
                unsafe_allow_html=True,
            )
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Got it!", use_container_width=True, type="primary"):
                    st.session_state.score_known += 1
                    st.session_state.card_idx += 1
                    st.rerun()
            with c2:
                if st.button("🔁 Need review", use_container_width=True):
                    st.session_state.score_unsure += 1
                    st.session_state.card_idx += 1
                    st.rerun()
    else:
        k = st.session_state.score_known
        st.success(f"🎉 Done! Score: **{k}/{total}**")
        if st.button("🔄 Restart", use_container_width=True):
            reset_cards(items)
            st.rerun()

# ── CONCEPTS MODE ─────────────────────────────────────────────────────────────
else:
    if not concepts:
        st.info("No key concepts in this session.")
        st.stop()
    if st.session_state.fc_order is None or len(st.session_state.fc_order) != len(concepts):
        reset_cards(concepts)

    order = st.session_state.fc_order
    idx = st.session_state.card_idx
    total = len(order)

    st.progress(idx / total if total else 0)

    if idx < total:
        c = concepts[order[idx]]
        key = f"con_{order[idx]}"
        is_revealed = key in st.session_state.revealed

        st.markdown(
            f"<div class='fc-wrap' style='min-height:200px'>"
            f"<div class='fc-icon'>🔑</div>"
            f"<div class='fc-type'>Define this concept</div>"
            f"<div class='fc-text'>{c['concept']}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

        if not is_revealed:
            if st.button("👁️ Reveal definition", use_container_width=True):
                st.session_state.revealed.add(key)
                st.rerun()
        else:
            st.markdown(
                f"<div class='q-reveal-box'>{c['definition']}</div>",
                unsafe_allow_html=True,
            )
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Got it!", use_container_width=True, type="primary"):
                    st.session_state.score_known += 1
                    st.session_state.card_idx += 1
                    st.rerun()
            with c2:
                if st.button("🔁 Need review", use_container_width=True):
                    st.session_state.score_unsure += 1
                    st.session_state.card_idx += 1
                    st.rerun()
    else:
        k = st.session_state.score_known
        st.success(f"🎉 Done! Score: **{k}/{total}**")
        if st.button("🔄 Restart", use_container_width=True):
            reset_cards(concepts)
            st.rerun()
