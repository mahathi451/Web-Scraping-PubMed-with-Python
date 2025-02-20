from scraper.pubmed_scraper import PubMedScraper
import json

def main():
    scraper = PubMedScraper()
    results = scraper.search("machine learning cancer", max_results=50)
    
    with open('pubmed_results.json', 'w') as f:
        json.dump(results, f, indent=2)
        
if __name__ == "__main__":
    main()
