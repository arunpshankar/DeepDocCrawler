from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from typing import Tuple, Dict, List, Optional
import requests
from src.config.logging import setup_logger

logger = setup_logger()

class WebScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def clean_href(self, href: str) -> Tuple[Optional[str], Optional[urlparse]]:
        """Clean and parse the href links."""
        if not href:
            return None, None
        href = urljoin(self.base_url, href)
        parsed_href = urlparse(href)
        cleaned_href = f"{parsed_href.scheme}://{parsed_href.netloc}{parsed_href.path}"
        return cleaned_href, parsed_href

    def extract_links(self, input_url: str) -> List[Dict[str, str]]:
        """Extract internal links from a given page."""
        
        # Define the headers for the request. Using a commonly accepted user-agent for compatibility.
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        current_url_domain = urlparse(input_url).netloc
        urls = []

        logger.info(f'Scraping URL: {input_url}')
        
        # Sending a GET request to the specified URL with the defined headers.
        response = requests.get(input_url, headers=HEADERS)

        # Check if the response status code is other than 200 (OK). If so, log a warning and return an empty list.
        if response.status_code != 200:
            logger.warning(f"Failed to retrieve {input_url}")
            logger.warning(response)
            return urls

        # Parse the content of the page using BeautifulSoup.
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Find all anchor tags in the parsed content.
        anchor_links = soup.find_all('a')

        # Loop through each anchor tag to extract and clean the href links.
        for anchor in anchor_links:
            href = anchor.attrs.get('href')
            cleaned_href, parsed_href = self.clean_href(href)

            # Check if the href link is valid and belongs to the same domain as the input URL.
            if parsed_href and parsed_href.scheme and parsed_href.netloc and current_url_domain in cleaned_href:
                link_info = {
                    'root': self.base_url,
                    'parent': input_url,
                    'child': cleaned_href
                }
                urls.append(link_info)

        return urls
