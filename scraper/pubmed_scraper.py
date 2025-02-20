from bs4 import BeautifulSoup
import requests
import time
from .utils import validate_query
from config import settings

class PubMedScraper:
    def __init__(self):
        self.base_url = "https://pubmed.ncbi.nlm.nih.gov"
        self.delay = settings.REQUEST_DELAY
        
    def search(self, query, max_results=100):
        validate_query(query)
        results = []
        page = 1
        
        while len(results) < max_results:
            url = f"{self.base_url}/search/?term={query}&page={page}"
            response = requests.get(url, headers=settings.HEADERS)
            soup = BeautifulSoup(response.text, 'lxml')
            
            articles = soup.find_all('article', class_='full-docsum')
            if not articles:
                break
                
            for article in articles:
                if len(results) >= max_results:
                    break
                    
                title = article.find('a', class_='docsum-title').text.strip()
                authors = article.find('span', class_='docsum-authors').text.strip()
                citation = article.find('span', class_='docsum-journal-citation').text.strip()
                
                results.append({
                    'title': title,
                    'authors': authors,
                    'citation': citation,
                    'link': f"{self.base_url}{article.a['href']}"
                })
                
            time.sleep(self.delay)
            page += 1
            
        return results[:max_results]
