# API and scraping parameters
REQUEST_DELAY = 2.0  # Seconds between requests
MAX_RETRIES = 3
TIMEOUT = 15  # Seconds
USER_AGENT = "ResearchScraper/1.0 (+https://yourdomain.com/bot-info)"

# HTML parsing selectors
SELECTORS = {
    'article_container': 'article.docsum-summary',
    'title': 'a.docsum-title',
    'authors': 'span.docsum-authors',
    'citation': 'span.docsum-journal-citation',
    'link': 'a.docsum-title'
}

# Ethical constraints
MAX_RESULTS_PER_QUERY = 500
MAX_REQUESTS_PER_HOUR = 180
