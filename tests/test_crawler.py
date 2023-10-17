from src.crawl.crawler import DeepCrawler

crawler = DeepCrawler()

# Test crawling a sample URL
urls = crawler.crawl("https://example1.com")
print("Crawled URLs:", urls)