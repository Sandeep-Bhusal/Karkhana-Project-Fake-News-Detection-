"""
Search for fact-check articles from trusted sources
"""

def search_fact_check(query, num_results=5):
    """
    Return fact-check resources from trusted sources
    
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
