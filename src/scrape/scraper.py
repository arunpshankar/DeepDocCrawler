from src.config.logging import setup_logger
from urllib.parse import urlparse
from aiohttp import ClientTimeout
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from bs4.builder import ParserRejectedMarkup
from typing import Optional
from chardet import detect
from random import choice
from typing import Tuple
from typing import Dict
from typing import List
import requests
import asyncio
import aiohttp


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
    
    def core_domain_match(self, url1: str, url2: str) -> bool:
        """
        Check if the core domain (ignoring schemes, www, and top-level domains) of two URLs match.
        
        Parameters:
        - url1, url2 (str): The URLs to compare.
        
        Returns:
        - Boolean indicating if the core domains are the same.
        """
        
        def extract_core_domain(url: str) -> str:
            # Extract the domain from the URL
            domain = urlparse(url).netloc or urlparse("http://" + url).netloc
            # Remove 'www.' prefix if present
            domain = domain.replace("www.", "")
            # Strip top-level domain (e.g., .com, .org, etc.)
            core_domain = domain.split('.')[0]
            return core_domain
        
        return extract_core_domain(url1) == extract_core_domain(url2)


    async def extract_links(self, input_url: str) -> List[Dict[str, str]]:
        USER_AGENTS = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36 OPR/62.0.3331.18',
            'Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1'
        ]
        headers = {
            'User-Agent': choice(USER_AGENTS)
        }

        current_url_domain = urlparse(input_url).netloc
        urls = []
        max_retries = 2

        for retry in range(max_retries + 1):  # +1 to account for the first try
            logger.info(f'Scraping URL: {input_url} (Attempt: {retry + 1})')
            timeout = ClientTimeout(total=10)  # Set to 10 seconds

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(input_url, headers=headers, timeout=timeout) as response:
                        if response.status != 200:
                            logger.warning(f"Failed to retrieve {input_url} with status {response.status}. Falling back to synchronous call.")
                            raise ValueError("Non-200 status code")
                        
                        content_type = response.headers.get('Content-Type', '').lower()
                        if 'text' not in content_type:
                            logger.warning(f"Non-textual content at {input_url}. Skipping.")
                            return urls

                        content_bytes = await response.read()
                        if 'charset=utf-8' in content_type:
                            content = content_bytes.decode('utf-8')
                        else:
                            detected_encoding = detect(content_bytes)['encoding']
                            content = content_bytes.decode(detected_encoding or 'utf-8', errors='ignore')
                        break  # If successful, break out of the retry loop

            except (aiohttp.ClientConnectorSSLError, aiohttp.ClientConnectorError, asyncio.TimeoutError, ValueError) as e:
                error_type = type(e).__name__
                logger.warning(f"Async error occurred for {input_url}. Type={error_type} Falling back to synchronous call.")
                if retry == max_retries or isinstance(e, ValueError):  # Retry on async errors but immediately fallback on ValueError
                    try:
                        response = requests.get(input_url, headers=headers)
                        content = response.text
                    except requests.RequestException as req_e:
                        logger.error(f"Failed to retrieve {input_url} with synchronous call. Error: {req_e}")
                        return urls

        try:
            soup = BeautifulSoup(content, 'html.parser')
            anchor_links = soup.find_all('a')
            for anchor in anchor_links:
                href = anchor.get('href')
                cleaned_href, parsed_href = self.clean_href(href)
                if parsed_href and parsed_href.scheme and parsed_href.netloc and self.core_domain_match(current_url_domain, cleaned_href):
                    link_info = {
                        'root': self.base_url,
                        'parent': input_url,
                        'child': cleaned_href
                    }
                    urls.append(link_info)
        except ParserRejectedMarkup:
            # Handle the BeautifulSoup parsing exception
            logger.error(f"Failed to parse content from {input_url}. The provided markup may be malformed or in an unexpected format.")
            return []
        except Exception as e:
            # General error handling
            logger.error(f"An unexpected error occurred while processing {input_url}. Error: {e}")
            return []

        return urls
