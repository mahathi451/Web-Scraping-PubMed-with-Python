import pytest
from unittest.mock import patch
from scraper.pubmed_scraper import PubMedScraper
from bs4 import BeautifulSoup

@pytest.fixture
def mock_article_html():
    return """
    <article class="docsum-summary">
      <a class="docsum-title" href="/12345/">Test Article</a>
      <span class="docsum-authors">Smith J, Doe A</span>
      <span class="docsum-journal-citation">J Test Sci 2023</span>
    </article>
    """

def test_full_parse(mock_article_html):
    with patch('scraper.pubmed_scraper.PubMedScraper._get_page') as mock_get:
        mock_get.return_value = BeautifulSoup(mock_article_html, 'lxml')
        
        scraper = PubMedScraper()
        results = scraper.search("test query", max_results=1)
        
        assert len(results) == 1
        assert results[0]['pmid'] == '12345'
        assert 'Smith J' in results[0]['authors']

def test_rate_limiting():
    scraper = PubMedScraper()
    scraper.search("test", max_results=1)
    assert scraper.request_count == 1
    scraper.search("test", max_results=1)
    assert scraper.request_count == 2

def test_query_validation():
    scraper = PubMedScraper()
    with pytest.raises(ValueError):
        scraper.search("a" * 301)
    with pytest.raises(ValueError):
        scraper.search("invalid@character")
