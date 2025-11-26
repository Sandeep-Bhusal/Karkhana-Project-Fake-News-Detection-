"""
Test script to verify the fake news detection system
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.predictor import FakeNewsPredictor
from src.utils import clean_text

def test_predictor():
    """Test the prediction functionality"""
    
    print("=" * 60)
    print("TESTING FAKE NEWS PREDICTOR")
    print("=" * 60)
    
    # Initialize predictor
    print("\n[1/3] Loading model...")
    predictor = FakeNewsPredictor()
    
    if not predictor.model or not predictor.tfidf:
        print("✗ Model not loaded. Please train the model first.")
        print("Run: python model/train_model.py")
        return
    
    print("✓ Model loaded successfully")
    
    # Test samples
    test_samples = [
        {
            'text': "Scientists discover cure for all diseases using magic crystals found in ancient ruins",
            'expected': 'Fake'
        },
        {
            'text': "Stock markets showed mixed results today as investors weighed economic data and corporate earnings",
            'expected': 'Real'
        },
        {
            'text': "Breaking: Government confirms secret alien base on moon, officials reveal shocking details",
            'expected': 'Fake'
        },
        {
            'text': "Technology company announces quarterly earnings, reporting revenue growth and expansion plans",
            'expected': 'Real'
        }
    ]
    
    print("\n[2/3] Running predictions...")
    print()
    
    correct = 0
    total = len(test_samples)
    
    for i, sample in enumerate(test_samples, 1):
        print(f"Test {i}/{total}:")
        print(f"Text: {sample['text'][:80]}...")
        print(f"Expected: {sample['expected']}")
        
        result = predictor.predict(sample['text'])
        
        if result.get('error'):
            print(f"✗ Error: {result['error']}")
        else:
            print(f"Predicted: {result['label']}")
            print(f"Confidence: {result['confidence']:.2f}%")
            
            if result['label'] == sample['expected']:
                print("✓ CORRECT")
                correct += 1
            else:
                print("✗ INCORRECT")
        
        print("-" * 60)
        print()
    
    # Summary
    print("[3/3] Test Summary:")
    accuracy = (correct / total) * 100
    print(f"Correct predictions: {correct}/{total}")
    print(f"Accuracy: {accuracy:.1f}%")
    
    if accuracy >= 75:
        print("✓ Model is performing well!")
    elif accuracy >= 50:
        print("⚠ Model needs improvement. Consider training with more data.")
    else:
        print("✗ Model performance is poor. Please retrain with proper dataset.")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    test_predictor()
