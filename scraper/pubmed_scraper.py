import requests
from bs4 import BeautifulSoup
import time
import logging
from typing import List, Dict
from .utils import validate_query, format_search_url
from config import settings

logger = logging.getLogger(__name__)

class PubMedScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': settings.USER_AGENT})
        self.request_count = 0
        self.last_request_time = 0.0

    def _rate_limit(self):
        """Enforce request rate limiting"""
        elapsed = time.time() - self.last_request_time
        if elapsed < settings.REQUEST_DELAY:
            time.sleep(settings.REQUEST_DELAY - elapsed)
        self.last_request_time = time.time()
        self.request_count += 1

        if self.request_count >= settings.MAX_REQUESTS_PER_HOUR:
            logger.warning("Hourly request limit reached")
            time.sleep(3600)
            self.request_count = 0

    def _get_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse page content with retries"""
        for attempt in range(settings.MAX_RETRIES):
            try:
                self._rate_limit()
                response = self.session.get(
                    url, 
                    timeout=settings.TIMEOUT,
                    allow_redirects=True
                )
                response.raise_for_status()
                return BeautifulSoup(response.text, 'lxml')
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt+1} failed: {str(e)}")
                time.sleep(2 ** attempt)
        raise ConnectionError(f"Failed to retrieve {url}")

    def search(self, query: str, max_results=100) -> List[Dict]:
        """Execute PubMed search with pagination"""
        validate_query(query)
        results = []
        page = 1
        
        while len(results) < min(max_results, settings.MAX_RESULTS_PER_QUERY):
            url = format_search_url(query, page)
            soup = self._get_page(url)
            
            articles = soup.select(settings.SELECTORS['article_container'])
            if not articles:
                break

            for article in articles:
                if len(results) >= max_results:
                    break

                try:
                    result = {
                        'title': article.select_one(settings.SELECTORS['title']).text.strip(),
                        'authors': article.select_one(settings.SELECTORS['authors']).text.strip(),
                        'citation': article.select_one(settings.SELECTORS['citation']).text.strip(),
                        'link': f"https://pubmed.ncbi.nlm.nih.gov{article.select_one(settings.SELECTORS['link'])['href']}",
                        'pmid': article.select_one(settings.SELECTORS['link'])['href'].split('/')[-2]
                    }
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error parsing article: {str(e)}")

            page += 1
            
        return results
