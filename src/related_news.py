"""
Search for related news articles from reliable sources
"""
import requests
import os

def search_related_news(query, api_key=None, num_results=5):
    """
    Search for related news articles from reliable sources
    
    Args:
        query (str): Search query (news headline or main topic)
        api_key (str): Bing News Search API key (optional, can use env variable)
        num_results (int): Number of results to return
        
    Returns:
        list: List of dictionaries containing related news articles
    """
    # Use provided API key or get from environment
    if not api_key:
        api_key = os.environ.get('BING_API_KEY', '')
    
    # If no API key available, return mock results
    if not api_key:
        return get_mock_news_results(query)
    
    try:
        # Bing News Search API endpoint
        endpoint = "https://api.bing.microsoft.com/v7.0/news/search"
        
        # Set up headers
        headers = {
            'Ocp-Apim-Subscription-Key': api_key
        }
        
        # Set up parameters
        params = {
            'q': query,
            'count': num_results,
            'mkt': 'en-US',
            'safeSearch': 'Moderate',
            'freshness': 'Month'  # Get recent news
        }
        
        # Make request
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        
        # Parse results
        data = response.json()
        results = []
        
        if 'value' in data:
            for item in data['value']:
                results.append({
                    'title': item.get('name', ''),
                    'url': item.get('url', ''),
                    'snippet': item.get('description', ''),
                    'source': item.get('provider', [{}])[0].get('name', 'Unknown'),
                    'date': item.get('datePublished', '')
                })
        
        return results
        
    except Exception as e:
        print(f"Error in news search: {str(e)}")
        return get_mock_news_results(query)

def get_mock_news_results(query, num_results=5):
    """
    Return mock news results when API is not available
    
    Args:
        query (str): Search query
        num_results (int): Number of results to return
        
    Returns:
        list: List of mock news sources
    """
    # Common reliable news sources
    news_sources = [
        {
            'title': f'Search on BBC News',
            'url': f'https://www.bbc.com/search?q={query.replace(" ", "+")}',
            'snippet': 'Find related news articles on BBC News - Trusted international news source',
            'source': 'BBC News',
            'date': ''
        },
        {
            'title': f'Search on Reuters',
            'url': f'https://www.reuters.com/search/news?blob={query.replace(" ", "+")}',
            'snippet': 'Find related news on Reuters - Breaking international news and world coverage',
            'source': 'Reuters',
            'date': ''
        },
        {
            'title': f'Search on Associated Press',
            'url': f'https://apnews.com/search?q={query.replace(" ", "+")}',
            'snippet': 'Find related news on AP News - Independent global news organization',
            'source': 'AP News',
            'date': ''
        },
        {
            'title': f'Search on CNN',
            'url': f'https://www.cnn.com/search?q={query.replace(" ", "+")}',
            'snippet': 'Find related news on CNN - Breaking news and latest updates',
            'source': 'CNN',
            'date': ''
        },
        {
            'title': f'Search on The Guardian',
            'url': f'https://www.theguardian.com/search?q={query.replace(" ", "+")}',
            'snippet': 'Find related news on The Guardian - Latest news and analysis',
            'source': 'The Guardian',
            'date': ''
        }
    ]
    
    return news_sources[:num_results]
