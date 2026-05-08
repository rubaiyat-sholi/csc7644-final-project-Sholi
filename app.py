import re
import streamlit as st

from detector import detect_ai_text
from explainer import generate_explanation
from rewriter import generate_rewrite

# Page config
st.set_page_config(
    page_title="Explainable AI Detector",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&display=swap');

:root {
    --purple:      #461D7C;
    --purple-dark: #2D1050;
    --purple-deep: #1A0830;
    --gold:        #FDD023;
}

* { font-family: 'Sora', sans-serif !important; }

html, body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stHeader"],
.main,
.block-container,
[data-testid="block-container"] {
    background-color: var(--purple-deep) !important;
    background: var(--purple-deep) !important;
}

.block-container {
    padding: 4rem 4rem 5rem 4rem !important;
    max-width: 900px !important;
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background-color: var(--purple-dark) !important;
    border-right: 1px solid rgba(253,208,35,0.35) !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: var(--gold) !important; }
section[data-testid="stSidebar"] > div {
    background-color: var(--purple-dark) !important;
    padding: 2rem 1.5rem !important;
}
.s-brand { font-size: 20px; font-weight: 800; color: #fff; letter-spacing: -0.3px; line-height: 1.3; margin-bottom: 2px; }
.s-brand em { color: var(--gold); font-style: normal; }
.s-sub { font-size: 12px; font-weight: 300; color: rgba(255,255,255,0.35); }
.s-rule { border: none; border-top: 1px solid rgba(253,208,35,0.18); margin: 22px 0; }
.s-label { font-size: 9px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase; color: var(--gold); display: block; margin-bottom: 10px; }
.s-body { font-size: 13px; font-weight: 300; line-height: 1.8; color: rgba(255,255,255,0.5); }
.s-step { display: flex; gap: 12px; margin-bottom: 14px; align-items: flex-start; }
.s-num { min-width: 24px; height: 24px; border-radius: 50%; border: 1px solid rgba(253,208,35,0.4); color: var(--gold); font-size: 10px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.s-step-text { font-size: 13px; font-weight: 300; line-height: 1.7; color: rgba(255,255,255,0.55); }

/* ── PAGE TITLE ── */
.page-eyebrow { font-size: 10px; font-weight: 600; letter-spacing: 5px; text-transform: uppercase; color: var(--gold); margin-bottom: 14px; }
.page-title { font-size: 54px; font-weight: 800; color: #fff; line-height: 1.05; letter-spacing: -1.5px; margin: 0 0 16px 0; white-space: nowrap; }
.page-title em { color: var(--gold); font-style: normal; }
.page-sub { font-size: 17px; font-weight: 300; color: rgba(255,255,255,0.4); line-height: 1.65; margin-bottom: 44px; }

/* ── INPUT ── */
.stTextArea label { font-size: 11px !important; font-weight: 700 !important; letter-spacing: 4px !important; text-transform: uppercase !important; color: var(--gold) !important; margin-bottom: 10px !important; }
.stTextArea textarea { background: #2D1050 !important; border: 1px solid rgba(253,208,35,0.3) !important; border-radius: 14px !important; font-size: 16px !important; font-weight: 300 !important; color: rgba(255,255,255,0.9) !important; padding: 22px !important; line-height: 1.75 !important; caret-color: var(--gold) !important; }
.stTextArea textarea::placeholder { color: rgba(255,255,255,0.2) !important; }
.stTextArea textarea:focus { border-color: rgba(253,208,35,0.55) !important; background: #3a1a6e !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: var(--gold) !important;
    color: #2D1050 !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 14px 44px !important;
    border: none !important;
    border-radius: 10px !important;
    margin-top: 14px !important;
    white-space: nowrap !important;
    min-width: 180px !important;
    line-height: 1.2 !important;
    transition: all 0.18s !important;
}
.stButton > button:hover { background: #fff !important; color: #461D7C !important; transform: translateY(-2px) !important; }

/* Re-analyze button — outlined style */
.reanalyze-wrap .stButton > button {
    background: transparent !important;
    color: var(--gold) !important;
    border: 1.5px solid rgba(253,208,35,0.5) !important;
    min-width: 140px !important;
    padding: 12px 28px !important;
    font-size: 12px !important;
    margin-top: 0 !important;
}
.reanalyze-wrap .stButton > button:hover {
    background: rgba(253,208,35,0.1) !important;
    color: #fff !important;
    transform: none !important;
}

/* ── HIDE ALERTS / PROGRESS ── */
.stProgress { display: none !important; }
.stAlert    { display: none !important; }

/* ── DIVIDER ── */
.divider { border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(253,208,35,0.3), transparent); margin: 40px 0; }

/* ── SCORE CARD ── */
.score-card { background: var(--gold); border-radius: 20px; padding: 44px 28px; text-align: center; }
.score-eye { font-size: 9px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase; color: rgba(45,16,80,0.55); margin-bottom: 12px; }
.score-num { font-size: 92px; font-weight: 800; color: #2D1050; line-height: 1; letter-spacing: -4px; margin-bottom: 22px; }
.score-tag { font-size: 11px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; padding: 8px 22px; border-radius: 8px; display: inline-block; }
.tag-ai    { background: #2D1050; color: var(--gold); }
.tag-human { background: rgba(45,16,80,0.12); color: #2D1050; }

/* ── VERDICT CARD ── */
.verdict-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); border-top: 2px solid rgba(255,255,255,0.15); border-radius: 16px; padding: 32px 34px; }
.v-eye { font-size: 9px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase; color: var(--gold); margin-bottom: 10px; }
.v-title { font-size: 30px; font-weight: 800; color: #fff; letter-spacing: -0.5px; margin: 6px 0 22px; }
.bar-bg { background: rgba(255,255,255,0.1); border-radius: 50px; height: 6px; margin-bottom: 10px; }
.bar-meta { font-size: 12px; font-weight: 300; color: rgba(255,255,255,0.3); }

/* ── RESULT CARDS ── */
.r-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07); border-top: 2px solid var(--gold); border-radius: 16px; padding: 32px 36px; margin-bottom: 18px; }
.r-eye { font-size: 9px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase; color: var(--gold); margin-bottom: 10px; }
.r-title { font-size: 22px; font-weight: 700; color: #fff; margin: 6px 0 14px; letter-spacing: -0.3px; }
.r-body { font-size: 16px; font-weight: 300; color: rgba(255,255,255,0.62); line-height: 1.85; }

/* ── SENTENCE HIGHLIGHTING ── */
.sent-wrap { line-height: 2.4; font-size: 16px; font-weight: 300; }
.sent-high {
    background: rgba(253,208,35,0.28);
    border-bottom: 2px solid var(--gold);
    border-radius: 4px;
    padding: 2px 4px;
    color: #fff;
    cursor: default;
}
.sent-mid {
    background: rgba(253,208,35,0.09);
    border-bottom: 1px solid rgba(253,208,35,0.3);
    border-radius: 4px;
    padding: 2px 4px;
    color: rgba(255,255,255,0.8);
    cursor: default;
}
.sent-low {
    color: rgba(255,255,255,0.45);
    padding: 2px 4px;
}
.legend {
    display: flex;
    gap: 20px;
    margin-bottom: 18px;
    flex-wrap: wrap;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 11px;
    color: rgba(255,255,255,0.4);
}
.leg-box {
    width: 12px; height: 12px;
    border-radius: 3px;
    display: inline-block;
}

/* ── FEEDBACK LOOP CARDS ── */
.fb-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 28px 32px;
    text-align: center;
}
.fb-score { font-size: 56px; font-weight: 800; line-height: 1; letter-spacing: -3px; margin: 8px 0 10px; }
.fb-label { font-size: 11px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; }
.fb-delta { font-size: 13px; font-weight: 600; margin-top: 8px; }

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stStatusWidget"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ── Sentence scoring helper ───────────────────────────────────────────────────
def score_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if len(s.split()) > 3]
    scored = []
    for s in sentences:
        r = detect_ai_text(s)
        scored.append((s, r["score"]))
    return scored


def render_highlighted(scored_sentences):
    html = '<div class="sent-wrap">'
    for sent, score in scored_sentences:
        if score > 0.60:
            cls = "sent-high"
            title = f"AI score: {score} — likely AI"
        elif score > 0.40:
            cls = "sent-mid"
            title = f"AI score: {score} — uncertain"
        else:
            cls = "sent-low"
            title = f"AI score: {score} — likely human"
        html += f'<span class="{cls}" title="{title}">{sent}</span> '
    html += '</div>'
    return html


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="s-brand">Explainable <em>AI</em></div>
    <div class="s-sub">Text Detection Assistant</div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="s-rule">', unsafe_allow_html=True)
    st.markdown('<span class="s-label">About</span>', unsafe_allow_html=True)
    st.markdown("""
    <div class="s-body">
        This project detects AI-generated text,
        explains the reasoning,
        and suggests human-like rewrites.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="s-rule">', unsafe_allow_html=True)
    st.markdown('<span class="s-label">How it works</span>', unsafe_allow_html=True)
    st.markdown("""
    <div class="s-step"><div class="s-num">1</div><div class="s-step-text">Paste any text into the input field</div></div>
    <div class="s-step"><div class="s-num">2</div><div class="s-step-text">Click <strong style="color:#fff;font-weight:600">Analyze Text</strong> to run the pipeline</div></div>
    <div class="s-step"><div class="s-num">3</div><div class="s-step-text">Review score, sentence highlights, explanation &amp; rewrite</div></div>
    <div class="s-step"><div class="s-num">4</div><div class="s-step-text">Click <strong style="color:#fff;font-weight:600">Re-analyze Rewrite</strong> to see if it improved</div></div>
    """, unsafe_allow_html=True)


# ── Page title ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-eyebrow">Agentic AI System</div>
<div class="page-title">Explainable <em>AI Detector</em></div>
<div class="page-sub">An agentic AI system for transparent AI-text detection and explanation.</div>
""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
user_text = st.text_area(
    "Enter text:",
    height=220,
    placeholder="Paste text here..."
)

# ── Analyze button ────────────────────────────────────────────────────────────
if st.button("🚀 Analyze Text"):

    if user_text.strip() == "":
        st.warning("Please enter some text.")

    else:
        with st.spinner("Analyzing..."):
            result        = detect_ai_text(user_text)
            explanation   = generate_explanation(user_text, result["score"])
            suggestion    = generate_rewrite(user_text, result["score"])
            scored_sents  = score_sentences(user_text)

        # Save to session for feedback loop
        st.session_state["last_result"]     = result
        st.session_state["last_suggestion"] = suggestion
        st.session_state["last_explanation"]= explanation
        st.session_state["last_scored"]     = scored_sents

# ── Results — render from session state so Re-analyze doesn't wipe them ───────
if "last_result" in st.session_state:

    result      = st.session_state["last_result"]
    suggestion  = st.session_state["last_suggestion"]
    explanation = st.session_state["last_explanation"]
    scored_sents= st.session_state["last_scored"]

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Score + verdict row
    col1, col2 = st.columns([1, 1.6], gap="large")

    with col1:
        tag_cls = "tag-ai" if result["label"] == "AI-generated" else "tag-human"
        st.markdown(f"""
        <div class="score-card">
            <div class="score-eye">AI Score</div>
            <div class="score-num">{result["score"]}</div>
            <span class="score-tag {tag_cls}">{result["label"]}</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        pct       = int(result["score"] * 100)
        bar_color = "#FDD023" if result["score"] > 0.35 else "#4ade80"
        st.markdown(f"""
        <div class="verdict-card">
            <div class="v-eye">Label</div>
            <div class="v-title">{result["label"]}</div>
            <div class="bar-bg">
                <div style="width:{pct}%;background:{bar_color};height:6px;border-radius:50px;"></div>
            </div>
            <div class="bar-meta">Confidence {pct}% &nbsp;&middot;&nbsp; Threshold 35%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Feature 1: Sentence-level highlighting ────────────────────────────────
    if scored_sents:
        highlighted_html = render_highlighted(scored_sents)
        st.markdown(f"""
        <div class="r-card">
            <div class="r-eye">Sentence Analysis</div>
            <div class="r-title">Which sentences sound most AI-generated?</div>
            <div class="legend">
                <div class="legend-item">
                    <span class="leg-box" style="background:rgba(253,208,35,0.4);border-bottom:2px solid #FDD023;"></span>
                    High AI likelihood
                </div>
                <div class="legend-item">
                    <span class="leg-box" style="background:rgba(253,208,35,0.1);border-bottom:1px solid rgba(253,208,35,0.4);"></span>
                    Medium
                </div>
                <div class="legend-item">
                    <span class="leg-box" style="background:rgba(255,255,255,0.04);"></span>
                    Likely human
                </div>
            </div>
            {highlighted_html}
        </div>
        """, unsafe_allow_html=True)

    # Explanation
    st.markdown(f"""
    <div class="r-card">
        <div class="r-eye">Explanation</div>
        <div class="r-title">Explanation</div>
        <div class="r-body">{explanation}</div>
    </div>
    """, unsafe_allow_html=True)

    # Rewrite suggestion
    st.markdown(f"""
    <div class="r-card">
        <div class="r-eye">Rewrite Suggestion</div>
        <div class="r-title">Rewrite Suggestion</div>
        <div class="r-body">{suggestion}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Feature 2: Rewrite Feedback Loop ─────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="r-eye" style="margin-bottom:8px;">Rewrite Feedback Loop</div>
    <div class="r-title" style="font-size:20px;color:#fff;margin-bottom:6px;">Did the rewrite help?</div>
    <div class="r-body" style="margin-bottom:20px;">Re-analyze the rewrite to see if it scores lower than the original.</div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="reanalyze-wrap">', unsafe_allow_html=True)
        if st.button("🔁 Re-analyze Rewrite"):
            with st.spinner("Scoring rewrite..."):
                rewrite_result = detect_ai_text(suggestion)
                st.session_state["rewrite_result"] = rewrite_result
        st.markdown('</div>', unsafe_allow_html=True)

    # Show comparison if re-analysis done
    if "rewrite_result" in st.session_state:
        rr    = st.session_state["rewrite_result"]
        delta = round(result["score"] - rr["score"], 2)
        improved = delta > 0

        delta_color = "#4ade80" if improved else "#f87171"
        delta_str   = f"↓ {delta} lower — improved!" if improved else f"↑ {abs(delta)} higher — try again"

        col_a, col_b = st.columns(2, gap="large")

        with col_a:
            st.markdown(f"""
            <div class="fb-card" style="border-top: 2px solid rgba(255,255,255,0.15);">
                <div class="r-eye">Original</div>
                <div class="fb-score" style="color:var(--gold);">{result["score"]}</div>
                <div class="fb-label" style="color:rgba(255,255,255,0.4);">{result["label"]}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_b:
            st.markdown(f"""
            <div class="fb-card" style="border-top: 2px solid {delta_color};">
                <div class="r-eye">Rewrite</div>
                <div class="fb-score" style="color:#fff;">{rr["score"]}</div>
                <div class="fb-label" style="color:rgba(255,255,255,0.4);">{rr["label"]}</div>
                <div class="fb-delta" style="color:{delta_color};">{delta_str}</div>
            </div>
            """, unsafe_allow_html=True)