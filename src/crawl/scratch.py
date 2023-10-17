import jsonlines
import requests
from bs4 import BeautifulSoup
from typing import Tuple, Set, Dict, List
from urllib.parse import urlparse, urljoin
from src.config.logging import setup_logger

logger = setup_logger()

class WebCrawler:
    def __init__(self, base_url: str, depth: int = 2):
        self.base_url = base_url
        self.depth = depth
        self.internal_links = []

    def clean_href(self, href: str) -> Tuple[str, str]:
        """Clean and parse the href links."""
        if not href:
            return None, None
        href = urljoin(self.base_url, href)
        parsed_href = urlparse(href)
        cleaned_href = f"{parsed_href.scheme}://{parsed_href.netloc}{parsed_href.path}"
        return cleaned_href, parsed_href

    def level_crawler(self, input_url: str) -> List[Dict[str, str]]:
        """Crawl a single level of the website."""
        current_url_domain = urlparse(input_url).netloc
        urls = []

        logger.info(f'Scraping URL: {input_url}')
        response = requests.get(input_url)
        if response.status_code != 200:
            logger.warning(f"Failed to retrieve {input_url}")
            return urls

        soup = BeautifulSoup(response.content, 'lxml')
        for anchor in soup.findAll('a'):
            href = anchor.attrs.get('href')
            cleaned_href, parsed_href = self.clean_href(href)
            
            if parsed_href and parsed_href.scheme and parsed_href.netloc:
                if current_url_domain in cleaned_href and cleaned_href not in [link['child'] for link in self.internal_links]:
                    logger.info(f'Found: {cleaned_href}')
                    link_info = {
                        'root': self.base_url,
                        'parent': input_url,
                        'child': cleaned_href
                    }
                    urls.append(link_info)
                    self.internal_links.append(link_info)
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
