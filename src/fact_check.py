"""
Search for fact-check articles using Bing Search API
"""
import requests
import os

def search_fact_check(query, api_key=None, num_results=5):
    """
    Search for fact-checking articles related to the news topic
    
    Args:
        query (str): Search query (news headline or main topic)
        api_key (str): Bing Search API key (optional, can use env variable)
        num_results (int): Number of results to return
        
    Returns:
        list: List of dictionaries containing fact-check articles
    """
    # Use provided API key or get from environment
    if not api_key:
        api_key = os.environ.get('BING_API_KEY', '')
    
    # If no API key available, return mock results
    if not api_key:
        return get_mock_fact_check_results(query)
    
    try:
        # Bing Search API endpoint
        endpoint = "https://api.bing.microsoft.com/v7.0/search"
        
        # Add fact-check specific terms to query
        search_query = f"{query} fact check snopes politifact"
        
        # Set up headers
        headers = {
            'Ocp-Apim-Subscription-Key': api_key
        }
        
        # Set up parameters
        params = {
            'q': search_query,
            'count': num_results,
            'mkt': 'en-US',
            'safeSearch': 'Moderate'
        }
        
        # Make request
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        
        # Parse results
        data = response.json()
        results = []
        
        if 'webPages' in data and 'value' in data['webPages']:
            for item in data['webPages']['value']:
                results.append({
                    'title': item.get('name', ''),
                    'url': item.get('url', ''),
                    'snippet': item.get('snippet', ''),
                    'source': 'Bing Search'
                })
        
        return results
        
    except Exception as e:
        print(f"Error in fact-check search: {str(e)}")
        return get_mock_fact_check_results(query)

def get_mock_fact_check_results(query):
    """
    Return mock fact-check results when API is not available
    
    Args:
        query (str): Search query
        
    Returns:
        list: List of mock fact-check resources
    """
    # Common fact-checking websites
    fact_check_sites = [
        {
            'title': f'Snopes Fact Check',
            'url': f'https://www.snopes.com/?s={query.replace(" ", "+")}',
            'snippet': 'Check this topic on Snopes - The definitive Internet reference source for fact-checking',
            'source': 'Snopes'
        },
        {
            'title': f'FactCheck.org',
            'url': f'https://www.factcheck.org/?s={query.replace(" ", "+")}',
            'snippet': 'Verify claims and statements on FactCheck.org - A nonpartisan fact-checking website',
            'source': 'FactCheck.org'
        },
        {
            'title': f'PolitiFact',
            'url': f'https://www.politifact.com/search/?q={query.replace(" ", "+")}',
            'snippet': 'Check facts and claims on PolitiFact - Pulitzer Prize-winning fact-checking',
            'source': 'PolitiFact'
        },
        {
            'title': f'Reuters Fact Check',
            'url': f'https://www.reuters.com/fact-check',
            'snippet': 'Reuters fact-checking team verifies claims and debunks misinformation',
            'source': 'Reuters'
        },
        {
            'title': f'AP Fact Check',
            'url': f'https://apnews.com/ap-fact-check',
            'snippet': 'Associated Press fact-checking service for accurate news verification',
            'source': 'AP News'
        }
    ]
    
    return fact_check_sites[:5]
