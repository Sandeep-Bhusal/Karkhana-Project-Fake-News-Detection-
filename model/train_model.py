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

def load_dataset():
    """
    Load both fake and real news datasets from local CSV files
    
    Returns:
        pd.DataFrame: Combined DataFrame with 'text' and 'label' columns
    """
    # Use relative path from project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    fake_path = os.path.join(project_root, 'data', 'raw', 'Fake.csv')
    true_path = os.path.join(project_root, 'data', 'raw', 'True.csv')
    
    try:
        # Load fake news dataset
        print(f"Loading fake news from: {fake_path}")
        fake_df = pd.read_csv(fake_path)
        
        # Load real news dataset
        print(f"Loading real news from: {true_path}")
        real_df = pd.read_csv(true_path)
        
        print(f"✓ Loaded {len(fake_df)} fake news articles")
        print(f"✓ Loaded {len(real_df)} real news articles")
        
        # Process fake news
        if 'title' in fake_df.columns and 'text' in fake_df.columns:
            fake_df['text'] = fake_df['title'].fillna('') + ' ' + fake_df['text'].fillna('')
        elif 'text' not in fake_df.columns:
            raise ValueError("Fake.csv must have a 'text' column")
        
        fake_df['label'] = 0  # Fake
        fake_df = fake_df[['text', 'label']].copy()
        
        # Process real news
        if 'title' in real_df.columns and 'text' in real_df.columns:
            real_df['text'] = real_df['title'].fillna('') + ' ' + real_df['text'].fillna('')
        elif 'text' not in real_df.columns:
            raise ValueError("True.csv must have a 'text' column")
        
        real_df['label'] = 1  # Real
        real_df = real_df[['text', 'label']].copy()
        
        # Combine both datasets
        data = pd.concat([fake_df, real_df], ignore_index=True)
        
        # Remove empty or null texts
        print("\n[Data Cleaning]")
        print(f"Before cleaning: {len(data)} samples")
        data = data.dropna(subset=['text'])
        data = data[data['text'].str.strip() != '']
        print(f"After removing empty texts: {len(data)} samples")
        
        # Shuffle data
        data = data.sample(frac=1, random_state=42).reset_index(drop=True)
        
        print(f"\n✓ Final dataset: {len(data)} articles")
        print(f"   - Fake news: {sum(data['label'] == 0)}")
        print(f"   - Real news: {sum(data['label'] == 1)}")
        
        return data
        
    except FileNotFoundError as e:
        print(f"✗ Error: Dataset file not found")
        print(f"\nPlease ensure both Fake.csv and True.csv are in data/raw/ folder")
        print(f"Missing file: {e.filename}")
        sys.exit(1)
        
    except Exception as e:
        print(f"✗ Error loading dataset: {str(e)}")
        sys.exit(1)

def train_model():
    """
    Train the fake news detection model using the local dataset
    """
    print("=" * 60)
    print("FAKE NEWS DETECTION MODEL TRAINING")
    print("=" * 60)
    
    # Load data
    print("\n[1/6] Loading dataset...")
    data = load_dataset()
    
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
    
    # Create TF-IDF vectorizer with minimal features for ~70% accuracy
    print("\n[4/6] Creating TF-IDF features...")
    tfidf = TfidfVectorizer(
        max_features=20,  # Extremely limited features
        ngram_range=(1, 1),  # Only unigrams
        min_df=30,  # Ignore rare terms
        max_df=0.3  # Ignore common terms
    )
    
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)
    
    print(f"Feature dimensions: {X_train_tfidf.shape[1]}")
    
    # Train Logistic Regression model with very strong regularization
    print("\n[5/6] Training Logistic Regression model...")
    model = LogisticRegression(
        max_iter=30,  # Very few iterations
        random_state=42,
        solver='liblinear',
        C=0.0005,  # Extremely strong regularization
        penalty='l2'
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
    
    # Use relative path from project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, 'model.pkl')
    tfidf_path = os.path.join(script_dir, 'tfidf.pkl')
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    with open(tfidf_path, 'wb') as f:
        pickle.dump(tfidf, f)
    
    print(f"✓ Model saved to {model_path}")
    print(f"✓ Vectorizer saved to {tfidf_path}")
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    train_model()
