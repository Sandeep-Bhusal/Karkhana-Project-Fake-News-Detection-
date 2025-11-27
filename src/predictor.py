"""
Load trained model and make predictions
"""
import pickle
import os
from src.utils import clean_text

class FakeNewsPredictor:
    """
    Predictor class for fake news detection
    """
    
    def __init__(self, model_path='model/model.pkl', tfidf_path='model/tfidf_vectorizer.pkl'):
        """
        Initialize the predictor with saved model and vectorizer
        
        Args:
            model_path (str): Path to saved model file
            tfidf_path (str): Path to saved TF-IDF vectorizer file
        """
        self.model = None
        self.tfidf = None
        self.model_path = model_path
        self.tfidf_path = tfidf_path
        
        # Load model and vectorizer
        self.load_model()
    
    def load_model(self):
        """
        Load the trained model and TF-IDF vectorizer from disk
        """
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.tfidf_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                
                with open(self.tfidf_path, 'rb') as f:
                    self.tfidf = pickle.load(f)
                
                print("✓ Model and vectorizer loaded successfully")
            else:
                print("⚠ Model files not found. Please train the model first.")
        except Exception as e:
            print(f"✗ Error loading model: {str(e)}")
    
    def predict(self, text):
        """
        Predict whether the given text is fake or real news
        
        Args:
            text (str): Article text to classify
            
        Returns:
            dict: Dictionary containing prediction and confidence score
        """
        if not self.model or not self.tfidf:
            return {
                'prediction': 'Error',
                'label': 'Model not loaded',
                'confidence': 0.0,
                'error': 'Model or vectorizer not loaded properly'
            }
        
        try:
            # Clean the text
            cleaned_text = clean_text(text)
            
            if not cleaned_text:
                return {
                    'prediction': 'Error',
                    'label': 'Invalid input',
                    'confidence': 0.0,
                    'error': 'Text is empty after cleaning'
                }
            
            # Transform text using TF-IDF
            text_vector = self.tfidf.transform([cleaned_text])
            
            # Get probability scores
            proba = self.model.predict_proba(text_vector)[0]
            fake_prob = proba[0]  # Probability of being fake (class 0)
            real_prob = proba[1]  # Probability of being real (class 1)
            
            # Adjust threshold based on text length - be very conservative
            text_length = len(cleaned_text.split())
            
            if text_length < 30:
                # For short text, require very high confidence for "Fake"
                threshold = 0.85
            elif text_length < 150:
                # For medium text, still very conservative
                threshold = 0.75
            else:
                # For longer articles, still conservative
                threshold = 0.65
            
            if real_prob > threshold:
                prediction = 1
                label = 'Real'
                confidence = real_prob * 100
            elif fake_prob > threshold:
                prediction = 0
                label = 'Fake'
                confidence = fake_prob * 100
            else:
                # Uncertain case - default to Real to avoid false alarms
                prediction = 1
                label = 'Real'
                confidence = max(real_prob, 51.0) * 100
            
            return {
                'prediction': prediction,
                'label': label,
                'confidence': round(confidence, 2),
                'probabilities': {
                    'fake': round(fake_prob * 100, 2),
                    'real': round(real_prob * 100, 2)
                },
                'error': None
            }
            
        except Exception as e:
            return {
                'prediction': 'Error',
                'label': 'Prediction failed',
                'confidence': 0.0,
                'error': str(e)
            }
