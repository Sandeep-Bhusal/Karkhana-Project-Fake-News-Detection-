# Deployment Guide

## For Streamlit Cloud Deployment

1. **Push your code to GitHub** ✅ (Already done!)

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository: `RoshanKapali/Karkhana-Project-Fake-News-Detection-`
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Important Notes:**
   - Streamlit Cloud will automatically install dependencies from `requirements.txt`
   - The app uses pre-trained models (`model.pkl` and `tfidf_vectorizer.pkl`) which are already in the repo
   - First deployment may take 5-10 minutes

## For Running on Friend's Laptop

### Prerequisites
- Python 3.8 or higher
- Git installed

### Setup Steps

1. **Clone the repository:**
```bash
git clone https://github.com/RoshanKapali/Karkhana-Project-Fake-News-Detection-.git
cd Karkhana-Project-Fake-News-Detection-
```

2. **Create virtual environment:**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the app:**
```bash
streamlit run app.py
```

5. **Access the app:**
   - Open browser at `http://localhost:8501`

### Troubleshooting

**If you get scikit-learn version warnings:**
- These are safe to ignore as long as predictions work
- Models were trained with scikit-learn 1.3.0

**If newspaper3k fails to extract content:**
- This is normal for some websites with strict security
- Try using the text input mode instead

**If NLTK data is missing:**
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## Project Structure

```
Fake-News-Detection/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── HOW_TO_RUN.md                  # Quick start guide
├── DEPLOYMENT.md                  # This file
├── model/
│   ├── fake-news-detection.ipynb  # Training notebook
│   ├── model.pkl                  # Logistic Regression model
│   └── tfidf_vectorizer.pkl       # Text vectorizer
└── src/
    ├── predictor.py               # Prediction logic
    ├── extractor.py               # Article extraction
    ├── fact_check.py              # Fact-checking links
    ├── related_news.py            # Related news fetcher
    └── utils.py                   # Utility functions
```

## System Requirements

- **RAM:** 2GB minimum
- **Storage:** 500MB free space
- **Internet:** Required for URL extraction and related news
- **OS:** Windows, Mac, or Linux

## Model Information

- **Algorithm:** Logistic Regression
- **Accuracy:** ~79%
- **Training Data:** 44,898 articles (Kaggle Fake and Real News Dataset)
- **Features:** TF-IDF vectorization with 5000 features
