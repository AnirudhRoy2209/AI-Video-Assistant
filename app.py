"""
AI Video Assistant — Streamlit UI
Wraps the existing CLI pipeline (pipeline.py) in a minimal, modern web UI.
Run with: streamlit run app.py
"""

import os

import streamlit as st

# ---- import your existing pipeline -----------------------------------
# Adjust this import if your CLI file has a different name (e.g. main.py)
from main import pipeline  # noqa: E402
from core.rag_engine import ask_questions  # noqa: E402


# ======================================================================
# PAGE CONFIG
# ======================================================================
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎞️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ======================================================================
# FORMAL / EDITORIAL CSS — Slate Navy + Muted Gold
# ======================================================================
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

        :root {
            --navy: #0e1a2b;
            --navy-deep: #081120;
            --slate: #334155;
            --gold: #b68d40;
            --gold-light: #e8d4a2;
            --ink: #1a2433;
            --muted: #5b6b7d;
            --paper: #fbfaf7;
            --card: #ffffff;
            --border: #e3e1d9;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .stApp {
            background: var(--paper);
            color: var(--ink);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1140px;
        }

        #MainMenu, footer, header {visibility: hidden;}

        h1, h2, h3, h4 {
            font-family: 'Source Serif 4', Georgia, serif !important;
            color: var(--navy) !important;
            letter-spacing: -0.01em;
        }

        /* ---- masthead ---- */
        .masthead {
            border-bottom: 2px solid var(--navy);
            padding-bottom: 1.1rem;
            margin-bottom: 1.8rem;
        }
        .masthead-eyebrow {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.72rem;
            font-weight: 500;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: var(--gold);
            margin-bottom: 0.4rem;
        }
        .app-title {
            font-size: 2.1rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
            line-height: 1.1;
        }
        .app-subtitle {
            color: var(--muted);
            font-size: 0.98rem;
            font-family: 'Inter', sans-serif;
        }

        /* ---- cards ---- */
        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-top: 3px solid var(--navy);
            border-radius: 6px;
            padding: 1.5rem 1.6rem;
            margin-bottom: 1rem;
        }
        .card h4 {
            margin-top: 0;
            margin-bottom: 0.7rem;
            font-size: 0.78rem;
            font-weight: 600;
            font-family: 'IBM Plex Mono', monospace !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--slate) !important;
        }

        /* ---- pills / status ---- */
        .pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.3rem 0.8rem;
            border-radius: 4px;
            font-size: 0.74rem;
            font-weight: 600;
            font-family: 'IBM Plex Mono', monospace;
            letter-spacing: 0.03em;
            background: var(--navy);
            color: var(--gold-light);
            margin-bottom: 1rem;
        }
        .pill::before {
            content: "";
            width: 6px; height: 6px;
            background: var(--gold);
            border-radius: 50%;
        }

        /* ---- buttons ---- */
        .stButton>button {
            border-radius: 5px;
            font-weight: 600;
            padding: 0.6rem 1.3rem;
            border: 1px solid var(--navy);
            background: var(--navy);
            color: #ffffff;
            letter-spacing: 0.01em;
        }
        .stButton>button:hover {
            background: var(--navy-deep);
            border-color: var(--navy-deep);
        }

        /* ---- tabs ---- */
        button[data-baseweb="tab"] {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.82rem;
            font-weight: 500;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: var(--navy) !important;
        }
        div[data-baseweb="tab-highlight"] {
            background-color: var(--gold) !important;
        }

        /* ---- chat bubbles ---- */
        .chat-user {
            background: #eef1f5;
            border-left: 3px solid var(--slate);
            border-radius: 4px;
            padding: 0.65rem 0.95rem;
            margin-bottom: 0.45rem;
            font-size: 0.93rem;
        }
        .chat-assistant {
            background: #fbf6ea;
            border-left: 3px solid var(--gold);
            border-radius: 4px;
            padding: 0.65rem 0.95rem;
            margin-bottom: 0.95rem;
            font-size: 0.93rem;
        }

        /* ---- inputs ---- */
        .stTextInput input, .stTextArea textarea, div[data-testid="stSelectbox"] > div {
            border-radius: 5px !important;
            border: 1px solid var(--border) !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: var(--navy) !important;
            box-shadow: 0 0 0 3px rgba(14, 26, 43, 0.08) !important;
        }

        /* ---- sidebar ---- */
        section[data-testid="stSidebar"] {
            background: var(--navy);
            border-right: 1px solid var(--navy-deep);
        }
        section[data-testid="stSidebar"] * {
            color: #e7ebf1 !important;
        }
        section[data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.12) !important;
        }
        section[data-testid="stSidebar"] .stTextInput input,
        section[data-testid="stSidebar"] div[data-testid="stSelectbox"] > div {
            background-color: rgba(255,255,255,0.06) !important;
            border: 1px solid rgba(255,255,255,0.16) !important;
            color: #ffffff !important;
        }
        section[data-testid="stSidebar"] .stTextInput input::placeholder {
            color: rgba(231,235,241,0.4) !important;
        }
        section[data-testid="stSidebar"] .stButton>button {
            background: var(--gold) !important;
            border-color: var(--gold) !important;
            color: var(--navy-deep) !important;
        }
        section[data-testid="stSidebar"] .stButton>button:hover {
            background: var(--gold-light) !important;
            border-color: var(--gold-light) !important;
        }

        .sidebar-brand {
            font-family: 'Source Serif 4', serif;
            font-weight: 700;
            font-size: 1.12rem;
            color: #ffffff !important;
            margin-bottom: 0.1rem;
        }
        .sidebar-kicker {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.68rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--gold-light) !important;
            margin-bottom: 1.1rem;
        }
        .sb-label {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.7rem;
            font-weight: 500;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: rgba(231,235,241,0.55) !important;
            margin: 1rem 0 0.4rem 0;
        }
        .key-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.72rem;
            font-weight: 600;
            font-family: 'IBM Plex Mono', monospace;
            padding: 0.3rem 0.65rem;
            border-radius: 4px;
            margin-top: 0.5rem;
            background: rgba(182, 141, 64, 0.18);
            border: 1px solid rgba(182, 141, 64, 0.4);
            color: var(--gold-light) !important;
        }
        .key-pill.active {
            background: rgba(52, 211, 153, 0.15);
            border: 1px solid rgba(52, 211, 153, 0.4);
            color: #a7f3d0 !important;
        }
        .key-dot {
            width: 6px; height: 6px; border-radius: 50%;
            background: currentColor;
        }
        .sidebar-footnote {
            font-size: 0.74rem;
            color: rgba(231,235,241,0.5) !important;
            line-height: 1.5;
            margin-top: 0.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ======================================================================
# SESSION STATE
# ======================================================================
if "result" not in st.session_state:
    st.session_state.result = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of (role, text)
if "processing" not in st.session_state:
    st.session_state.processing = False


# ======================================================================
# SIDEBAR — INPUT + BYOK
# ======================================================================
with st.sidebar:
    st.markdown('<div class="sidebar-brand">🎞️ AI Video Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-kicker">Meeting & Video Intelligence</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-label">New Meeting / Video</div>', unsafe_allow_html=True)
    st.caption("Paste a YouTube URL or upload a local file path.")

    source = st.text_input(
        "Source",
        placeholder="https://youtube.com/watch?v=... or /path/to/file.mp4",
        label_visibility="collapsed",
    )

    language = st.selectbox("Language", ["english", "hinglish"], index=0)

    run = st.button("Process ▶", use_container_width=True, type="primary")

    st.divider()

    # ---- Bring Your Own Key ----
    st.markdown('<div class="sb-label">🔑 Bring Your Own Key</div>', unsafe_allow_html=True)
    st.caption("Use your own provider key for private, unmetered processing.")

    key_provider = st.selectbox(
        "Provider",
        ["OpenAI", "Anthropic (Claude)", "Google (Gemini)", "Groq"],
        label_visibility="collapsed",
        key="byok_provider",
    )

    user_api_key = st.text_input(
        "API Key",
        type="password",
        placeholder=f"Paste your {key_provider} key…",
        label_visibility="collapsed",
        key="byok_api_key",
    )

    if user_api_key:
        env_var_map = {
            "OpenAI": "OPENAI_API_KEY",
            "Anthropic (Claude)": "ANTHROPIC_API_KEY",
            "Google (Gemini)": "GOOGLE_API_KEY",
            "Groq": "GROQ_API_KEY",
        }
        os.environ[env_var_map[key_provider]] = user_api_key
        st.session_state["using_own_key"] = True
        st.markdown(
            "<span class='key-pill active'><span class='key-dot'></span>Using your key</span>",
            unsafe_allow_html=True,
        )
    else:
        st.session_state["using_own_key"] = False
        st.markdown(
            "<span class='key-pill'><span class='key-dot'></span>Using default key</span>",
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div class='sidebar-footnote'>Your key is held only for this session and is never logged or stored.</div>",
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown('<div class="sb-label">Output</div>', unsafe_allow_html=True)
    st.caption(
        "Title, summary, action items, key decisions, and open questions "
        "will appear on the right once processing finishes. Then chat with "
        "the transcript below."
    )

    if st.session_state.result:
        if st.button("↺ Start a new session", use_container_width=True):
            st.session_state.result = None
            st.session_state.chat_history = []
            st.rerun()


# ======================================================================
# MASTHEAD
# ======================================================================
st.markdown(
    """
    <div class="masthead">
        <div class="masthead-eyebrow">Transcription · Synthesis · Q&amp;A</div>
        <div class="app-title">AI Video Assistant</div>
        <div class="app-subtitle">Transcribe, summarize, and interrogate any meeting or video — with a grounded, citable record.</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ======================================================================
# RUN PIPELINE
# ======================================================================
if run:
    if not source.strip():
        st.warning("Please enter a YouTube URL or a file path first.")
    else:
        st.session_state.chat_history = []
        with st.spinner("Processing video — transcribing, summarizing, indexing…"):
            try:
                st.session_state.result = pipeline(source.strip(), language)
            except Exception as e:
                st.session_state.result = None
                st.error(f"Something went wrong: {e}")


# ======================================================================
# RESULTS
# ======================================================================
result = st.session_state.result

if result is None:
    st.info("Enter a source in the sidebar and click **Process** to get started.")
else:
    st.markdown('<span class="pill">PROCESSED</span>', unsafe_allow_html=True)
    st.markdown(f"## {result['title']}")

    tab_summary, tab_details, tab_transcript, tab_chat = st.tabs(
        ["Summary", "Details", "Transcript", "Chat"]
    )

    # ---- Summary tab ----
    with tab_summary:
        st.markdown(
            f'<div class="card"><h4>Summary</h4>{result["summary"]}</div>',
            unsafe_allow_html=True,
        )

    # ---- Details tab (action items / decisions / questions) ----
    with tab_details:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<div class="card"><h4>Action Items</h4>', unsafe_allow_html=True)
            st.write(result["action_items"])
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card"><h4>Key Decisions</h4>', unsafe_allow_html=True)
            st.write(result["key_decisions"])
            st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="card"><h4>Open Questions</h4>', unsafe_allow_html=True)
            st.write(result["open_questions"])
            st.markdown("</div>", unsafe_allow_html=True)

    # ---- Transcript tab ----
    with tab_transcript:
        st.markdown('<div class="card"><h4>Full Transcript</h4></div>', unsafe_allow_html=True)
        st.text_area(
            "Transcript",
            value=result["transcript"],
            height=400,
            label_visibility="collapsed",
        )

    # ---- Chat tab ----
    with tab_chat:
        st.caption("Ask questions about this meeting — answers are grounded in the transcript.")

        chat_container = st.container()
        with chat_container:
            for role, text in st.session_state.chat_history:
                if role == "user":
                    st.markdown(f'<div class="chat-user">{text}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-assistant">{text}</div>', unsafe_allow_html=True)

        with st.form("chat_form", clear_on_submit=True):
            col_input, col_btn = st.columns([5, 1])
            with col_input:
                question = st.text_input(
                    "Ask a question",
                    placeholder="e.g. What was decided about the budget?",
                    label_visibility="collapsed",
                )
            with col_btn:
                submitted = st.form_submit_button("Send", use_container_width=True)

        if submitted and question.strip():
            st.session_state.chat_history.append(("user", question.strip()))
            with st.spinner("Thinking…"):
                try:
                    answer = ask_questions(result["rag_chain"], question.strip())
                except Exception as e:
                    answer = f"Error: {e}"
            st.session_state.chat_history.append(("assistant", answer))
            st.rerun()