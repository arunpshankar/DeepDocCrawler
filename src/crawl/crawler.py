from typing import Dict
from typing import List
import jsonlines
from src.scrape.scraper import WebScraper
from src.config.logging import setup_logger

logger = setup_logger()


class WebCrawler:
    def __init__(self, base_url: str, depth: int = 2):
        self.base_url = base_url
        self.depth = depth
        self.internal_links = []
        self.scraper = WebScraper(base_url)

    def level_crawler(self, input_url: str) -> List[Dict[str, str]]:
        """Crawl a single level of the website."""
        found_pages = self.scraper.extract_links(input_url)
        urls = [link for link in found_pages if link['child'] not in [existing_link['child'] for existing_link in self.internal_links]]
        self.internal_links.extend(urls)
        return urls

    def crawl(self):
        """Crawl the website to the specified depth."""
        queue = [self.base_url]
        for _ in range(self.depth):
            temp_queue = []
            for url in queue:
                found_pages = self.level_crawler(url)
                temp_queue.extend([link_info['child'] for link_info in found_pages])
            queue = temp_queue
        self.save_links(self.internal_links)

    def save_links(self, links: List[Dict[str, str]], file_path='./data/crawled_links.jsonl'):
        """Save the links to a jsonlines file."""
        with jsonlines.open(file_path, mode='w') as writer:
            for link in links:
                writer.write(link)

if __name__ == '__main__':
    crawler = WebCrawler(base_url='https://www.coralgables.com/', depth=2)
    crawler.crawl()
