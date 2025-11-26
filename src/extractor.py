"""
Extract text content from news article URLs
"""
from newspaper import Article
import requests
from bs4 import BeautifulSoup

def extract_article_text(url, timeout=10):
    """
    Extract article text from a given URL using newspaper3k
    
    Args:
        url (str): URL of the news article
        timeout (int): Request timeout in seconds
        
    Returns:
        dict: Dictionary containing title, text, and authors
    """
    try:
        # Create Article object
        article = Article(url)
        
        # Download and parse the article
        article.download()
        article.parse()
        
        # Extract information
        result = {
            'title': article.title,
            'text': article.text,
            'authors': article.authors,
            'publish_date': article.publish_date,
            'success': True,
            'error': None
        }
        
        # Combine title and text for analysis
        full_text = f"{article.title}. {article.text}"
        result['full_text'] = full_text
        
        return result
        
    except Exception as e:
        return {
            'title': '',
            'text': '',
            'authors': [],
            'publish_date': None,
            'full_text': '',
            'success': False,
            'error': str(e)
        }

def extract_with_beautifulsoup(url, timeout=10):
    """
    Fallback method to extract text using BeautifulSoup
    
    Args:
        url (str): URL of the news article
        timeout (int): Request timeout in seconds
        
    Returns:
        str: Extracted text content
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(['script', 'style']):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
        
    except Exception as e:
        return f"Error: {str(e)}"
