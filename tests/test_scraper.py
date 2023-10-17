from src.scrape.scraper import Scraper

scraper = Scraper()

# For testing, consider you have some sample HTML content (this is just a placeholder)
sample_html = "<a href='https://example.com/doc1.pdf'>Document 1</a>"

# Extract links
links = scraper.extract_links(sample_html)
print("Extracted Links:", links)
