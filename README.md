# 🔍 Fake News Detection System

A machine learning-powered web application that analyzes news articles to detect fake news and provides fact-checking resources.

## 📋 Overview

This project uses Natural Language Processing (NLP) and Machine Learning to classify news articles as real or fake. The application extracts content from URLs, analyzes it using a trained model, and provides users with fact-checking resources and related news from trusted sources.

## ✨ Features

- **URL-based Analysis**: Simply paste a news article URL to analyze
- **AI-Powered Detection**: Uses TF-IDF vectorization and Logistic Regression
- **Fact-Check Resources**: Provides links to fact-checking websites for suspicious content
- **Related News**: Shows similar articles from trusted news sources
- **Clean UI**: Google-inspired interface with intuitive design
- **Confidence Scores**: Shows prediction confidence for transparency

## 🏗️ Project Structure

```
Fake News/
│
├── app.py                       # Streamlit web application
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── model/
│   ├── train_model.py           # Model training script
│   ├── model.pkl                # Trained model (generated)
│   └── tfidf.pkl                # TF-IDF vectorizer (generated)
│
├── src/
│   ├── extractor.py             # URL text extraction
│   ├── predictor.py             # Prediction logic
│   ├── fact_check.py            # Fact-checking search
│   ├── related_news.py          # Related news search
│   └── utils.py                 # Utility functions
│
└── data/
    ├── raw/                     # Raw datasets (optional)
    └── processed/               # Processed data (optional)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download this repository**

2. **Navigate to the project directory**
   ```bash
   cd "Fake News"
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the model**
   ```bash
   python model/train_model.py
   ```
   
   This creates `model.pkl` and `tfidf.pkl` files needed for predictions.

5. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser** and go to `http://localhost:8501`

## 📊 Using the Application

1. **Enter URL**: Paste a news article URL in the search box
2. **Click Analyze**: Press the "Analyze News" button
3. **View Results**: 
   - See if the article is likely FAKE or REAL
   - View confidence score
   - Access fact-checking resources (if fake)
   - Find similar articles from trusted sources

## 🔧 Model Training

### Default Training

The system includes sample data for quick setup. Run:

```bash
python model/train_model.py
```

### Training with Real Dataset

For better accuracy, download the Kaggle Fake and Real News Dataset:

1. Download from [Kaggle](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)
2. Extract `Fake.csv` and `True.csv` to `data/raw/` folder
3. Run training script again:
   ```bash
   python model/train_model.py
   ```

The model will automatically detect and use the Kaggle dataset.

## 🔑 Optional: Bing Search API

For enhanced fact-checking and news search:

1. Get a free Bing Search API key from [Microsoft Azure](https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/)
2. Set environment variable:
   
   **Windows:**
   ```bash
   set BING_API_KEY=your_api_key_here
   ```
   
   **Linux/Mac:**
   ```bash
   export BING_API_KEY=your_api_key_here
   ```

Without the API key, the app uses fallback links to popular fact-checking websites.

## 🌐 Deployment on Streamlit Cloud

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin your-github-repo-url
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Optional: Add API Key**
   - In Streamlit Cloud dashboard, go to app settings
   - Add secret: `BING_API_KEY = your_key`

## 🧪 How It Works

### Text Extraction
- Uses `newspaper3k` library to extract article content from URLs
- Falls back to BeautifulSoup if needed
- Cleans and preprocesses text

### Classification Model
- **Vectorization**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Algorithm**: Logistic Regression
- **Features**: 5000 most important words, unigrams and bigrams
- **Training**: 80-20 train-test split

### Search Integration
- Fact-checking: Links to Snopes, FactCheck.org, PolitiFact, Reuters, AP
- Related news: Searches trusted sources like BBC, Reuters, CNN, AP, The Guardian
- Optional Bing API integration for live search results

## 📈 Model Performance

With sample data (demonstration):
- Accuracy: ~90-95%
- Limited training samples for quick setup

With Kaggle dataset (recommended):
- Accuracy: ~95-98%
- 40,000+ training samples
- Better generalization

## ⚠️ Limitations

- Model accuracy depends on training data quality
- Cannot detect all forms of misinformation
- Works best with English news articles
- Requires internet connection for URL extraction
- Should be used as an assistive tool, not sole source of truth

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **ML Model**: Scikit-learn (Logistic Regression)
- **Text Processing**: TF-IDF, NLTK
- **Web Scraping**: Newspaper3k, BeautifulSoup
- **API Integration**: Bing Search API (optional)

## 📝 Contributing

Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📄 License

This project is for educational purposes. Use responsibly.

## 👤 Author

Created as part of a text classification project.

## 🙏 Acknowledgments

- Kaggle for the Fake and Real News Dataset
- Streamlit for the amazing framework
- Scikit-learn for ML tools
- All contributors to open-source libraries used

## 📞 Support

If you encounter issues:
1. Check that all dependencies are installed
2. Ensure model is trained (model.pkl and tfidf.pkl exist)
3. Verify URL format (must start with http:// or https://)
4. Check your internet connection

---

**Remember**: Always verify important information through multiple trusted sources. This tool is meant to assist, not replace, critical thinking and fact-checking.
