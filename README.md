# Fake News Detection System

A machine learning-powered web application that analyzes news articles to detect fake news and provides fact-checking resources.

## Overview

This project uses Natural Language Processing (NLP) and Machine Learning to classify news articles as real or fake. The application extracts content from URLs, analyzes it using a trained model, and provides users with fact-checking resources and related news from trusted sources.

## Features

- **URL-based Analysis**: Simply paste a news article URL to analyze
- **AI-Powered Detection**: Uses TF-IDF vectorization and Logistic Regression
- **Fact-Check Resources**: Provides links to fact-checking websites for suspicious content
- **Related News**: Shows similar articles from trusted news sources
- **Clean UI**: Google-inspired interface with intuitive design
- **Confidence Scores**: Shows prediction confidence for transparency

## Project Structure

```
Fake News/
│
├── app.py                       # Streamlit web application
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── HOW_TO_RUN.md               # Detailed setup guide
│
├── model/
│   ├── fake-news-detection.ipynb   # Model training notebook
│   ├── model.pkl                   # Trained Logistic Regression model
│   ├── tfidf_vectorizer.pkl        # TF-IDF vectorizer
│   └── all_models.pkl              # All trained models (LR, DT, GBC, RFC)
│
├── src/
│   ├── extractor.py             # URL text extraction
│   ├── predictor.py             # Prediction logic
│   ├── fact_check.py            # Fact-checking search
│   ├── related_news.py          # Related news search
│   └── utils.py                 # Utility functions
│
└── data/
    └── raw/                     # Raw datasets (Fake.csv, True.csv)
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

4. **Download the dataset** (Required for training)
   
   The model requires both Fake.csv and True.csv to train:
   
   - Download from [Kaggle Fake and Real News Dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)
   - Extract `Fake.csv` and `True.csv`
   - Place both files in `data/raw/` folder
   
   **Note:** Pre-trained model files are already included. You only need to download the dataset if you want to retrain the models.

5. **Train the models** (Optional - skip if using pre-trained models)
   
   Open and run the Jupyter notebook:
   ```bash
   jupyter notebook model/fake-news-detection.ipynb
   ```
   
   Or open in VS Code and run all cells. This notebook trains 4 different models:
   - Logistic Regression (~79% accuracy) - used by the app
   - Decision Tree
   - Gradient Boosting Classifier
   - Random Forest Classifier

6. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   ```

7. **Open your browser** and go to `http://localhost:8501`

## 📊 Using the Application

1. **Enter URL**: Paste a news article URL in the search box
2. **Click Analyze**: Press the "Analyze News" button
3. **View Results**: 
   - See if the article is likely FAKE or REAL
   - View confidence score
   - Access fact-checking resources (if fake)
   - Find similar articles from trusted sources

## 🔧 Model Training

The system uses a Jupyter notebook (`model/fake-news-detection.ipynb`) to train multiple machine learning models:

1. **Logistic Regression** - Fast, interpretable, ~79% accuracy (used by the app)
2. **Decision Tree** - Simple tree-based model
3. **Gradient Boosting Classifier** - Ensemble method for better accuracy
4. **Random Forest Classifier** - Multiple decision trees ensemble

To retrain the models:
1. Ensure datasets are in `data/raw/` (Fake.csv and True.csv)
2. Open the notebook in Jupyter or VS Code
3. Run all cells sequentially
4. Models are automatically saved to `model/` directory

The notebook includes:
- Data loading and preprocessing
- Text cleaning with regex
- TF-IDF vectorization
- Training all 4 models
- Classification reports for each model
- Model persistence with pickle

## 🧠 Technical Details

### Using Pre-trained Model (Recommended)

The repository includes pre-trained model files (`model.pkl` and `tfidf.pkl`) with ~72% accuracy. You can use these directly without training.

### Retraining the Model

If you want to retrain or update the model:

1. **Download the dataset** (Required):
   - Go to [Kaggle Fake and Real News Dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)
   - Download and extract `Fake.csv` and `True.csv`
   - Place both files in `data/raw/` folder

2. **Run training script**:
   ```bash
   python model/train_model.py
   ```

3. **Commit new model files** (if deploying):
   ```bash
   git add model/*.pkl
   git commit -m "Update trained model"
   git push origin main
   ```

**Note:** The CSV files are ~100MB total and are not included in the repository to keep it lightweight.



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
