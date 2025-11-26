"""
Train a fake news detection model using TF-IDF and Logistic Regression
"""
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import clean_text

def load_sample_data():
    """
    Create sample training data for demonstration
    In production, replace this with actual dataset loading
    
    Returns:
        pd.DataFrame: DataFrame with 'text' and 'label' columns
    """
    # Sample fake news examples
    fake_news = [
        "BREAKING: Scientists discover cure for all diseases using magic crystals!",
        "Government officials secretly meeting with aliens, insider reveals shocking truth",
        "This one weird trick will make you a millionaire overnight, banks hate it",
        "Celebrity found to be robot, sources confirm shocking revelation",
        "New study shows drinking gasoline improves health, doctors amazed",
        "Government planning to ban all internet usage next week, prepare now",
        "Miracle fruit cures cancer in 24 hours, pharmaceutical companies hiding truth",
        "President admits to being time traveler from the future",
        "Scientists confirm Earth is actually flat, textbooks were wrong",
        "Drinking 10 liters of water daily makes you immortal, new research shows"
    ]
    
    # Sample real news examples
    real_news = [
        "Stock markets showed mixed results today as investors weighed economic data",
        "Local government announces new infrastructure development plan for the city",
        "Research team publishes findings on climate change effects in peer-reviewed journal",
        "Technology company reports quarterly earnings, beats analyst expectations",
        "Supreme Court hears arguments in landmark civil rights case",
        "International summit brings together world leaders to discuss trade policies",
        "Scientists discover new species of marine life in deep ocean exploration",
        "Education department announces changes to curriculum standards for next year",
        "Healthcare workers receive additional training in new medical procedures",
        "Sports team advances to championship after winning playoff series"
    ]
    
    # Create DataFrame
    data = pd.DataFrame({
        'text': fake_news + real_news,
        'label': [0] * len(fake_news) + [1] * len(real_news)  # 0 = Fake, 1 = Real
    })
    
    return data

def load_kaggle_dataset(fake_path='data/raw/Fake.csv', real_path='data/raw/True.csv'):
    """
    Load fake news dataset from Kaggle (if available)
    Download from: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset
    
    Args:
        fake_path (str): Path to fake news CSV file
        real_path (str): Path to real news CSV file
        
    Returns:
        pd.DataFrame: Combined DataFrame with 'text' and 'label' columns
    """
    try:
        # Load datasets
        fake_df = pd.read_csv(fake_path)
        real_df = pd.read_csv(real_path)
        
        # Add labels
        fake_df['label'] = 0  # Fake
        real_df['label'] = 1  # Real
        
        # Combine title and text
        fake_df['text'] = fake_df['title'] + ' ' + fake_df['text']
        real_df['text'] = real_df['title'] + ' ' + real_df['text']
        
        # Select relevant columns
        fake_df = fake_df[['text', 'label']]
        real_df = real_df[['text', 'label']]
        
        # Combine datasets
        data = pd.concat([fake_df, real_df], ignore_index=True)
        
        # Shuffle data
        data = data.sample(frac=1, random_state=42).reset_index(drop=True)
        
        print(f"✓ Loaded {len(data)} articles from Kaggle dataset")
        return data
        
    except Exception as e:
        print(f"⚠ Could not load Kaggle dataset: {str(e)}")
        print("Using sample data instead...")
        return load_sample_data()

def train_model(use_kaggle=False):
    """
    Train the fake news detection model
    
    Args:
        use_kaggle (bool): Whether to use Kaggle dataset or sample data
    """
    print("=" * 60)
    print("FAKE NEWS DETECTION MODEL TRAINING")
    print("=" * 60)
    
    # Load data
    print("\n[1/6] Loading dataset...")
    if use_kaggle:
        data = load_kaggle_dataset()
    else:
        data = load_sample_data()
    
    print(f"Total samples: {len(data)}")
    print(f"Fake news: {sum(data['label'] == 0)}")
    print(f"Real news: {sum(data['label'] == 1)}")
    
    # Clean text
    print("\n[2/6] Cleaning text data...")
    data['cleaned_text'] = data['text'].apply(clean_text)
    
    # Remove empty texts
    data = data[data['cleaned_text'].str.len() > 0]
    
    # Split data
    print("\n[3/6] Splitting data into train and test sets...")
    X = data['cleaned_text']
    y = data['label']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    
    # Create TF-IDF vectorizer
    print("\n[4/6] Creating TF-IDF features...")
    tfidf = TfidfVectorizer(
        max_features=5000,  # Limit features for efficiency
        ngram_range=(1, 2),  # Use unigrams and bigrams
        min_df=2,  # Ignore terms that appear in less than 2 documents
        max_df=0.8  # Ignore terms that appear in more than 80% of documents
    )
    
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)
    
    print(f"Feature dimensions: {X_train_tfidf.shape[1]}")
    
    # Train Logistic Regression model
    print("\n[5/6] Training Logistic Regression model...")
    model = LogisticRegression(
        max_iter=1000,
        random_state=42,
        solver='liblinear'
    )
    
    model.fit(X_train_tfidf, y_train)
    print("✓ Model training completed")
    
    # Evaluate model
    print("\n[6/6] Evaluating model performance...")
    y_pred = model.predict(X_test_tfidf)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy * 100:.2f}%")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Fake', 'Real']))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Save model and vectorizer
    print("\n[SAVING] Saving model and vectorizer...")
    
    os.makedirs('model', exist_ok=True)
    
    with open('model/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('model/tfidf.pkl', 'wb') as f:
        pickle.dump(tfidf, f)
    
    print("✓ Model saved to model/model.pkl")
    print("✓ Vectorizer saved to model/tfidf.pkl")
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    # Check if Kaggle dataset exists
    kaggle_exists = os.path.exists('data/raw/Fake.csv') and os.path.exists('data/raw/True.csv')
    
    if kaggle_exists:
        print("Kaggle dataset found! Training with full dataset...")
        train_model(use_kaggle=True)
    else:
        print("Kaggle dataset not found. Training with sample data...")
        print("\nTo use the full dataset:")
        print("1. Download from: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset")
        print("2. Place Fake.csv and True.csv in data/raw/ folder")
        print("3. Run this script again\n")
        train_model(use_kaggle=False)
