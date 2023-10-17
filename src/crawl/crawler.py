from src.config.logging import setup_logger
from src.scrape.scraper import WebScraper
from typing import Dict, List
import jsonlines

# Setting up the logger
logger = setup_logger()

class WebCrawler:
    def __init__(self, base_url: str, depth: int = 2):
        """Initialize the web crawler with a base URL and depth."""
        self.base_url = base_url
        self.depth = depth
        # List to store internal links found during crawling
        self.internal_links = []
        # Initializing the scraper object
        self.scraper = WebScraper(base_url)

    def level_crawler(self, input_url: str) -> List[Dict[str, str]]:
        """
        Crawl a single level of the website and return found pages.
        
        Args:
        - input_url (str): The URL to start crawling from.

        Returns:
        - List[Dict[str, str]]: A list of dictionaries containing parent and child links.
        """
        found_pages = self.scraper.extract_links(input_url)
        # Filtering out links already in the internal_links list
        urls = [link for link in found_pages if link['child'] not in [existing_link['child'] for existing_link in self.internal_links]]
        self.internal_links.extend(urls)
        return urls

    def crawl(self):
        """Crawl the website up to the specified depth."""
        # Initializing the queue with the base URL
        queue = [self.base_url]
        for _ in range(self.depth):
            temp_queue = []
            for url in queue:
                found_pages = self.level_crawler(url)
                # Extending the queue with child links of found pages
                temp_queue.extend([link_info['child'] for link_info in found_pages])
            queue = temp_queue
        self.save_links(self.internal_links)

    def save_links(self, links: List[Dict[str, str]], file_path='./data/crawled_links.jsonl'):
        """
        Save the found links to a jsonlines file.
        
        Args:
        - links (List[Dict[str, str]]): List of dictionaries containing found links.
        - file_path (str, optional): Path to save the jsonlines file. Defaults to './data/crawled_links.jsonl'.
        """
        with jsonlines.open(file_path, mode='w') as writer:
            for link in links:
                writer.write(link)
