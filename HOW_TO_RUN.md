# How to Run the Fake News Detection System

## Prerequisites

Before running the code, make sure you have:
- **Python 3.8 or higher** installed on your system
- **pip** (Python package manager)
- **Internet connection** (for downloading packages and analyzing URLs)

---

## Step 1: Install Dependencies

Open PowerShell or Command Prompt and navigate to the project folder:

```bash
cd "c:\Users\Roshan\OneDrive\Desktop\Fake News"
```

Install all required packages:

```bash
pip install -r requirements.txt
```

This will install:
- streamlit (web framework)
- pandas, numpy (data processing)
- scikit-learn (machine learning)
- newspaper3k, beautifulsoup4, lxml (web scraping)
- requests (HTTP requests)
- nltk (text processing)

## Step 2: Train the Model (Using Jupyter Notebook)

The models are trained using the Jupyter notebook. Open and run the notebook:

**Option 1: Using VS Code**
1. Open `model/fake-news-detection.ipynb` in VS Code
2. Select Python kernel (the .venv environment)
3. Click "Run All" or run cells sequentially
4. Wait for all cells to complete (takes 5-10 minutes)

**Option 2: Using Jupyter Notebook**
```bash
jupyter notebook
```
Then navigate to `model/fake-news-detection.ipynb` and run all cells.

**What the notebook does:**
- Loads and processes the dataset (Fake.csv and True.csv)
- Trains 4 different ML models:
  - Logistic Regression
  - Decision Tree
  - Gradient Boosting Classifier
  - Random Forest Classifier
- Evaluates each model with classification reports
- Saves the trained models:
  - `model.pkl` - Logistic Regression (used by Streamlit app)
  - `tfidf_vectorizer.pkl` - TF-IDF vectorizer
  - `all_models.pkl` - All 4 models for comparison

**Expected output at the end:**
```
✓ Logistic Regression model saved
✓ TF-IDF vectorizer saved
✓ All models saved

============================================================
MODEL TRAINING COMPLETED!
============================================================
```

**Note:** Pre-trained models are already included. You only need to retrain if you want to update the models with new data.

---

## Step 3: Run the Streamlit App

Start the web application:

```bash
streamlit run app.py
```

**What happens:**
- Streamlit starts a local web server
- Opens your default browser automatically
- If not, manually go to the URL shown in terminal

**Expected Output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

**Time:** ~5 seconds to start

---

## Step 4: Use the Application

### In your web browser:

1. **Enter a news article URL** in the search box
   - Example: `https://www.bbc.com/news/article-example`

2. **Click "🔍 Analyze News"** button

3. **View Results:**
   - Prediction: Fake or Real
   - Confidence score
   - Fact-check resources (if fake)
   - Similar news from other sources (if real)

---

## Alternative: Quick Setup (Windows)

Use the automated setup script:

```bash
.\setup.ps1
```

This will:
- Check Python installation
- Install dependencies
- Train the model
- Show next steps

---

## Testing the System

To verify everything works correctly:

```bash
python test_system.py
```

**What it does:**
- Tests the model with 4 sample articles
- Shows predictions and accuracy
- Confirms model is working properly

**Expected Output:**
```
============================================================
TESTING FAKE NEWS PREDICTOR
============================================================

Test 1/4:
Text: Scientists discover cure for all diseases...
Expected: Fake
Predicted: Fake
Confidence: XX.XX%
✓ CORRECT

[... more tests ...]

Accuracy: 100.0%
✓ Model is performing well!
============================================================
```

---

## Stopping the App

To stop the Streamlit app:
- Press **Ctrl + C** in the terminal/PowerShell window
- Or close the terminal window

---

## Troubleshooting

### Problem: "Python not found"
**Solution:** Install Python from https://www.python.org/downloads/

### Problem: "pip not found"
**Solution:** Reinstall Python and check "Add to PATH" during installation

### Problem: "Model not found"
**Solution:** Run `python model/train_model.py` first

### Problem: "Import errors"
**Solution:** Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

### Problem: "Port 8501 already in use"
**Solution:** 
- Kill existing process: `taskkill /F /IM streamlit.exe`
- Or use different port: `streamlit run app.py --server.port 8502`

### Problem: "Article extraction failed"
**Solution:** 
- Check your internet connection
- Try a different news URL
- Make sure URL starts with `http://` or `https://`

---

## Improving Model Accuracy

For better accuracy, use the Kaggle dataset:

1. **Download dataset:**
   - Go to: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset
   - Download `Fake.csv` and `True.csv`

2. **Place files:**
   - Put both CSV files in `data/raw/` folder

3. **Retrain model:**
   ```bash
   python model/train_model.py
   ```

This will train with 40,000+ articles and achieve 95-98% accuracy!

---

## Common Commands Summary

```bash
# Install dependencies
pip install -r requirements.txt

# Train model
python model/train_model.py

# Run app
streamlit run app.py

# Test system
python test_system.py

# Quick setup (Windows)
.\setup.ps1
```

---

## File Structure Reference

```
Fake News/
├── app.py              ← Run this for web app
├── requirements.txt    ← Dependencies list
├── model/
│   ├── train_model.py  ← Run this to train
│   ├── model.pkl       ← Generated after training
│   └── tfidf.pkl       ← Generated after training
├── src/
│   ├── extractor.py    ← Extracts text from URLs
│   ├── predictor.py    ← Makes predictions
│   ├── fact_check.py   ← Searches fact-check sites
│   ├── related_news.py ← Searches related news
│   └── utils.py        ← Helper functions
└── data/
    ├── raw/            ← Put Kaggle datasets here
    └── processed/
```

---

## Next Steps

After running locally:

1. **Test with different news URLs** to see how it performs
2. **Download Kaggle dataset** for better accuracy
3. **Deploy to Streamlit Cloud** for public access
4. **Share your app** with others!

---

## Need Help?

Check the **README.md** file for more detailed information about the project, features, and deployment options.

---

**You're all set! Enjoy detecting fake news!**
