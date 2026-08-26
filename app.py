"""
AI Video Assistant — Streamlit UI
Wraps the existing CLI pipeline (pipeline.py) in a minimal, modern web UI.
Run with: streamlit run app.py
"""

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
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ======================================================================
# MINIMAL / MODERN CSS
# ======================================================================
st.markdown(
    """
    <style>
        /* ---- global ---- */
        html, body, [class*="css"]  {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        .block-container {
            padding-top: 2.2rem;
            padding-bottom: 3rem;
            max-width: 1100px;
        }

        /* ---- hide default chrome ---- */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* ---- headline ---- */
        .app-title {
            font-size: 1.9rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 0.15rem;
        }
        .app-subtitle {
            color: rgba(120,120,120,0.9);
            font-size: 0.95rem;
            margin-bottom: 1.6rem;
        }

        /* ---- cards ---- */
        .card {
            background: var(--background-color, #ffffff);
            border: 1px solid rgba(128,128,128,0.15);
            border-radius: 14px;
            padding: 1.4rem 1.5rem;
            margin-bottom: 1rem;
        }
        .card h4 {
            margin-top: 0;
            margin-bottom: 0.6rem;
            font-size: 0.95rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: rgba(120,120,120,0.9);
        }

        /* ---- pills / status ---- */
        .pill {
            display: inline-block;
            padding: 0.2rem 0.7rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
            background: rgba(16,163,127,0.12);
            color: #10a37f;
            margin-bottom: 0.8rem;
        }

        /* ---- buttons ---- */
        .stButton>button {
            border-radius: 10px;
            font-weight: 600;
            padding: 0.55rem 1.2rem;
            border: none;
        }

        /* ---- chat bubbles ---- */
        .chat-user {
            background: rgba(16,163,127,0.10);
            border-radius: 12px;
            padding: 0.6rem 0.9rem;
            margin-bottom: 0.4rem;
        }
        .chat-assistant {
            background: rgba(128,128,128,0.08);
            border-radius: 12px;
            padding: 0.6rem 0.9rem;
            margin-bottom: 0.9rem;
        }

        /* ---- sidebar ---- */
        section[data-testid="stSidebar"] {
            border-right: 1px solid rgba(128,128,128,0.15);
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
# SIDEBAR — INPUT
# ======================================================================
with st.sidebar:
    st.markdown("### 🎬 New meeting / video")
    st.caption("Paste a YouTube URL or upload a local file path.")

    source = st.text_input(
        "Source",
        placeholder="https://youtube.com/watch?v=... or /path/to/file.mp4",
        label_visibility="collapsed",
    )

    language = st.selectbox("Language", ["english", "hinglish"], index=0)

    run = st.button("Process ▶", use_container_width=True, type="primary")

    st.divider()
    st.caption("Output")
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
# HEADER
# ======================================================================
st.markdown('<div class="app-title">AI Video Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Transcribe, summarize, and chat with any meeting or video.</div>',
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
    st.markdown(f'<span class="pill">✔ Processed</span>', unsafe_allow_html=True)
    st.markdown(f"## 📌 {result['title']}")

    tab_summary, tab_details, tab_transcript, tab_chat = st.tabs(
        ["📋 Summary", "✅ Details", "📝 Transcript", "💬 Chat"]
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
            st.markdown('<div class="card"><h4>✅ Action Items</h4>', unsafe_allow_html=True)
            st.write(result["action_items"])
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card"><h4>🔑 Key Decisions</h4>', unsafe_allow_html=True)
            st.write(result["key_decisions"])
            st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="card"><h4>❓ Open Questions</h4>', unsafe_allow_html=True)
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
                    st.markdown(f'<div class="chat-user">🧑 {text}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-assistant">🤖 {text}</div>', unsafe_allow_html=True)

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