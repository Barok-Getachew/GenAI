import streamlit as st
import os
import re
from dotenv import load_dotenv
from pathlib import Path

# ── load env ──────────────────────────────────────────────────────────────────
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

# ── page config (MUST be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="HealthAI Analyser",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── premium dark CSS ──────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary:    #0a0f1e;
    --bg-card:       #111827;
    --bg-card2:      #1a2235;
    --accent-blue:   #3b82f6;
    --accent-green:  #10b981;
    --accent-red:    #ef4444;
    --accent-amber:  #f59e0b;
    --text-primary:  #f0f6ff;
    --text-muted:    #94a3b8;
    --border:        rgba(59,130,246,0.18);
    --glow-blue:     0 0 24px rgba(59,130,246,0.25);
    --radius-lg:     16px;
    --radius-md:     10px;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background: var(--bg-primary) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
}

/* Hero */
.hero-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 40%, #0c1a3a 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--glow-blue);
}
.hero-header::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 70% 60% at 80% 40%, rgba(59,130,246,0.12) 0%, transparent 70%),
                radial-gradient(ellipse 40% 40% at 10% 80%, rgba(139,92,246,0.1) 0%, transparent 60%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #60a5fa, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.4rem 0;
    line-height: 1.15;
}
.hero-subtitle {
    color: var(--text-muted);
    font-size: 1.05rem;
    margin: 0;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(59,130,246,0.12);
    border: 1px solid rgba(59,130,246,0.3);
    border-radius: 999px;
    padding: 0.25rem 0.85rem;
    font-size: 0.78rem;
    font-weight: 500;
    color: #93c5fd;
    margin-bottom: 1rem;
}

/* Cards */
.glass-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
    transition: border-color 0.3s, box-shadow 0.3s;
}
.glass-card:hover {
    border-color: rgba(59,130,246,0.4);
    box-shadow: var(--glow-blue);
}
.section-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0 0 1rem 0;
}

/* Metrics */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 0.9rem;
    margin-top: 0.5rem;
}
.metric-card {
    background: var(--bg-card2);
    border-radius: var(--radius-md);
    padding: 1rem 1.1rem;
    border: 1px solid var(--border);
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover { transform: translateY(-2px); }
.metric-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 3px 0 0 3px;
}
.metric-card.normal::before { background: var(--accent-green); box-shadow: 0 0 8px var(--accent-green); }
.metric-card.high::before   { background: var(--accent-red);   box-shadow: 0 0 8px var(--accent-red); }
.metric-card.low::before    { background: var(--accent-amber); box-shadow: 0 0 8px var(--accent-amber); }
.metric-card.normal:hover { box-shadow: 0 4px 20px rgba(16,185,129,0.2); }
.metric-card.high:hover   { box-shadow: 0 4px 20px rgba(239,68,68,0.2); }
.metric-card.low:hover    { box-shadow: 0 4px 20px rgba(245,158,11,0.2); }

.metric-name  { font-size: 0.78rem; color: var(--text-muted); font-weight: 500; margin-bottom: 0.3rem; }
.metric-value { font-size: 1.35rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; color: var(--text-primary); }
.metric-ref   { font-size: 0.7rem; color: var(--text-muted); margin-top: 0.2rem; }
.status-badge {
    display: inline-block;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    padding: 0.15rem 0.55rem;
    border-radius: 999px;
    margin-top: 0.45rem;
    text-transform: uppercase;
}
.badge-normal { background: rgba(16,185,129,0.15); color: #6ee7b7; border: 1px solid rgba(16,185,129,0.3); }
.badge-high   { background: rgba(239,68,68,0.15);  color: #fca5a5; border: 1px solid rgba(239,68,68,0.3); }
.badge-low    { background: rgba(245,158,11,0.15); color: #fcd34d; border: 1px solid rgba(245,158,11,0.3); }

/* Stats bar */
.stats-bar {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 1.4rem;
}
.stat-pill {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 0.4rem 1rem;
    font-size: 0.85rem;
    font-weight: 500;
}
.stat-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0b1120 !important;
    border-right: 1px solid var(--border) !important;
}

/* Step indicators */
.step-indicator {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}
.step-num {
    width: 22px; height: 22px;
    border-radius: 50%;
    background: linear-gradient(135deg, #3b82f6, #6366f1);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.7rem; font-weight: 700; color: white; flex-shrink: 0;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(59,130,246,0.3); border-radius: 3px; }

/* Footer */
.footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.78rem;
    padding: 1.5rem 0 0.5rem;
    border-top: 1px solid var(--border);
    margin-top: 2rem;
}
</style>
""",
    unsafe_allow_html=True,
)


# ── LLM ───────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_llm():
    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )


# ── helpers ───────────────────────────────────────────────────────────────────
def parse_metrics(text: str) -> list:
    pattern = re.compile(
        r"-\s*(?P<name>[^:]+?):\s*(?P<value>[^|]+?)\s*\|"
        r"\s*Status:\s*(?P<status>High|Low|Normal)\s*\|"
        r"\s*Reference:\s*(?P<ref>[^\n]+)",
        re.IGNORECASE,
    )
    return [
        {
            "name":   m.group("name").strip(),
            "value":  m.group("value").strip(),
            "status": m.group("status").strip().capitalize(),
            "ref":    m.group("ref").strip(),
        }
        for m in pattern.finditer(text)
    ]


def render_metrics(metrics: list):
    counts = {"Normal": 0, "High": 0, "Low": 0}
    for m in metrics:
        counts[m["status"]] = counts.get(m["status"], 0) + 1

    st.markdown(
        f"""
        <div class="stats-bar">
            <div class="stat-pill">
                <span class="stat-dot" style="background:#10b981;box-shadow:0 0 6px #10b981"></span>
                <span>{counts['Normal']} Normal</span>
            </div>
            <div class="stat-pill">
                <span class="stat-dot" style="background:#ef4444;box-shadow:0 0 6px #ef4444"></span>
                <span>{counts['High']} High</span>
            </div>
            <div class="stat-pill">
                <span class="stat-dot" style="background:#f59e0b;box-shadow:0 0 6px #f59e0b"></span>
                <span>{counts['Low']} Low</span>
            </div>
            <div class="stat-pill">
                <span style="color:#94a3b8">📋 {len(metrics)} markers total</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cards_html = '<div class="metric-grid">'
    for m in metrics:
        css = {"Normal": "normal", "High": "high", "Low": "low"}.get(m["status"], "normal")
        cards_html += (
            f'<div class="metric-card {css}">'
            f'<div class="metric-name">{m["name"]}</div>'
            f'<div class="metric-value">{m["value"]}</div>'
            f'<div class="metric-ref">Ref: {m["ref"]}</div>'
            f'<span class="status-badge badge-{css}">{m["status"]}</span>'
            f"</div>"
        )
    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)


# ── sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="padding:1rem 0 1.5rem">
            <div style="font-size:1.5rem;font-weight:800;
                        background:linear-gradient(135deg,#60a5fa,#a78bfa);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                        margin-bottom:0.2rem">🩺 HealthAI</div>
            <div style="font-size:0.78rem;color:#64748b;">Powered by Gemini AI</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**How it works**")
    for num, text in [
        ("1", "Upload or paste your blood report"),
        ("2", "AI extracts & classifies all markers"),
        ("3", "View visual health dashboard"),
        ("4", "Get personalised diet recommendations"),
    ]:
        st.markdown(
            f'<div class="step-indicator">'
            f'<div class="step-num">{num}</div><span>{text}</span></div>',
            unsafe_allow_html=True,
        )

    st.divider()
    st.markdown("**Settings**")
    diet_style = st.selectbox(
        "Diet style",
        ["Ethiopian", "Mediterranean", "General / International"],
        help="Personalises the dietary recommendations.",
    )
    show_raw = st.toggle("Show raw AI output", value=False)

    st.divider()
    st.markdown(
        "<div style='font-size:0.75rem;color:#475569;line-height:1.6'>"
        "⚠️ <strong>Disclaimer:</strong> This tool is for educational purposes only. "
        "Always consult a qualified healthcare professional for medical advice."
        "</div>",
        unsafe_allow_html=True,
    )


# ── hero ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-header">
        <div class="hero-badge">✦ AI-Powered Health Intelligence</div>
        <h1 class="hero-title">Blood Work Analyser</h1>
        <p class="hero-subtitle">
            Upload your lab report and get an instant AI-generated health summary,
            visual biomarker dashboard, and personalised dietary recommendations.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ── input section ─────────────────────────────────────────────────────────────
col_left, col_right = st.columns([3, 2], gap="large")

with col_left:
    st.markdown(
        '<div class="glass-card"><p class="section-title">📁 Blood Report Input</p>',
        unsafe_allow_html=True,
    )
    input_mode = st.radio(
        "Input method",
        ["📂 Upload a .txt file", "✏️ Paste report text"],
        horizontal=True,
        label_visibility="collapsed",
    )

    blood_report = ""

    if input_mode == "📂 Upload a .txt file":
        uploaded = st.file_uploader(
            "Drop your blood report (.txt)",
            type=["txt"],
            label_visibility="collapsed",
        )
        if uploaded:
            blood_report = uploaded.read().decode("utf-8")
            st.success(f"✓ Loaded **{uploaded.name}** ({len(blood_report)} chars)")
    else:
        blood_report = st.text_area(
            "Paste report",
            height=260,
            placeholder="Patient: John Doe, Age 45, Male\nDate: ...\n\nCOMPLETE BLOOD COUNT\n...",
            label_visibility="collapsed",
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Load sample
    sample_path = Path(__file__).resolve().parent.parent / "blood_work.txt"
    if sample_path.exists():
        if st.button("🧪 Load Sample Report", key="load_sample"):
            st.session_state["sample_report"] = sample_path.read_text()

if "sample_report" in st.session_state and not blood_report.strip():
    blood_report = st.session_state["sample_report"]

with col_right:
    st.markdown(
        '<div class="glass-card"><p class="section-title">👤 Patient Preview</p>',
        unsafe_allow_html=True,
    )
    if blood_report.strip():
        lines = [l for l in blood_report.strip().splitlines() if l.strip()]
        patient_line = next((l for l in lines if "patient" in l.lower()), lines[0])
        date_line = next((l for l in lines if "date" in l.lower()), "")
        doc_line = next(
            (l for l in lines if any(k in l.lower() for k in ["physician", "doctor", "dr."])),
            "",
        )
        doc_html = (
            f'<div style="font-size:0.78rem;color:#64748b;margin-top:0.3rem">🩺 {doc_line}</div>'
            if doc_line
            else ""
        )
        entry_count = len([l for l in lines if any(k in l for k in [":", "–", "-"])])
        st.markdown(
            f"""
            <div style="display:flex;flex-direction:column;gap:0.7rem">
                <div style="display:flex;align-items:center;gap:0.8rem">
                    <div style="width:48px;height:48px;border-radius:50%;
                                background:linear-gradient(135deg,#3b82f6,#8b5cf6);
                                display:flex;align-items:center;justify-content:center;
                                font-size:1.4rem;flex-shrink:0">👤</div>
                    <div>
                        <div style="font-size:0.95rem;font-weight:600">{patient_line}</div>
                        <div style="font-size:0.75rem;color:#64748b">{date_line}</div>
                    </div>
                </div>
                {doc_html}
                <div style="font-size:0.78rem;color:#94a3b8;background:rgba(59,130,246,0.06);
                            border:1px solid rgba(59,130,246,0.12);border-radius:8px;
                            padding:0.6rem 0.8rem;margin-top:0.2rem">
                    {entry_count} data entries detected
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """<div style="text-align:center;color:#475569;padding:2rem 0">
                <div style="font-size:2.5rem;margin-bottom:0.5rem">📋</div>
                <div style="font-size:0.85rem">Upload or paste a report to see patient info</div>
            </div>""",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


# ── analyse button ────────────────────────────────────────────────────────────
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
col_btn, _ = st.columns([1, 3])
with col_btn:
    analyse_clicked = st.button(
        "🔬 Analyse Report", type="primary", use_container_width=True
    )


# ── pipeline ──────────────────────────────────────────────────────────────────
if analyse_clicked:
    if not blood_report.strip():
        st.error("⚠️ Please upload or paste a blood report before analysing.")
    else:
        try:
            llm = get_llm()
        except Exception as e:
            st.error(f"❌ Could not connect to Gemini API: {e}")
            st.stop()

        # ── Stage 1: Extraction ──────────────────────────────────────────────
        st.markdown("---")
        st.markdown(
            '<p class="section-title">🔬 Stage 1 — Biomarker Extraction</p>',
            unsafe_allow_html=True,
        )

        extraction_prompt = (
            "You are a medical data extraction assistant.\n\n"
            "From the blood report below, extract all test values and classify each one as "
            "High, Low or Normal based on the reference ranges provided in the report.\n\n"
            "Format your response EXACTLY as (one per line):\n"
            "- Test Name: value | Status: High/Low/Normal | Reference: range\n\n"
            f"Blood Report:\n{blood_report}"
        )

        with st.spinner("🧬 Extracting and classifying biomarkers…"):
            try:
                ext_resp = llm.invoke(extraction_prompt)
                extracted_values = ext_resp.text
            except Exception as e:
                st.error(f"❌ Extraction failed: {e}")
                st.stop()

        if show_raw:
            with st.expander("Raw extraction output"):
                st.code(extracted_values, language="text")

        metrics = parse_metrics(extracted_values)
        if metrics:
            render_metrics(metrics)
        else:
            st.warning("Could not parse structured metrics — showing raw output:")
            st.code(extracted_values, language="text")

        # ── Stage 2: Health Summary + Diet ──────────────────────────────────
        st.markdown("---")
        st.markdown(
            '<p class="section-title">🥗 Stage 2 — Health Summary & Diet Plan</p>',
            unsafe_allow_html=True,
        )

        diet_prompt = (
            f"You are a clinical nutritionist specializing in {diet_style} dietary habits.\n\n"
            "Based on the blood work analysis below, write:\n"
            "1. A health summary in 4-5 sentences explaining the patient's condition in simple, empathetic language.\n"
            "2. A practical diet plan with exactly TWO sections:\n"
            "   ### 🚫 Foods to Avoid\n"
            "   (bullet points)\n"
            "   ### ✅ Foods to Eat More Of\n"
            "   (bullet points)\n\n"
            "Do NOT include any other sections.\n\n"
            f"Blood work Analysis:\n{extracted_values}"
        )

        with st.spinner("🥗 Generating health summary and diet recommendations…"):
            try:
                diet_resp = llm.invoke(diet_prompt)
                diet_text = diet_resp.text
            except Exception as e:
                st.error(f"❌ Diet plan generation failed: {e}")
                st.stop()

        if show_raw:
            with st.expander("Raw diet plan output"):
                st.code(diet_text, language="text")

        # Parse sections
        avoid_m   = re.search(r"(###?\s*🚫.*?(?=###|$))", diet_text, re.DOTALL | re.IGNORECASE)
        include_m = re.search(r"(###?\s*✅.*?(?=###|$))", diet_text, re.DOTALL | re.IGNORECASE)
        first = min(
            avoid_m.start()   if avoid_m   else len(diet_text),
            include_m.start() if include_m else len(diet_text),
        )
        summary_text = diet_text[:first].strip()
        avoid_text   = avoid_m.group(1).strip()   if avoid_m   else ""
        include_text = include_m.group(1).strip() if include_m else ""

        col_a, col_b = st.columns(2, gap="large")

        with col_a:
            st.markdown(
                '<div class="glass-card"><p class="section-title">📝 Health Summary</p>',
                unsafe_allow_html=True,
            )
            st.markdown(summary_text if summary_text else diet_text)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_b:
            st.markdown(
                '<div class="glass-card"><p class="section-title">🥗 Diet Recommendations</p>',
                unsafe_allow_html=True,
            )
            if avoid_text or include_text:
                st.markdown(avoid_text)
                st.markdown(include_text)
            else:
                st.markdown(diet_text)
            st.markdown("</div>", unsafe_allow_html=True)

        # Success banner
        st.markdown(
            """
            <div style="background:linear-gradient(135deg,rgba(16,185,129,0.12),rgba(6,182,212,0.08));
                        border:1px solid rgba(16,185,129,0.25);border-radius:12px;
                        padding:1rem 1.4rem;display:flex;align-items:center;gap:0.8rem;margin-top:0.5rem">
                <span style="font-size:1.4rem">✅</span>
                <div>
                    <div style="font-weight:600;color:#6ee7b7">Analysis Complete</div>
                    <div style="font-size:0.8rem;color:#64748b">
                        Remember: always discuss these results with your doctor before making health decisions.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── footer ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer">HealthAI Analyser · Built with Streamlit & Gemini AI · For educational use only</div>',
    unsafe_allow_html=True,
)
