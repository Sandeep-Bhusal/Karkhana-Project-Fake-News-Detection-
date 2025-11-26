"""
Search for related news articles from reliable sources
"""

def search_related_news(query, num_results=2):
    """
    Return related news from trusted sources
    
    Args:
        query (str): Search query
        num_results (int): Number of results to return
        
    Returns:
        list: List of mock news sources
    """
    # Reliable news sources - Nepali and International
    news_sources = [
        {
            'title': f'Search on Online Khabar',
            'url': f'https://www.onlinekhabar.com/?s={query.replace(" ", "+")}',
            'snippet': 'Find related news on Online Khabar - Leading Nepali news portal with comprehensive coverage',
            'source': 'Online Khabar',
            'date': ''
        },
        {
            'title': f'Search on CNN News',
            'url': f'https://www.cnn.com/search?q={query.replace(" ", "+")}',
            'snippet': 'Find related news on CNN News - Trusted international news source with global coverage',
            'source': 'CNN News',
            'date': ''
        }
    ]
    
    return news_sources[:num_results]
