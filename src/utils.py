"""
Utility functions for the fake news detection system
"""
import re
import string

def clean_text(text):
    """
    Clean and preprocess text data
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove special characters and digits
    text = re.sub(r'\d+', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def extract_keywords(text, max_keywords=5):
    """
    Extract important keywords from text for search queries
    
    Args:
        text (str): Text to extract keywords from
        max_keywords (int): Maximum number of keywords to return
        
    Returns:
        str: Space-separated keywords
    """
    if not text:
        return ""
    
    # Common stop words to remove
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'what', 'which', 'who', 'when', 'where', 'why', 'how'
    }
    
    # Convert to lowercase and split into words
    words = text.lower().split()
    
    # Filter out stop words, short words, and non-alphabetic words
    keywords = [
        word.strip(string.punctuation) 
        for word in words 
        if len(word) > 3 and word.lower() not in stop_words and word.isalpha()
    ]
    
    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for word in keywords:
        if word not in seen:
            seen.add(word)
            unique_keywords.append(word)
    
    # Return top keywords
    return ' '.join(unique_keywords[:max_keywords])

def validate_url(url):
    """
    Validate if a string is a proper URL
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if valid URL, False otherwise
    """
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None
