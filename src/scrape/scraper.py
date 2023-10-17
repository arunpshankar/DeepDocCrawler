from src.config.logging import setup_logger
from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from typing import Tuple
from typing import Dict
from typing import List
import requests


logger = setup_logger()


class WebScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def clean_href(self, href: str) -> Tuple[str, str]:
        """Clean and parse the href links."""
        if not href:
            return None, None
        href = urljoin(self.base_url, href)
        parsed_href = urlparse(href)
        cleaned_href = f"{parsed_href.scheme}://{parsed_href.netloc}{parsed_href.path}"
        return cleaned_href, parsed_href

    def extract_links(self, input_url: str) -> List[Dict[str, str]]:
        """Extract internal links from a given page."""
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
                if current_url_domain in cleaned_href:
                    link_info = {
                        'root': self.base_url,
                        'parent': input_url,
                        'child': cleaned_href
                    }
                    urls.append(link_info)
        return urls
