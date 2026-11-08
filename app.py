import hashlib
import streamlit as st

from src.pdf_processor import extract_text_from_pdf
from src.text_chunker import split_text_into_chunks
from src.embedding import generate_embeddings
from src.vector_store import build_vector_store, search_similar_chunks
from src.gemini_client import generate_answer


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #faf9fe;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 7rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #211b3c;
    border-right: 1px solid #332b53;
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] .stButton button {
    background: #7660d9;
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 10px;
    font-weight: 600;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: #8975ed;
    border: none;
}

/* HERO */

.hero {
    background: linear-gradient(
        120deg,
        #f0ebff,
        #ffffff 60%,
        #eeeaff
    );

    border: 1px solid #e9e2ff;
    border-radius: 22px;
    padding: 32px 35px;
    margin-bottom: 28px;

    box-shadow: 0 8px 30px rgba(70, 49, 130, 0.04);
}

.hero-label {
    color: #8064dc !important;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.hero h1 {
    font-family: 'Manrope', sans-serif;
    font-size: 36px;
    font-weight: 800;
    color: #292343 !important;
    margin: 0;
    line-height: 1.3;
}

.hero p {
    color: #77728d !important;
    font-size: 15px;
    margin-top: 10px;
    margin-bottom: 0;
}

/* SECTION HEADINGS */

.section-title {
    color: #302b4c !important;
    font-family: 'Manrope', sans-serif;
    font-size: 21px;
    font-weight: 800;
    margin-top: 25px;
    margin-bottom: 15px;
}

.section-subtitle {
    color: #858097 !important;
    font-size: 13px;
    margin-top: -10px;
    margin-bottom: 20px;
}

/* INFO CARDS */

.info-card {
    background: #ffffff;
    border: 1px solid #ece8f5;
    border-radius: 17px;
    padding: 20px;
    box-shadow: 0 5px 20px rgba(46, 36, 92, 0.035);
}

.info-card h3 {
    color: #302b4c !important;
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 8px;
}

.info-card p {
    color: #858097 !important;
    font-size: 13px;
    line-height: 1.6;
    margin-bottom: 0;
}

/* METRICS */

[data-testid="stMetric"] {
    background: #ffffff;
    padding: 17px;
    border: 1px solid #ece8f5;
    border-radius: 15px;
}

[data-testid="stMetricLabel"] {
    color: #858097 !important;
}

[data-testid="stMetricValue"] {
    color: #302b4c !important;
    font-weight: 800;
}

/* UPLOADER */

[data-testid="stFileUploader"] {
    background: #ffffff;
    border: 1px dashed #c9bdf0;
    border-radius: 15px;
    padding: 15px;
}

/* BUTTONS */

.stButton button {
    border-radius: 11px;
    font-weight: 700;
    transition: all 0.2s ease;
}

.stButton button[kind="primary"] {
    background: linear-gradient(135deg, #8064e8, #6548c8);
    color: white !important;
    border: none;
    box-shadow: 0 5px 15px rgba(112, 82, 210, 0.18);
}

.stButton button[kind="primary"]:hover {
    background: linear-gradient(135deg, #9279f1, #7356d9);
    box-shadow: 0 7px 20px rgba(112, 82, 210, 0.25);
    transform: translateY(-1px);
}

/* CHAT MESSAGES */

[data-testid="stChatMessage"] {
    padding: 16px 18px;
    margin-bottom: 13px;
    border: 1px solid #eeecf5;
    border-radius: 17px;
    background: #ffffff !important;
    color: #27243f !important;
    box-shadow: 0 4px 14px rgba(40, 34, 80, 0.035);
}

[data-testid="stChatMessage"] * {
    color: #27243f !important;
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li {
    color: #27243f !important;
    line-height: 1.7;
}

/* PREMIUM CHAT INPUT */

[data-testid="stChatInput"] {
    background: linear-gradient(
        120deg,
        #ffffff,
        #f7f4ff
    ) !important;

    border: 1.5px solid #ded5f8 !important;
    border-radius: 22px !important;
    padding: 7px 10px !important;

    box-shadow:
        0 8px 28px rgba(76, 55, 145, 0.09),
        0 2px 6px rgba(76, 55, 145, 0.035) !important;

    transition: all 0.25s ease !important;
}

[data-testid="stChatInput"]:focus-within {
    border: 1.5px solid #9579ed !important;

    box-shadow:
        0 0 0 4px rgba(137, 106, 231, 0.12),
        0 10px 30px rgba(76, 55, 145, 0.12) !important;

    background: #ffffff !important;
}

[data-testid="stChatInput"] > div {
    background: transparent !important;
    border: none !important;
}

[data-testid="stChatInput"] textarea {
    color: #292641 !important;
    background: transparent !important;
    -webkit-text-fill-color: #292641 !important;
    caret-color: #8062e9 !important;

    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    line-height: 1.6 !important;

    padding: 11px 10px !important;
    border: none !important;
    box-shadow: none !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #9892aa !important;
    -webkit-text-fill-color: #9892aa !important;
    opacity: 1 !important;
    font-weight: 400 !important;
}

[data-testid="stChatInput"] textarea:focus {
    outline: none !important;
    box-shadow: none !important;
}

[data-testid="stChatInputSubmitButton"] {
    background: linear-gradient(
        135deg,
        #8c70ec,
        #6548c8
    ) !important;

    border: none !important;
    border-radius: 14px !important;
    width: 42px !important;
    height: 42px !important;
    min-width: 42px !important;

    box-shadow: 0 4px 12px rgba(105, 76, 202, 0.22) !important;
    transition: all 0.2s ease !important;
}

[data-testid="stChatInputSubmitButton"]:hover {
    background: linear-gradient(
        135deg,
        #a18af4,
        #7658da
    ) !important;

    transform: translateY(-2px) !important;
    box-shadow: 0 7px 16px rgba(105, 76, 202, 0.3) !important;
}

[data-testid="stChatInputSubmitButton"] svg {
    fill: #ffffff !important;
    color: #ffffff !important;
}

/* SOURCES */

[data-testid="stExpander"] {
    border: 1px solid #ece9f4;
    border-radius: 13px;
    background: #ffffff !important;
}

[data-testid="stExpander"] p,
[data-testid="stExpander"] span,
[data-testid="stExpander"] summary {
    color: #45405c !important;
}

/* WELCOME PANEL */

.welcome-panel {
    text-align: center;

    background: linear-gradient(
        135deg,
        #ffffff,
        #f6f2ff
    );

    border: 1px solid #ece6fc;
    border-radius: 20px;
    padding: 45px 25px;
    margin-top: 20px;
}

.welcome-icon {
    font-size: 42px;
    margin-bottom: 12px;
}

.welcome-panel h3 {
    color: #302b4c !important;
    font-size: 21px;
    font-weight: 800;
}

.welcome-panel p {
    color: #858097 !important;
    font-size: 14px;
    line-height: 1.7;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #9892aa !important;
    font-size: 12px;
    padding: 30px 0 10px;
}

/* RESPONSIVE */

@media (max-width: 768px) {

    .hero {
        padding: 23px;
    }

    .hero h1 {
        font-size: 27px;
    }

    .block-container {
        padding-top: 1rem;
    }

    [data-testid="stChatInput"] {
        border-radius: 17px !important;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "index" not in st.session_state:
    st.session_state.index = None

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "processed_file_hash" not in st.session_state:
    st.session_state.processed_file_hash = None

if "filename" not in st.session_state:
    st.session_state.filename = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html("""
    <div style="padding: 15px 5px 25px;">
        <div style="font-size: 30px;">📚</div>
        <h2 style="margin: 5px 0 0; font-weight: 800;">
            DocuMind AI
        </h2>
        <p style="font-size: 12px; color: #c3bbdf;">
            Your intelligent document assistant
        </p>
    </div>
    """)

    st.markdown("---")

    st.markdown("### 📄 Document")

    if st.session_state.filename:
        st.success(f"Loaded: {st.session_state.filename}")
    else:
        st.info("No document uploaded yet.")

    st.markdown("---")

    st.markdown("### ⚙️ Actions")

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    if st.button("🔄 Reset document", use_container_width=True):

        st.session_state.index = None
        st.session_state.chunks = []
        st.session_state.chat_history = []
        st.session_state.processed_file_hash = None
        st.session_state.filename = None

        st.rerun()

    st.markdown("---")

    st.html("""
    <div style="font-size: 12px; color: #c3bbdf; line-height: 1.8;">
        <b>Powered by</b><br>
        • Google Gemini<br>
        • Sentence Transformers<br>
        • FAISS Vector Search<br>
        • Streamlit
    </div>
    """)


# ============================================================
# HERO SECTION
# ============================================================

st.html("""
<div class="hero">

    <div class="hero-label">
        ✦ AI POWERED DOCUMENT INTELLIGENCE
    </div>

    <h1>Knowledge, within reach.</h1>

    <p>
        Upload your PDF, ask questions, and get intelligent
        answers directly from your document.
    </p>

</div>
""")


# ============================================================
# DOCUMENT UPLOAD
# ============================================================

st.html("""
<div class="section-title">📂 Upload your document</div>
<div class="section-subtitle">
    Choose a PDF document to begin your conversation.
</div>
""")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"],
    label_visibility="collapsed"
)


# ============================================================
# PROCESS PDF
# ============================================================

if uploaded_file is not None:

    pdf_bytes = uploaded_file.getvalue()

    current_file_hash = hashlib.md5(
        pdf_bytes
    ).hexdigest()

    if (
        st.session_state.processed_file_hash is not None
        and current_file_hash != st.session_state.processed_file_hash
    ):

        st.session_state.index = None
        st.session_state.chunks = []
        st.session_state.chat_history = []
        st.session_state.filename = None
        st.session_state.processed_file_hash = None

    col1, col2 = st.columns([3, 1])

    with col1:

        st.html(f"""
        <div class="info-card">
            <h3>📄 {uploaded_file.name}</h3>
            <p>
                File size: {len(pdf_bytes) / (1024 * 1024):.2f} MB
                &nbsp; • &nbsp; PDF document
            </p>
        </div>
        """)

    with col2:

        st.write("")

        process_button = st.button(
            "✨ Process PDF",
            type="primary",
            use_container_width=True
        )

    if process_button:

        try:

            with st.spinner(
                "Reading your PDF and building the AI knowledge base..."
            ):

                extracted_text = extract_text_from_pdf(pdf_bytes)

                chunks = split_text_into_chunks(
                    extracted_text,
                    chunk_size=500,
                    overlap=100
                )

                if not chunks:
                    raise ValueError(
                        "No readable text chunks were generated."
                    )

                embeddings = generate_embeddings(chunks)

                index = build_vector_store(
                    chunks,
                    embeddings
                )

                st.session_state.index = index
                st.session_state.chunks = chunks
                st.session_state.processed_file_hash = current_file_hash
                st.session_state.filename = uploaded_file.name
                st.session_state.chat_history = []

            st.success(
                "🎉 Your PDF is ready! You can now ask questions."
            )

            st.rerun()

        except Exception as error:

            st.error(f"Unable to process this PDF: {error}")


# ============================================================
# DOCUMENT METRICS
# ============================================================

if st.session_state.index is not None:

    st.html("""
    <div class="section-title">📊 Document overview</div>
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Document", "Ready")

    with col2:
        st.metric("Text chunks", len(st.session_state.chunks))

    with col3:
        st.metric("Vector dimensions", "384")


# ============================================================
# CHAT SECTION
# ============================================================

st.html("""
<div class="section-title">💬 Chat with your PDF</div>

<div class="section-subtitle">
    Ask questions and explore the information inside your document.
</div>
""")


# ============================================================
# WELCOME PANEL
# ============================================================

if st.session_state.index is None:

    st.html("""
    <div class="welcome-panel">

        <div class="welcome-icon">📖</div>

        <h3>Your document journey starts here</h3>

        <p>
            Upload a PDF and click <b>Process PDF</b>.<br>
            DocuMind AI will understand your document
            and help you find the information you need.
        </p>

    </div>
    """)


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.chat_history:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            with st.expander("📚 View document sources"):

                for source in message["sources"]:

                    st.markdown(
                        f"**Source Chunk {source['chunk_index'] + 1}**"
                    )

                    st.caption(
                        f"Similarity score: {source['score']:.4f}"
                    )

                    st.write(source["text"])

                    st.markdown("---")


# ============================================================
# CHAT INPUT AND GEMINI RESPONSE
# ============================================================

if st.session_state.index is not None:

    user_question = st.chat_input(
        "Ask something about your PDF..."
    )

    if user_question:

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question
        })

        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):

            with st.spinner("DocuMind AI is thinking..."):

                try:

                    search_results = search_similar_chunks(
                        user_question,
                        st.session_state.index,
                        st.session_state.chunks,
                        top_k=3
                    )

                    if not search_results:

                        answer = (
                            "I couldn't find relevant information "
                            "in the uploaded document."
                        )

                        sources = []

                    else:

                        context = "\n\n".join(
                            result["text"]
                            for result in search_results
                        )

                        answer = generate_answer(
                            context,
                            user_question
                        )

                        sources = search_results

                    st.markdown(answer)

                    if sources:

                        with st.expander("📚 View document sources"):

                            for source in sources:

                                st.markdown(
                                    f"**Source Chunk {source['chunk_index'] + 1}**"
                                )

                                st.caption(
                                    f"Similarity score: {source['score']:.4f}"
                                )

                                st.write(source["text"])

                                st.markdown("---")

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })

                except Exception as error:

                    error_message = (
                        f"Sorry, something went wrong: {error}"
                    )

                    st.error(error_message)

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": error_message,
                        "sources": []
                    })


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">
    Built with ❤️ using Python, Streamlit, FAISS & Google Gemini
    <br><br>
    DocuMind AI © 2026
</div>
""")