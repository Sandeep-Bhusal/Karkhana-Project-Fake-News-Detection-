"""
Fake News Detection System - Streamlit Application
"""
import streamlit as st
import os
from src.extractor import extract_article_text
from src.predictor import FakeNewsPredictor
from src.fact_check import search_fact_check
from src.related_news import search_related_news
from src.utils import validate_url

# Page configuration
st.set_page_config(
    page_title="Fake News Detector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Google-like interface
st.markdown("""
    <style>
    /* Main background and spacing */
    .main {
        padding-top: 2rem;
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        padding: 3rem 0 2rem 0;
    }
    
    .app-title {
        font-size: 3.5rem;
        font-weight: 300;
        color: #1a73e8;
        margin-bottom: 0.5rem;
        font-family: 'Arial', sans-serif;
    }
    
    .app-subtitle {
        font-size: 1.1rem;
        color: #5f6368;
        margin-bottom: 2rem;
    }
    
    /* Search box styling */
    .search-container {
        max-width: 700px;
        margin: 0 auto 3rem auto;
    }
    
    /* Result cards */
    .result-card {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        border-left: 4px solid #1a73e8;
    }
    
    .fake-card {
        border-left-color: #d93025;
        background: #fef7f7;
    }
    
    .real-card {
        border-left-color: #1e8e3e;
        background: #f6faf8;
    }
    
    /* Link styling */
    .news-link {
        color: #1a0dab;
        text-decoration: none;
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    .news-link:hover {
        text-decoration: underline;
    }
    
    .news-snippet {
        color: #4d5156;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    
    .news-source {
        color: #5f6368;
        font-size: 0.85rem;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #5f6368;
        font-size: 0.9rem;
        margin-top: 3rem;
        border-top: 1px solid #e0e0e0;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #1a73e8;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 2rem;
        font-size: 1rem;
        cursor: pointer;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #1557b0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

def display_header():
    """Display the application header"""
    st.markdown("""
        <div class="header-container">
            <div class="app-title">🔍 Fake News Detector</div>
            <div class="app-subtitle">Verify news authenticity with AI-powered analysis</div>
        </div>
    """, unsafe_allow_html=True)

def display_footer():
    """Display the application footer"""
    st.markdown("""
        <div class="footer">
            <p>🛡️ <strong>Fake News Detector</strong> | AI-Powered News Verification</p>
            <p style="font-size: 0.8rem;">Always verify information from multiple trusted sources</p>
            <p style="font-size: 0.75rem; color: #999;">© 2025 | Built with Streamlit & Machine Learning</p>
        </div>
    """, unsafe_allow_html=True)

def display_prediction_result(result, article_title):
    """
    Display prediction result with styling
    
    Args:
        result (dict): Prediction result dictionary
        article_title (str): Title of the article
    """
    if result['label'] == 'Fake':
        st.markdown(f"""
            <div class="result-card fake-card">
                <h2 style="color: #d93025; margin-bottom: 0.5rem;">⚠️ Likely FAKE News</h2>
                <p style="font-size: 1.1rem; margin-bottom: 0.5rem;"><strong>{article_title}</strong></p>
                <p style="color: #666;">Confidence: {result['confidence']:.1f}%</p>
            </div>
        """, unsafe_allow_html=True)
    elif result['label'] == 'Real':
        st.markdown(f"""
            <div class="result-card real-card">
                <h2 style="color: #1e8e3e; margin-bottom: 0.5rem;">✓ Likely REAL News</h2>
                <p style="font-size: 1.1rem; margin-bottom: 0.5rem;"><strong>{article_title}</strong></p>
                <p style="color: #666;">Confidence: {result['confidence']:.1f}%</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"Error: {result.get('error', 'Unknown error occurred')}")

def display_related_links(links, title, icon):
    """
    Display related links in a clean format
    
    Args:
        links (list): List of link dictionaries
        title (str): Section title
        icon (str): Icon emoji
    """
    if links:
        st.markdown(f"### {icon} {title}")
        
        for i, link in enumerate(links, 1):
            st.markdown(f"""
                <div style="margin: 1rem 0; padding: 1rem; background: #f8f9fa; border-radius: 4px;">
                    <a href="{link['url']}" target="_blank" class="news-link">{link['title']}</a>
                    <p class="news-snippet">{link['snippet']}</p>
                    <p class="news-source">Source: {link['source']}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info(f"No {title.lower()} found at the moment.")

def main():
    """Main application function"""
    
    # Display header
    display_header()
    
    # Initialize session state
    if 'analyzed' not in st.session_state:
        st.session_state.analyzed = False
    
    # Search container
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Input field
    url_input = st.text_input(
        "",
        placeholder="Enter news article URL here...",
        key="url_input",
        label_visibility="collapsed"
    )
    
    # Search button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        search_button = st.button("🔍 Analyze News", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process when search button is clicked
    if search_button and url_input:
        
        # Validate URL
        if not validate_url(url_input):
            st.error(" Please enter a valid URL (must start with http:// or https://)")
            return
        
        # Show loading spinner
        with st.spinner("🔄 Analyzing article... Please wait..."):
            
            # Step 1: Extract article text
            st.info("Extracting article content...")
            article_data = extract_article_text(url_input)
            
            if not article_data['success'] or not article_data['full_text']:
                st.error(f" Failed to extract article: {article_data.get('error', 'Unknown error')}")
                return
            
            article_title = article_data['title'] or "Untitled Article"
            article_text = article_data['full_text']
            
            # Step 2: Load model and predict
            st.info("Running AI prediction...")
            predictor = FakeNewsPredictor()
            prediction_result = predictor.predict(article_text)
            
            if prediction_result.get('error'):
                st.error(f" Prediction error: {prediction_result['error']}")
                return
            
            # Display prediction result
            st.markdown("---")
            display_prediction_result(prediction_result, article_title)
            
            # Step 3: Get related information using article title
            search_query = article_title
            
            # If fake news, show fact-check links
            if prediction_result['label'] == 'Fake':
                st.markdown("---")
                with st.spinner("🔍 Finding fact-check resources..."):
                    fact_check_links = search_fact_check(search_query)
                    display_related_links(
                        fact_check_links,
                        "Fact-Check Resources",
                        "🛡️"
                    )
                
                with st.spinner("🔍 Finding verified news sources..."):
                    related_links = search_related_news(search_query)
                    display_related_links(
                        related_links,
                        "Verified News from Trusted Sources",
                        "📰"
                    )
            
            # If real news, show similar news from other sources
            else:
                st.markdown("---")
                with st.spinner("🔍 Finding similar news from other sources..."):
                    related_links = search_related_news(search_query)
                    display_related_links(
                        related_links,
                        "Similar News from Other Sources",
                        "📰"
                    )
            
            st.session_state.analyzed = True
    
    elif search_button and not url_input:
        st.warning("⚠️ Please enter a news article URL to analyze")
    
    # Add some spacing before footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Display information about the app
    with st.expander("ℹ️ About This Tool"):
        st.markdown("""
        ### How It Works
        
        1. **Enter URL**: Paste the link to a news article you want to verify
        2. **AI Analysis**: Our machine learning model analyzes the content
        3. **Get Results**: Receive a prediction with confidence score
        4. **Verify Further**: Access fact-checking resources and related news
        
        ### Technology
        
        - **Model**: TF-IDF + Logistic Regression
        - **Text Extraction**: Newspaper3k library
        - **News Sources**: Online Khabar, BBC News
        - **Fact-Check**: Snopes, FactCheck.org, PolitiFact, Reuters, AP
        
        ### Disclaimer
        
        This tool uses AI to assist in identifying potentially fake news. Always verify 
        important information through multiple trusted sources. No automated system is 
        100% accurate.
        """)
    
    # Display footer
    display_footer()

if __name__ == "__main__":
    main()
