# PubMed Literature Scraper

Automated scraper for biomedical research papers from PubMed.

## Features
- Search PubMed with custom queries
- Configurable rate limiting
- JSON output format
- Query validation

## Usage
from scraper.pubmed_scraper import PubMedScraper
scraper = PubMedScraper()
results = scraper.search("crispr gene therapy", max_results=100)
text

## Ethical Considerations
- Default delay between requests: 2 seconds
- User-agent rotation supported
- Respects robots.txt exclusion standards

## Configuration
Edit `config/settings.py`:
REQUEST_DELAY = 2 # Seconds between requests
HEADERS = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ResearchScraper/1.0'
}
text
undefined
