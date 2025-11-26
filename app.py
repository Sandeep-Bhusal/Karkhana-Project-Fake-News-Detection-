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

# -------------------- CSS STYLING --------------------
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #e0e7ff 0, #f5f5f7 45%, #fef3c7 100%);
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
        color: #111827;
        margin-bottom: 0.4rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #4b5563;
        max-width: 540px;
        margin: 0 auto;
    }

    .hero-pill {
        background: rgba(99, 102, 241, 0.12);
        padding: 0.3rem 0.75rem;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.8rem;
        color: #4338ca;
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
        color: #1f2937;
        margin-bottom: 0.55rem;
    }

    .stTextInput {
        margin-bottom: 0.9rem !important;
    }

    .url-help {
        font-size: 0.85rem;
        color: #6b7280;
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
        border: none;
        background: linear-gradient(135deg, #4f46e5, #3b82f6);
        color: #ffffff;
        box-shadow: 0 10px 24px rgba(37, 99, 235, 0.4);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #4338ca, #2563eb);
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
        background-color: #fef2f2;
        color: #b91c1c;
    }

    .badge-real {
        background-color: #ecfdf3;
        color: #15803d;
    }

    .result-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin: 0.6rem 0 0.2rem 0;
        color: #111827;
    }

    .result-conf {
        font-size: 0.84rem;
        color: #6b7280;
        margin-bottom: 0.4rem;
    }

    .link-card {
        padding: 0.8rem 0.9rem;
        border-radius: 0.7rem;
        border: 1px solid #e5e7eb;
        background: #f9fafb;
        margin-bottom: 0.5rem;
    }

    .link-title {
        font-size: 0.94rem;
        font-weight: 600;
        color: #1d4ed8;
        text-decoration: none;
    }

    .link-title:hover {
        text-decoration: underline;
    }

    .link-snippet {
        font-size: 0.8rem;
        color: #4b5563;
        margin-top: 0.25rem;
    }

    .link-source {
        font-size: 0.78rem;
        color: #9ca3af;
        margin-top: 0.15rem;
    }

    .footer {
        text-align: center;
        font-size: 0.8rem;
        color: #a1a1aa;
        margin-top: 2rem;
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
    st.markdown(
        f'<p class="result-conf">Model confidence: {conf:.1f}%</p>',
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
                Paste a news article URL and let the model estimate whether the content is more
                likely to be <strong>real</strong> or <strong>fake</strong>. You also get links
                to help you cross-check the story.
            </p>
            <p class="meta">
                Model: TF–IDF + Logistic Regression · Interface: Streamlit Web App
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Main white card
    st.markdown('<div class="content-card">', unsafe_allow_html=True)

    # URL Input
    st.markdown('<div class="url-label">News article URL</div>', unsafe_allow_html=True)
    url = st.text_input(
        label="",
        placeholder="https://example.com/news-article",
        label_visibility="collapsed",
        key="news_url",
    )

    st.markdown(
        '<div class="url-help">Paste the full URL of an online news article you want to check.</div>',
        unsafe_allow_html=True,
    )

    # Button row
    st.markdown('<div class="action-row">', unsafe_allow_html=True)
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        analyze = st.button("Analyze article")
    st.markdown('</div>', unsafe_allow_html=True)

    # Logic
    if analyze and not url.strip():
        st.warning("Please enter a news article URL before analysing.")

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
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown(
                        '<div class="footer">Fake News Detector • Built with Streamlit & Machine Learning</div>',
                        unsafe_allow_html=True,
                    )
                    return

                article_title = article_data.get("title") or "Untitled article"
                article_text = article_data["full_text"]

                # 2. Predict
                predictor = FakeNewsPredictor()
                result = predictor.predict(article_text)

                if result.get("error"):
                    st.error(f"Prediction error: {result['error']}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown(
                        '<div class="footer">Fake News Detector • Built with Streamlit & Machine Learning</div>',
                        unsafe_allow_html=True,
                    )
                    return

            st.markdown("---")
            show_prediction(result, article_title)

            # Tabs
            tab_overview, tab_article, tab_links = st.tabs(
                ["Overview", "Article text", "Fact-check & similar news"]
            )

            with tab_overview:
                st.write(
                    "The prediction above is based on patterns learned from a labelled "
                    "fake/real news dataset. Treat it as a signal, not a final verdict."
                )
                st.write(
                    "- Check who published the article.\n"
                    "- Compare it with coverage from other outlets.\n"
                    "- Use the links in the next tab to verify further."
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

                if result["label"] == "Fake":
                    with st.spinner("Searching for fact-check resources..."):
                        fact_links = search_fact_check(query)
                    show_links(fact_links, "Fact-check resources", "🛡️")

                    with st.spinner("Searching for verified coverage..."):
                        verified_links = search_related_news(query)
                    st.markdown("")
                    show_links(verified_links, "Verified coverage from other sources", "📰")

                else:
                    with st.spinner("Searching for similar coverage from other sources..."):
                        related_links = search_related_news(query)
                    show_links(related_links, "Similar news from other sources", "📰")

    # About + footer
    with st.expander("About this tool"):
        st.markdown(
            """
            **How it works**

            1. You paste a news article URL.  
            2. The app extracts the main article text.  
            3. The text is converted into TF–IDF features and passed to a Logistic Regression model.  
            4. The model outputs a label (Real/Fake) and a confidence score.  
            5. The app suggests fact-check pages or similar news so you can cross-check.

            **Important**

            This tool is an aid to critical thinking, not a replacement.  
            Always rely on multiple trusted sources for important information.
            """
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
