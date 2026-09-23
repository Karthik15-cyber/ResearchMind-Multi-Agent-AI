
import time
import streamlit as st
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e8e4dc;
}
.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,80,30,0.08) 0%, transparent 55%);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

/* Hero */
.hero { text-align: center; padding: 3.5rem 0 2.5rem; }
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -0.03em;
    color: #f0ebe0;
    margin: 0 0 1rem;
}
.hero h1 span { color: #ff8c32; }
.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #a09890;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.65;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,140,50,0.3), transparent);
    margin: 2rem 0;
}

/* Input area */
.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,140,50,0.15);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(8px);
}
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,140,50,0.25) !important;
    border-radius: 10px !important;
    color: #f0ebe0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #ff8c32 !important;
    box-shadow: 0 0 0 3px rgba(255,140,50,0.12) !important;
}
.stTextInput > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #ff8c32 !important;
    font-weight: 500 !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2.2rem !important;
    cursor: pointer !important;
    box-shadow: 0 4px 20px rgba(255,140,50,0.3) !important;
    width: 100%;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(255,140,50,0.4) !important;
}

/* Example chips */
.chips-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}
.chip-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #605850;
    letter-spacing: 0.1em;
}
.chip {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 6px;
    padding: 0.25rem 0.7rem;
    font-size: 0.75rem;
    color: #a09890;
    font-family: 'DM Sans', sans-serif;
}

/* Pipeline step cards */
.section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #f0ebe0;
    margin: 0 0 1.2rem;
}
.step-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.3rem 1.6rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, background 0.3s;
}
.step-card.active {
    border-color: rgba(255,140,50,0.4);
    background: rgba(255,140,50,0.04);
}
.step-card.done {
    border-color: rgba(80,200,120,0.3);
    background: rgba(80,200,120,0.03);
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 14px 0 0 14px;
    background: rgba(255,255,255,0.05);
    transition: background 0.3s;
}
.step-card.active::before { background: #ff8c32; }
.step-card.done::before   { background: #50c878; }
.step-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    color: #ff8c32;
    opacity: 0.7;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #f0ebe0;
}
.step-status { margin-left: auto; font-family: 'DM Mono', monospace; font-size: 0.68rem; letter-spacing: 0.1em; }
.status-waiting { color: #444; }
.status-running { color: #ff8c32; }
.status-done    { color: #50c878; }
.step-desc { font-size: 0.82rem; color: #706860; margin-top: 0.35rem; }

/* Result panels */
.report-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,140,50,0.2);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
}
.feedback-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(80,200,120,0.2);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
}
.raw-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 0.5rem;
}
.panel-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 0.7rem;
}
.panel-label.orange { color: #ff8c32; border-bottom: 1px solid rgba(255,140,50,0.15); }
.panel-label.green  { color: #50c878; border-bottom: 1px solid rgba(80,200,120,0.15); }
.panel-label.muted  { color: #605850; border-bottom: 1px solid rgba(255,255,255,0.05); }
.raw-content { font-size: 0.85rem; line-height: 1.75; color: #8a8278; white-space: pre-wrap; font-family: 'DM Mono', monospace; }

/* Streamlit expander */
details { background: transparent !important; border: none !important; }
details summary {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #706860 !important;
    letter-spacing: 0.1em !important;
    cursor: pointer;
    padding: 0.5rem 0 !important;
}
.stSpinner > div { color: #ff8c32 !important; }
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid rgba(255,140,50,0.3) !important;
    color: #ff8c32 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.2rem !important;
    margin-top: 1.2rem;
    width: auto !important;
    box-shadow: none !important;
}
.stDownloadButton > button:hover {
    background: rgba(255,140,50,0.08) !important;
    transform: none !important;
}
.notice {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #333;
    text-align: center;
    margin-top: 4rem;
    letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [("results", {}), ("running", False), ("done", False), ("topic_val", "")]:
    if k not in st.session_state:
        st.session_state[k] = v


# ── Step card renderer ────────────────────────────────────────────────────────
def step_card(num, title, state, desc):
    states = {
        "waiting": ("WAITING",   "status-waiting", ""),
        "running": ("● RUNNING", "status-running", "active"),
        "done":    ("✓  DONE",   "status-done",    "done"),
    }
    label, scls, ccls = states.get(state, ("", "", ""))
    st.markdown(f"""
    <div class="step-card {ccls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {scls}">{label}</span>
        </div>
        <div class="step-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


def get_step_state(key):
    """Return waiting / running / done for a pipeline step key."""
    r = st.session_state.results
    order = ["search", "reader", "writer", "critic"]
    if key in r:
        return "done"
    if st.session_state.running:
        # first key not yet in results = currently running
        for k in order:
            if k not in r:
                return "running" if k == key else "waiting"
    return "waiting"


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>Research<span>Mind</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Two-column layout: input | pipeline ───────────────────────────────────────
col_left, col_gap, col_right = st.columns([5, 0.4, 4])

with col_left:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
    )
    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="chips-row">
        <span class="chip-label">TRY →</span>
        <span class="chip">LLM agents 2025</span>
        <span class="chip">CRISPR gene editing</span>
        <span class="chip">Fusion energy progress</span>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)
    step_card("01", "Search Agent",  get_step_state("search"), "Gathers recent web information")
    step_card("02", "Reader Agent",  get_step_state("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain",  get_step_state("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain",  get_step_state("critic"), "Reviews & scores the report")


# ── Trigger run ───────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results  = {}
        st.session_state.running  = True
        st.session_state.done     = False
        st.session_state.topic_val = topic.strip()
        st.rerun()


# ── Execute pipeline (runs after rerun when running=True) ─────────────────────
if st.session_state.running and not st.session_state.done:
    topic_val = st.session_state.topic_val
    results   = {}

    # Step 1 — Search
    with st.spinner("🔍  Search Agent is working…"):
        sa = build_search_agent()
        sr = sa.invoke({"messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]})
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    # Step 2 — Reader
    with st.spinner("📄  Reader Agent is scraping top resources…"):
        ra = build_reader_agent()
        rr = ra.invoke({"messages": [("user",
            f"""
            Based on the following search results about '{topic_val}',
            pick the most relevant URL and scrape it for deeper content.

            Search Results:
            {results['search'][:2500]}

            IMPORTANT:
            - Identify the URL yourself.
            - Use the scrape_url tool.
            - Do not ask the user for a URL.
            """
)]})
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # Step 3 — Writer
    with st.spinner("✍️  Writer is drafting the report…"):
       research_combined = (
    f"SEARCH RESULTS:\n"
    f"{results['search'][:2500]}\n\n"
    f"DETAILED SCRAPED CONTENT:\n"
    f"{results['reader'][:2000]}"
)
    results["writer"] = writer_chain.invoke({"topic": topic_val, "research": research_combined})
    st.session_state.results = dict(results)

    # Step 4 — Critic
    with st.spinner("🧐  Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({"report": results["writer"]})
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done    = True
    st.rerun()


# ── Results ───────────────────────────────────────────────────────────────────
r = st.session_state.results

if r and st.session_state.done:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    # Raw agent outputs (collapsed by default)
    if "search" in r:
        with st.expander("🔍  Search Agent output", expanded=False):
            st.markdown(f'<div class="raw-panel"><div class="panel-label muted">Search Results</div>'
                        f'<div class="raw-content">{r["search"]}</div></div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("📄  Reader Agent output", expanded=False):
            st.markdown(f'<div class="raw-panel"><div class="panel-label muted">Scraped Content</div>'
                        f'<div class="raw-content">{r["reader"]}</div></div>', unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        st.markdown('<div class="report-panel"><div class="panel-label orange">📝 &nbsp;Final Research Report</div>', unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_{st.session_state.topic_val.replace(' ','_')}_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:
        st.markdown('<div class="feedback-panel"><div class="panel-label green">🧐 &nbsp;Critic Feedback</div>', unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)