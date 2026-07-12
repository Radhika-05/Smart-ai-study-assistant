"""
Shared CSS injected on every page.
Call inject_styles() at the top of each Streamlit page.
"""

import streamlit as st

FONTS = "https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&family=Lora:ital,wght@0,400;0,600;1,400&display=swap"

PALETTE = {
    "bg":        "#080b14",
    "surface":   "#0f1420",
    "surface2":  "#161c2d",
    "surface3":  "#1d2540",
    "border":    "#232b42",
    "border2":   "#2e3a55",
    "text":      "#e2e8f0",
    "text2":     "#94a3b8",
    "text3":     "#64748b",
    "indigo":    "#6366f1",
    "indigo2":   "#818cf8",
    "violet":    "#7c3aed",
    "emerald":   "#10b981",
    "amber":     "#f59e0b",
    "rose":      "#f43f5e",
    "cyan":      "#06b6d4",
}

CSS = f"""
<style>
@import url('{FONTS}');

/* ── Reset & base ── */
html, body, [class*="css"] {{
    font-family: 'Sora', sans-serif;
    font-size: 15px;
}}

.stApp {{
    background-color: {PALETTE['bg']};
    color: {PALETTE['text']};
}}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0c1020 0%, #0f1428 100%);
    border-right: 1px solid {PALETTE['border']};
}}
section[data-testid="stSidebar"] .stMarkdown p {{
    color: {PALETTE['text2']};
    font-size: 0.82rem;
    line-height: 1.6;
}}

/* ── Buttons ── */
.stButton > button {{
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    letter-spacing: 0.02em;
    border-radius: 10px;
    transition: all 0.2s ease;
}}
.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    border: none;
    box-shadow: 0 4px 20px rgba(99,102,241,0.35);
}}
.stButton > button[kind="primary"]:hover {{
    transform: translateY(-1px);
    box-shadow: 0 6px 28px rgba(99,102,241,0.5);
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    background: {PALETTE['surface2']};
    border-radius: 12px;
    padding: 4px;
    gap: 2px;
    border: 1px solid {PALETTE['border']};
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.88rem;
    color: {PALETTE['text2']};
    padding: 0.5rem 1.2rem;
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
}}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea, .stSelectbox > div > div {{
    background: {PALETTE['surface2']} !important;
    border: 1px solid {PALETTE['border2']} !important;
    border-radius: 10px !important;
    color: {PALETTE['text']} !important;
    font-family: 'Sora', sans-serif !important;
}}
.stTextInput input:focus, .stTextArea textarea:focus {{
    border-color: {PALETTE['indigo']} !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.18) !important;
}}

/* ── Expanders ── */
.stExpander {{
    background: {PALETTE['surface2']};
    border: 1px solid {PALETTE['border']};
    border-radius: 12px;
}}

/* ── Alerts ── */
.stAlert {{
    border-radius: 10px;
    border: none;
}}

/* ── Dividers ── */
hr {{ border-color: {PALETTE['border']}; }}

/* ── Typography ── */
h1 {{ font-weight: 800; color: {PALETTE['text']} !important; letter-spacing: -0.03em; }}
h2 {{ font-weight: 700; color: {PALETTE['text']} !important; letter-spacing: -0.02em; }}
h3 {{ font-weight: 600; color: {PALETTE['text2']} !important; }}

/* ────────────────────────────────
   CUSTOM COMPONENT CLASSES
──────────────────────────────── */

/* Hero banner */
.hero-banner {{
    background: linear-gradient(135deg, #0f1a3a 0%, #1a0f3a 50%, #0f2a1a 100%);
    border: 1px solid {PALETTE['border2']};
    border-radius: 20px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}}
.hero-banner::before {{
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at 30% 40%, rgba(99,102,241,0.12) 0%, transparent 60%),
                radial-gradient(ellipse at 70% 60%, rgba(124,58,237,0.1) 0%, transparent 60%);
    pointer-events: none;
}}
.hero-title {{
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    background: linear-gradient(135deg, #a5b4fc 0%, #e0e7ff 50%, #c4b5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.5rem 0;
    line-height: 1.1;
}}
.hero-subtitle {{
    color: {PALETTE['text2']};
    font-size: 0.95rem;
    font-weight: 400;
    line-height: 1.6;
    margin: 0;
}}

/* Step progress */
.step-bar {{
    display: flex;
    align-items: center;
    gap: 0;
    margin: 1.5rem 0;
}}
.step-node {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    font-size: 0.78rem;
    font-weight: 700;
    flex-shrink: 0;
}}
.step-node.done {{
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
}}
.step-node.active {{
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    box-shadow: 0 0 16px rgba(99,102,241,0.5);
    animation: pulse-ring 1.8s infinite;
}}
.step-node.pending {{
    background: {PALETTE['surface3']};
    color: {PALETTE['text3']};
    border: 1px solid {PALETTE['border2']};
}}
.step-label {{
    font-size: 0.72rem;
    font-weight: 600;
    margin-top: 0.3rem;
    text-align: center;
    white-space: nowrap;
}}
.step-label.done   {{ color: #10b981; }}
.step-label.active {{ color: {PALETTE['indigo2']}; }}
.step-label.pending{{ color: {PALETTE['text3']}; }}
.step-connector {{
    flex: 1;
    height: 2px;
    margin: 0 4px;
}}
.step-connector.done   {{ background: linear-gradient(90deg, #10b981, #10b981); }}
.step-connector.pending{{ background: {PALETTE['border2']}; }}

@keyframes pulse-ring {{
    0%   {{ box-shadow: 0 0 0 0 rgba(99,102,241,0.5); }}
    70%  {{ box-shadow: 0 0 0 8px rgba(99,102,241,0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(99,102,241,0); }}
}}

/* Result cards */
.result-card {{
    background: {PALETTE['surface2']};
    border: 1px solid {PALETTE['border']};
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}}
.result-card:hover {{ border-color: {PALETTE['border2']}; }}

/* Summary */
.summary-text {{
    font-family: 'Lora', Georgia, serif;
    font-size: 1.02rem;
    line-height: 1.8;
    color: {PALETTE['text']};
    background: {PALETTE['surface2']};
    border: 1px solid {PALETTE['border']};
    border-left: 4px solid {PALETTE['indigo']};
    border-radius: 0 12px 12px 0;
    padding: 1.4rem 1.6rem;
}}

/* Keywords */
.kw-wrap {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    padding: 0.5rem 0;
}}
.kw-chip {{
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.4rem 1rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.01em;
    cursor: default;
    transition: transform 0.15s, box-shadow 0.15s;
    animation: chip-in 0.4s ease both;
}}
.kw-chip:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}}
.kw-chip.color-0 {{ background: rgba(99,102,241,0.18); color: #a5b4fc; border: 1px solid rgba(99,102,241,0.35); }}
.kw-chip.color-1 {{ background: rgba(124,58,237,0.18); color: #c4b5fd; border: 1px solid rgba(124,58,237,0.35); }}
.kw-chip.color-2 {{ background: rgba(6,182,212,0.18);  color: #67e8f9; border: 1px solid rgba(6,182,212,0.35); }}
.kw-chip.color-3 {{ background: rgba(16,185,129,0.18); color: #6ee7b7; border: 1px solid rgba(16,185,129,0.35); }}
.kw-chip.color-4 {{ background: rgba(245,158,11,0.18); color: #fcd34d; border: 1px solid rgba(245,158,11,0.35); }}
.kw-chip.color-5 {{ background: rgba(244,63,94,0.18);  color: #fda4af; border: 1px solid rgba(244,63,94,0.35); }}

@keyframes chip-in {{
    from {{ opacity: 0; transform: scale(0.85) translateY(4px); }}
    to   {{ opacity: 1; transform: scale(1) translateY(0); }}
}}

/* Questions */
.q-item {{
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    background: {PALETTE['surface2']};
    border: 1px solid {PALETTE['border']};
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.6rem;
    transition: border-color 0.2s, background 0.2s;
    animation: q-slide 0.35s ease both;
}}
.q-item:hover {{
    background: {PALETTE['surface3']};
    border-color: rgba(99,102,241,0.45);
}}
.q-num {{
    min-width: 28px;
    height: 28px;
    border-radius: 8px;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    font-size: 0.75rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
}}
.q-text {{
    font-size: 0.93rem;
    line-height: 1.55;
    color: {PALETTE['text']};
    padding-top: 2px;
}}

@keyframes q-slide {{
    from {{ opacity: 0; transform: translateX(-8px); }}
    to   {{ opacity: 1; transform: translateX(0); }}
}}

/* OCR raw text */
.ocr-box {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    line-height: 1.65;
    color: #94a3b8;
    background: #050810;
    border: 1px solid {PALETTE['border']};
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 280px;
    overflow-y: auto;
}}

/* Stat pills */
.stat-row {{
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin: 0.8rem 0;
}}
.stat-pill {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: {PALETTE['surface3']};
    border: 1px solid {PALETTE['border2']};
    border-radius: 999px;
    padding: 0.3rem 0.9rem;
    font-size: 0.78rem;
    font-weight: 600;
    color: {PALETTE['text2']};
}}

/* Topic badge */
.topic-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(6,182,212,0.12);
    border: 1px solid rgba(6,182,212,0.35);
    color: #67e8f9;
    border-radius: 999px;
    padding: 0.35rem 1rem;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.03em;
}}

/* Difficulty badge */
.diff-easy   {{ background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.4); color: #6ee7b7; border-radius: 999px; padding: 0.3rem 0.9rem; font-size: 0.78rem; font-weight: 700; display: inline-block; }}
.diff-medium {{ background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.4); color: #fcd34d; border-radius: 999px; padding: 0.3rem 0.9rem; font-size: 0.78rem; font-weight: 700; display: inline-block; }}
.diff-hard   {{ background: rgba(244,63,94,0.15);  border: 1px solid rgba(244,63,94,0.4);  color: #fda4af; border-radius: 999px; padding: 0.3rem 0.9rem; font-size: 0.78rem; font-weight: 700; display: inline-block; }}

/* Flashcard */
.flashcard-outer {{
    perspective: 1200px;
    width: 100%;
    height: 280px;
    cursor: pointer;
}}
.flashcard {{
    width: 100%;
    height: 100%;
    position: relative;
    transform-style: preserve-3d;
    transition: transform 0.55s cubic-bezier(0.23,1,0.32,1);
    border-radius: 18px;
}}
.flashcard.flipped {{ transform: rotateY(180deg); }}
.card-face {{
    position: absolute;
    inset: 0;
    border-radius: 18px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    text-align: center;
}}
.card-front {{
    background: linear-gradient(135deg, #1a1f40 0%, #1f1040 100%);
    border: 1px solid rgba(99,102,241,0.4);
}}
.card-back {{
    background: linear-gradient(135deg, #0f2a1a 0%, #1a1030 100%);
    border: 1px solid rgba(16,185,129,0.4);
    transform: rotateY(180deg);
}}
.card-hint {{
    font-size: 0.72rem;
    color: {PALETTE['text3']};
    margin-bottom: 0.8rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}}
.card-content {{
    font-size: 1.15rem;
    font-weight: 600;
    color: {PALETTE['text']};
    line-height: 1.5;
}}
.card-icon {{
    font-size: 2rem;
    margin-bottom: 0.5rem;
}}

/* History card */
.hist-card {{
    background: {PALETTE['surface2']};
    border: 1px solid {PALETTE['border']};
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
    cursor: pointer;
    transition: all 0.2s;
}}
.hist-card:hover {{
    border-color: rgba(99,102,241,0.5);
    background: {PALETTE['surface3']};
    transform: translateX(2px);
}}
.hist-meta {{
    font-size: 0.75rem;
    color: {PALETTE['text3']};
    margin-bottom: 0.4rem;
}}
.hist-title {{
    font-size: 0.95rem;
    font-weight: 600;
    color: {PALETTE['text']};
    margin-bottom: 0.3rem;
}}
.hist-preview {{
    font-size: 0.8rem;
    color: {PALETTE['text2']};
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}}

/* Empty state */
.empty-state {{
    text-align: center;
    padding: 4rem 2rem;
    color: {PALETTE['text3']};
}}
.empty-state .icon {{ font-size: 3rem; margin-bottom: 1rem; }}
.empty-state h3 {{ color: {PALETTE['text2']}; font-size: 1.1rem; margin-bottom: 0.5rem; }}
.empty-state p {{ font-size: 0.88rem; line-height: 1.6; }}

/* Image cards */
.img-card {{
    background: {PALETTE['surface2']};
    border: 1px solid {PALETTE['border']};
    border-radius: 12px;
    padding: 0.8rem;
    text-align: center;
}}
.img-card-label {{
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: {PALETTE['text3']};
    margin-bottom: 0.6rem;
}}

/* Mnemonic box */
.mnemonic-box {{
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.3);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    font-size: 0.9rem;
    color: #fde68a;
    line-height: 1.55;
}}
.mnemonic-box .label {{
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #f59e0b;
    margin-bottom: 0.3rem;
}}

/* Sidebar nav active */
.sidebar-nav-item {{
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.55rem 0.8rem;
    border-radius: 8px;
    font-size: 0.88rem;
    font-weight: 500;
    color: {PALETTE['text2']};
    cursor: pointer;
    transition: all 0.15s;
    text-decoration: none;
    margin-bottom: 2px;
}}
.sidebar-nav-item:hover {{
    background: {PALETTE['surface3']};
    color: {PALETTE['text']};
}}
.sidebar-nav-item.active {{
    background: rgba(99,102,241,0.18);
    color: {PALETTE['indigo2']};
    font-weight: 600;
}}
</style>
"""


def inject_styles() -> None:
    """Inject shared CSS into the current Streamlit page."""
    st.markdown(CSS, unsafe_allow_html=True)


def hero(title: str, subtitle: str, emoji: str = "📚") -> None:
    st.markdown(
        f"""
        <div class="hero-banner">
            <div style="font-size:2.8rem; margin-bottom:0.6rem;">{emoji}</div>
            <div class="hero-title">{title}</div>
            <p class="hero-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def step_progress(steps: list[str], current: int) -> None:
    """
    Render a horizontal step progress bar.
    steps: list of step labels
    current: 0-indexed current step (steps before are 'done')
    """
    html = "<div class='step-bar'>"
    for i, label in enumerate(steps):
        if i < current:
            state = "done"
            icon = "✓"
        elif i == current:
            state = "active"
            icon = str(i + 1)
        else:
            state = "pending"
            icon = str(i + 1)

        html += f"""
        <div style="display:flex;flex-direction:column;align-items:center;gap:4px">
            <div class="step-node {state}">{icon}</div>
            <div class="step-label {state}">{label}</div>
        </div>
        """
        if i < len(steps) - 1:
            conn_state = "done" if i < current else "pending"
            html += f"<div class='step-connector {conn_state}' style='margin-bottom:20px'></div>"

    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def stat_row(stats: list[tuple[str, str]]) -> None:
    """Render a row of stat pills. Each tuple is (icon+label, value)."""
    pills = "".join(
        f"<span class='stat-pill'>{icon} <b>{value}</b></span>"
        for icon, value in stats
    )
    st.markdown(f"<div class='stat-row'>{pills}</div>", unsafe_allow_html=True)


def keyword_chips(keywords: list[str]) -> None:
    chips = "".join(
        f"<span class='kw-chip color-{i % 6}'>{kw}</span>"
        for i, kw in enumerate(keywords)
    )
    st.markdown(f"<div class='kw-wrap'>{chips}</div>", unsafe_allow_html=True)


def question_list(questions: list[str]) -> None:
    items = "".join(
        f"""<div class='q-item' style='animation-delay:{i*0.06}s'>
                <div class='q-num'>{i+1}</div>
                <div class='q-text'>{q}</div>
            </div>"""
        for i, q in enumerate(questions)
    )
    st.markdown(items, unsafe_allow_html=True)


def summary_block(text: str) -> None:
    st.markdown(f"<div class='summary-text'>{text}</div>", unsafe_allow_html=True)


def ocr_block(text: str) -> None:
    import html as _html
    safe = _html.escape(text)
    st.markdown(f"<div class='ocr-box'>{safe}</div>", unsafe_allow_html=True)


def topic_badge(topic: str) -> str:
    return f"<span class='topic-badge'>🎯 {topic}</span>"


def difficulty_badge(level: str) -> str:
    cls = f"diff-{level.lower()}"
    icons = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
    icon = icons.get(level.lower(), "⚪")
    return f"<span class='{cls}'>{icon} {level.capitalize()}</span>"


def empty_state(icon: str, title: str, body: str) -> None:
    st.markdown(
        f"""<div class='empty-state'>
            <div class='icon'>{icon}</div>
            <h3>{title}</h3>
            <p>{body}</p>
        </div>""",
        unsafe_allow_html=True,
    )
