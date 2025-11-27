"""
Fake News Detection System – Streamlit Application (Colourful Clean UI)
"""
    
import streamlit as st
from src.extractor import extract_article_text
from src.predictor import FakeNewsPredictor
from src.fact_check import search_fact_check
from src.related_news import search_related_news
from src.utils import validate_url

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Fake News Detector",
    page_icon="📰",
    layout="centered",
    initial_sidebar_state="collapsed",
)

@st.cache_resource
def load_predictor():
    """Load predictor with caching"""
    try:
        detector = FakeNewsPredictor()
        st.success("✓ Model and vectorizer loaded successfully")
        return detector
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

# -------------------- CSS STYLING --------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    .page-wrapper {
        max-width: 780px;
        margin: 3rem auto 2.5rem auto;
        padding: 0 1rem 3rem 1rem;
    }

    .hero {
        text-align: center;
        margin-bottom: 2.2rem;
    }

    .hero-title {
        font-size: 2.4rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.4rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #e5e7eb;
        max-width: 540px;
        margin: 0 auto;
    }

    .hero-pill {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.3rem 0.75rem;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.8rem;
        color: #ffffff;
        display: inline-block;
        margin-bottom: 0.7rem;
    }

    .meta {
        font-size: 0.8rem;
        color: #9ca3af;
        margin-top: 0.55rem;
    }

    .url-label {
        font-size: 1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.55rem;
    }

    .stTextInput input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid transparent !important;
        border-image: linear-gradient(135deg, #667eea, #764ba2) 1 !important;
        border-radius: 999px !important;
        color: #ffffff !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1rem !important;
    }

    .stTextInput input::placeholder {
        color: #9ca3af !important;
    }

    .stTextInput input:focus {
        border-image: linear-gradient(135deg, #764ba2, #667eea) 1 !important;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3) !important;
    }

    .stTextInput {
        margin-bottom: 0.9rem !important;
    }

    .url-help {
        font-size: 0.85rem;
        color: #9ca3af;
        margin-bottom: 1.4rem;
    }

    .action-row {
        margin-top: 0.8rem;
        margin-bottom: 0.5rem;
    }

    .stButton > button {
        border-radius: 999px;
        padding: 0.65rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border: 2px solid transparent;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        box-shadow: 0 10px 24px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        box-shadow: 0 15px 30px rgba(118, 75, 162, 0.5);
        transform: translateY(-2px);
    }

    .badge-fake, .badge-real {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 1rem;
    }

    .badge-fake {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: #ffffff;
    }

    .badge-real {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff;
    }

    .result-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin: 0.6rem 0 0.2rem 0;
        color: #ffffff;
    }

    .result-conf {
        font-size: 0.84rem;
        color: #9ca3af;
        margin-bottom: 0.4rem;
    }

    .link-card {
        padding: 0.8rem 0.9rem;
        border-radius: 0.7rem;
        border: 1px solid rgba(102, 126, 234, 0.3);
        background: rgba(255, 255, 255, 0.05);
        margin-bottom: 0.5rem;
        backdrop-filter: blur(10px);
    }

    .link-title {
        font-size: 0.94rem;
        font-weight: 600;
        color: #818cf8;
        text-decoration: none;
    }

    .link-title:hover {
        color: #a5b4fc;
        text-decoration: underline;
    }

    .link-snippet {
        font-size: 0.8rem;
        color: #d1d5db;
        margin-top: 0.25rem;
    }

    .link-source {
        font-size: 0.78rem;
        color: #9ca3af;
        margin-top: 0.15rem;
    }

    .about-section {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 0.7rem;
        padding: 1.5rem;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
    }

    .about-section h3 {
        color: #ffffff;
        margin-bottom: 1rem;
    }

    .about-section p, .about-section li {
        color: #e5e7eb;
        line-height: 1.6;
    }

    .footer {
        text-align: center;
        font-size: 0.8rem;
        color: #9ca3af;
        margin-top: 2rem;
    }

    /* Streamlit specific overrides for dark theme */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        color: #9ca3af;
    }

    .stTabs [aria-selected="true"] {
        color: #ffffff;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        color: #ffffff !important;
    }

    .stMarkdown {
        color: #e5e7eb;
    }

    .stAlert {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        color: #ffffff !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- HELPERS --------------------
def show_prediction(result: dict, title: str):
    label = result.get("label")
    conf = result.get("confidence", 0.0)

    if label == "Fake":
        badge_html = '<span class="badge-fake">⚠️ Likely FAKE news</span>'
    elif label == "Real":
        badge_html = '<span class="badge-real">✅ Likely REAL news</span>'
    else:
        st.error(result.get("error", "Prediction failed."))
        return

    st.markdown(badge_html, unsafe_allow_html=True)
    st.markdown(
        f'<p class="result-title">{title or "Untitled article"}</p>',
        unsafe_allow_html=True,
    )


def show_links(links, heading: str, icon: str):
    if not links:
        st.info(f"No {heading.lower()} found for this article yet.")
        return

    st.markdown(f"**{icon} {heading}**")
    for link in links:
        st.markdown(
            f"""
            <div class="link-card">
                <a class="link-title" href="{link['url']}" target="_blank">{link['title']}</a>
                <p class="link-snippet">{link['snippet']}</p>
                <p class="link-source">Source: {link['source']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# -------------------- MAIN APP --------------------
def main():
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)

    # Hero
    st.markdown(
        """
        <div class="hero">
            <div class="hero-pill">
                <span>✨</span> AI-assisted news detection
            </div>
            <h1 class="hero-title">Fake News Detector</h1>
            <p class="hero-subtitle">
                Paste a news article URL or text and let the model estimate whether the content is more
                likely to be <strong>real</strong> or <strong>fake</strong>. You also get links
                to help you cross-check the story.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Main white card
    st.markdown('<div class="content-card">', unsafe_allow_html=True)

    # Load predictor
    predictor = load_predictor()
    
    if predictor is None:
        st.error("Unable to load the model. Please check if the model files exist.")
        return

    # Input options
    input_mode = st.radio(
        "Choose input method:",
        ["URL", "Text"],
        horizontal=True,
        label_visibility="visible"
    )

    if input_mode == "URL":
        st.markdown('<div class="url-label">News article URL</div>', unsafe_allow_html=True)
        url = st.text_input(
            label="",
            placeholder="https://example.com/news-article",
            label_visibility="collapsed",
            key="news_url",
        )
        text_input = ""
        st.markdown(
            '<div class="url-help">Paste the full URL of an online news article you want to check.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="url-label">News text or headline</div>', unsafe_allow_html=True)
        text_input = st.text_area(
            label="",
            placeholder="Enter news headline or paste article content here...",
            height=150,
            label_visibility="collapsed",
            key="news_text",
        )
        url = ""
        st.markdown(
            '<div class="url-help">⚠️ Note: The model analyzes text patterns, it cannot verify if events actually happened. Cross-check with reliable sources.</div>',
            unsafe_allow_html=True,
        )

    # Button row
    st.markdown('<div class="action-row">', unsafe_allow_html=True)
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        analyze = st.button("Analyze article")
    st.markdown('</div>', unsafe_allow_html=True)

    # Logic for URL or Text
    if analyze and not url.strip() and not text_input.strip():
        st.warning("Please enter a news article URL or paste text to analyze.")

    # ---- CASE 1: TEXT PASTED ----
    elif analyze and text_input.strip():

        article_title = text_input.strip()[:100] if len(text_input.strip()) < 200 else "User provided text"
        article_text = text_input.strip()

        with st.spinner("Analyzing text..."):
            # Get model prediction based on text content
            result = predictor.predict(article_text)

            if result.get("error"):
                st.error(f"Prediction error: {result['error']}")
                return
        
        # Search for related news for user to verify
        with st.spinner("Searching for related news..."):
            query = article_title
            related_links = search_related_news(query)

        st.markdown("---")
        
        # Warning box for text input
        st.warning(
            "⚠️ **Important Limitation**: This model analyzes text patterns and language style, "
            "NOT factual accuracy. It cannot verify if events actually happened. "
            "Always cross-check with multiple trusted news sources below."
        )
        
        show_prediction(result, article_title)

        # Tabs - removed fact-check tab
        tab_overview, tab_article, tab_links = st.tabs(
            ["Overview", "Article text", "Related news"]
        )

        with tab_overview:
            st.write(
                "**What the model does:**\n"
                "- Analyzes word patterns, writing style, and linguistic features\n"
                "- Compares against patterns learned from fake vs real news datasets\n"
                "- Searches for related coverage from trusted sources\n\n"
                "**What the model CANNOT do:**\n"
                "- Verify if events actually occurred\n"
                "- Check credibility of sources\n"
                "- Access real-time information or current events\n\n"
                "**Always verify with the related news sources in the next tab!**"
            )

        with tab_article:
            st.write("### Your input text")
            st.text_area(
                label="",
                value=article_text[:6000],
                height=260,
                label_visibility="collapsed",
            )

        with tab_links:
            show_links(related_links, "Related news from trusted sources", "📰")

    # ---- CASE 2: URL ANALYZED ----
    elif analyze and url.strip():

        if not validate_url(url):
            st.error("Please enter a valid URL starting with http:// or https://")

        else:
            with st.spinner("Extracting article and running the model..."):

                # 1. Extract article
                article_data = extract_article_text(url)

                if not article_data.get("success") or not article_data.get("full_text"):
                    st.error(
                        f"Could not extract the article content. "
                        f"{article_data.get('error', 'Unknown error.')}"
                    )
                    return

                article_title = article_data.get("title") or "Untitled article"
                article_text = article_data["full_text"]

                # 2. Predict
                result = predictor.predict(article_text)

                if result.get("error"):
                    st.error(f"Prediction error: {result['error']}")
                    return

            st.markdown("---")
            show_prediction(result, article_title)

            # Tabs
            tab_overview, tab_article, tab_links = st.tabs(
                ["Overview", "Article text", "Related news"]
            )

            with tab_overview:
                st.write(
                    "**What the model does:**\n"
                    "- Analyzes word patterns, writing style, and linguistic features\n"
                    "- Compares against patterns learned from fake vs real news datasets\n"
                    "- Searches for related coverage from trusted sources\n\n"
                    "**What the model CANNOT do:**\n"
                    "- Verify if events actually occurred\n"
                    "- Check credibility of sources\n"
                    "- Access real-time information or current events\n\n"
                    "**Always verify with the related news sources in the next tab!**"
                )

            with tab_article:
                st.write("### Extracted article text (preview)")
                st.text_area(
                    label="",
                    value=article_text[:6000],
                    height=260,
                    label_visibility="collapsed",
                )

            with tab_links:
                query = article_title
                with st.spinner("Searching for related coverage from other sources..."):
                    related_links = search_related_news(query)
                    show_links(related_links, "Similar news from other sources", "📰")

    # About section - always visible
    st.markdown(
        """
        <div class="about-section">
            <h3>ℹ️ About This Tool</h3>
            <p><strong>How it works</strong></p>
            <ol>
                <li>You paste a news article URL or text.</li>
                <li>The app extracts or uses the provided text.</li>
                <li>The text is converted into TF–IDF features and passed to a Logistic Regression model.</li>
                <li>The model analyzes language patterns (NOT factual accuracy).</li>
                <li>The model outputs a label (Real/Fake) and a confidence score.</li>
                <li>The app suggests fact-check pages or similar news so you can cross-check.</li>
            </ol>
            <p><strong>⚠️ Critical Limitations</strong></p>
            <p><strong>This model CANNOT verify if events actually happened.</strong> It only analyzes writing patterns and style. A well-written fake story may be classified as "real" and vice versa. <strong>Always verify claims with multiple trusted sources.</strong> This tool is an aid to critical thinking, not a replacement for thorough fact-checking.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)  # close content-card

    st.markdown(
        '<div class="footer">Fake News Detector • Built with Streamlit & Machine Learning</div>',
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)  # close page-wrapper


# -------------------- RUN APP --------------------
if __name__ == "__main__":
    main()
