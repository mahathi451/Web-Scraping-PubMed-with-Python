import re
from urllib.parse import quote_plus

def validate_query(query: str) -> None:
    """Validate PubMed search query format"""
    if not query:
        raise ValueError("Empty search query")
    
    if len(query) > 300:
        raise ValueError("Query exceeds 300 character limit")
    
    if re.search(r"[^\w\s\-()\"']", query):
        raise ValueError("Invalid special characters in query")

def format_search_url(query: str, page: int) -> str:
    """Build properly encoded search URL"""
    encoded_query = quote_plus(query.strip())
    return f"https://pubmed.ncbi.nlm.nih.gov/?term={encoded_query}&page={page}"
