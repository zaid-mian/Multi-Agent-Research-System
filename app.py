import streamlit as st
import time
from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Research Studio",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Courier+Prime:wght@400;700&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    color: #0f172a;
}

.stApp {
    background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%);
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1rem 2rem 3rem; max-width: 900px; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'Courier Prime', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #a78bfa;
    margin-bottom: 0.8rem;
}
.hero h1 {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(2.5rem, 10vw, 4rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
    color: #ffffff;
    margin: 0 0 1rem;
}
.hero h1 span {
    background: linear-gradient(135deg, #a78bfa 0%, #f472b6 50%, #fb7185 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 1rem;
    font-weight: 400;
    color: #94a3b8;
    max-width: 550px;
    margin: 0 auto;
    line-height: 1.7;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #a78bfa, #fb7185, transparent);
    margin: 2rem 0;
}

/* ── Input card ── */
.input-card {
    background: linear-gradient(135deg, rgba(30,27,75,0.8) 0%, rgba(15,23,42,0.9) 100%);
    border: 2px solid rgba(167,139,250,0.3);
    border-radius: 24px;
    padding: 2rem 2.2rem;
    margin-bottom: 2rem;
    backdrop-filter: blur(25px);
    box-shadow: 0 30px 80px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05);
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input {
    background: rgba(15,23,42,0.6) !important;
    border: 2px solid rgba(167,139,250,0.4) !important;
    border-radius: 14px !important;
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1rem !important;
    padding: 1rem 1.3rem !important;
    transition: all 0.3s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #f472b6 !important;
    box-shadow: 0 0 0 5px rgba(244,114,182,0.15) !important;
}
.stTextInput > label {
    font-family: 'Courier Prime', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #a78bfa !important;
    font-weight: 700 !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #a78bfa 0%, #f472b6 50%, #fb7185 100%) !important;
    color: #0f172a !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 1rem 3.5rem !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 15px 50px rgba(167,139,250,0.4) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-4px) scale(1.02) !important;
    box-shadow: 0 25px 70px rgba(244,114,182,0.5) !important;
}
.stButton > button:active {
    transform: translateY(-1px) !important;
}

/* ── Pipeline step cards with ICONS ── */
.step-card {
    background: rgba(15,23,42,0.6);
    border: 2px solid rgba(148,163,184,0.2);
    border-radius: 20px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    backdrop-filter: blur(20px);
    display: flex;
    align-items: flex-start;
    gap: 1.2rem;
}
.step-card:hover {
    border-color: rgba(167,139,250,0.5);
    background: rgba(30,27,75,0.7);
}
.step-card.active {
    border-color: #f472b6;
    background: linear-gradient(135deg, rgba(167,139,250,0.25), rgba(244,114,182,0.2));
    box-shadow: 0 0 40px rgba(244,114,182,0.3);
}
.step-card.done {
    border-color: #10b981;
    background: rgba(16,185,129,0.15);
}
.step-icon {
    font-size: 2rem;
    min-width: 3.5rem;
    height: 3.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(15,23,42,0.8);
    border-radius: 16px;
    border: 2px solid rgba(148,163,184,0.3);
}
.step-content {
    flex: 1;
}
.step-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.3rem;
}
.step-num {
    font-family: 'Courier Prime', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    color: #a78bfa;
}
.step-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #ffffff;
}
.step-status {
    margin-left: auto;
    font-family: 'Courier Prime', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
}
.status-waiting  { color: #64748b; }
.status-running  { color: #f472b6; }
.status-done     { color: #10b981; }

/* ── Result panels ── */
.result-panel {
    background: rgba(15,23,42,0.7);
    border: 2px solid rgba(148,163,184,0.3);
    border-radius: 18px;
    padding: 1.8rem 2rem;
    margin-top: 1.2rem;
    margin-bottom: 1.8rem;
    backdrop-filter: blur(20px);
}
.result-panel-title {
    font-family: 'Courier Prime', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #a78bfa;
    margin-bottom: 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid rgba(167,139,250,0.25);
}
.result-content {
    font-size: 0.95rem;
    line-height: 1.9;
    color: #cbd5e1;
    white-space: pre-wrap;
    font-family: 'Outfit', sans-serif;
}

/* ── Report & feedback panels ── */
.report-panel {
    background: linear-gradient(135deg, rgba(167,139,250,0.15), rgba(15,23,42,0.8));
    border: 2px solid rgba(167,139,250,0.4);
    border-radius: 22px;
    padding: 2.2rem 2.5rem;
    margin-top: 1.5rem;
    backdrop-filter: blur(25px);
}
.feedback-panel {
    background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(15,23,42,0.8));
    border: 2px solid rgba(16,185,129,0.4);
    border-radius: 22px;
    padding: 2.2rem 2.5rem;
    margin-top: 1.5rem;
    backdrop-filter: blur(25px);
}
.panel-label {
    font-family: 'Courier Prime', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 0.7rem;
}
.panel-label.orange {
    color: #a78bfa;
    border-bottom: 1px solid rgba(167,139,250,0.3);
}
.panel-label.green {
    color: #10b981;
    border-bottom: 1px solid rgba(16,185,129,0.3);
}

/* ── Progress text ── */
.stSpinner > div { color: #f472b6 !important; }

/* ── Expander ── */
details {
    background: rgba(15,23,42,0.5);
    border-radius: 12px;
    padding: 0.4rem 0.9rem;
    border: 1px solid rgba(148,163,184,0.25);
}
details summary {
    font-family: 'Courier Prime', monospace !important;
    font-size: 0.78rem !important;
    color: #94a3b8 !important;
    letter-spacing: 0.1em !important;
    cursor: pointer;
}

/* ── Section heading ── */
.section-heading {
    font-family: 'Outfit', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #ffffff;
    margin: 2rem 0 1.2rem;
}

/* ── Toast-style notice ── */
.notice {
    font-family: 'Courier Prime', monospace;
    font-size: 0.7rem;
    color: #64748b;
    text-align: center;
    margin-top: 2.5rem;
    letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card with ICONS ─────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = "", icon: str = "🔹"):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }

    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")

    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-icon">{icon}</div>
        <div class="step-content">
            <div class="step-header">
                <span class="step-num">{num}</span>
                <span class="step-title">{title}</span>
                <span class="step-status {cls}">{label}</span>
            </div>
            {"<div style='font-size:0.85rem;color:#94a3b8;margin-top:0.3rem;'>"+desc+"</div>" if desc else ""}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">AI Research Studio</div>
    <h1>Smart<span>Research</span></h1>
    <p class="hero-sub">
        Four AI-powered steps — search, scrape, write, critique — to craft
        comprehensive research reports on any subject you choose.
    </p>
</div>

<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Vertical Layout (all centered!) ───────────────────────────────────────────

st.markdown('<div class="input-card">', unsafe_allow_html=True)

topic = st.text_input(
    "What do you want to research?",
    placeholder="e.g. The future of renewable energy in 2030",
    key="topic_input",
    label_visibility="visible",
)

run_btn = st.button(
    "🚀 Start Research",
    use_container_width=True
)

st.markdown('</div>', unsafe_allow_html=True)

# Example chips (simplified!)
examples = [
    "AI in Healthcare 2026",
    "Space Exploration Trends",
    "Quantum Computing Basics"
]

st.markdown("""
<div style="display:flex;gap:0.6rem;flex-wrap:wrap;justify-content:center;margin-bottom:2rem;">
    <span style="font-family:'Courier Prime',monospace;font-size:0.72rem;color:#64748b;letter-spacing:0.08em;">
        Quick Ideas:
    </span>
""", unsafe_allow_html=True)

for ex in examples:
    st.markdown(f"""
    <span style="
        background:rgba(167,139,250,0.15);
        border:1px solid rgba(167,139,250,0.3);
        border-radius:50px;
        padding:0.4rem 1rem;
        font-size:0.8rem;
        color:#e0e7ff;
        font-family:'Outfit',sans-serif;
        cursor:default;
    ">
        {ex}
    </span>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# ── Pipeline Steps (Vertical) ────────────────────────────────────────────────
st.markdown(
    '<div class="section-heading">✨ Research Pipeline</div>',
    unsafe_allow_html=True
)

r = st.session_state.results
done = st.session_state.done

def s(step):
    if not r:
        return "waiting"
    steps = ["search", "reader", "writer", "critic"]
    if step in r:
        return "done"
    if st.session_state.running:
        for k in steps:
            if k not in r:
                return "running" if k == step else "waiting"
    return "waiting"

step_card(
    "01",
    "Search the Web",
    s("search"),
    "Find recent, reliable information",
    icon="🔍"
)

step_card(
    "02",
    "Scrape Deep Content",
    s("reader"),
    "Extract details from top sources",
    icon="📄"
)

step_card(
    "03",
    "Write the Report",
    s("writer"),
    "Draft a structured, clear report",
    icon="✍️"
)

step_card(
    "04",
    "Review & Score",
    s("critic"),
    "Get feedback and improvements",
    icon="🧐"
)


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:

    if not topic.strip():
        st.warning("Please enter a research topic first.")

    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()


if st.session_state.running and not st.session_state.done:

    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("🔍 Searching the web…"):

        search_agent = build_search_agent()

        sr = search_agent.invoke({
            "messages": [
                ("user",
                 f"Find recent, reliable and detailed information about: {topic_val}")
            ]
        })

        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 2: Reader ──
    with st.spinner("📄 Scraping content…"):

        reader_agent = build_reader_agent()

        rr = reader_agent.invoke({
            "messages": [(
                "user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })

        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("✍️ Writing report…"):

        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )

        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })

        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("🧐 Reviewing report…"):

        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })

        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True

    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">📊 Results</div>',
        unsafe_allow_html=True
    )

    # Raw outputs
    if "search" in r:
        with st.expander("🔍 Search Results", expanded=False):

            st.markdown(
                f'''
                <div class="result-panel">
                    <div class="result-panel-title">
                        Search Results
                    </div>
                    <div class="result-content">
                        {r["search"]}
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )

    if "reader" in r:
        with st.expander("📄 Scraped Content", expanded=False):

            st.markdown(
                f'''
                <div class="result-panel">
                    <div class="result-panel-title">
                        Scraped Content
                    </div>
                    <div class="result-content">
                        {r["reader"]}
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )

    # Final report
    if "writer" in r:

        st.markdown("""
        <div class="report-panel">
            <div class="panel-label orange">
                📝 Final Research Report
            </div>
        """, unsafe_allow_html=True)

        st.markdown(r["writer"])

        st.markdown("</div>", unsafe_allow_html=True)

        # Download button
        st.download_button(
            label="⬇ Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:

        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label green">
                🧐 Feedback & Review
            </div>
        """, unsafe_allow_html=True)

        st.markdown(r["critic"])

        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    SmartResearch · AI-Powered Research Studio
</div>
""", unsafe_allow_html=True)
