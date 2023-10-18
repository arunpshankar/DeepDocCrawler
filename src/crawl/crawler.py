from aiohttp.client_exceptions import ServerDisconnectedError
from aiohttp.client_exceptions import ClientError
from src.config.logging import setup_logger
from src.scrape.scraper import WebScraper
from typing import Dict
from typing import List
import jsonlines
import asyncio


logger = setup_logger()

MAX_RETRIES = 2
DELAY = 1 

class WebCrawler:
    def __init__(self, base_url: str, depth: int, company: str):
        """Initialize the web crawler with a base URL and depth."""
        self.base_url = base_url
        self.depth = depth
        self.company = company
        self.internal_links = set()  
        self.link_info_list = []    
        self.scraper = WebScraper(base_url)

    async def level_crawler(self, input_url: str) -> List[Dict[str, str]]:
        for retry in range(MAX_RETRIES):
            try:
                found_pages = await self.scraper.extract_links(input_url)
                new_links = []
                for link in found_pages:
                    if link['child'] not in self.internal_links:
                        self.internal_links.add(link['child'])
                        new_links.append({
                            'seed': self.base_url,
                            'parent': input_url,
                            'child': link['child']
                        })
                self.link_info_list.extend(new_links)
                return new_links
            except ServerDisconnectedError:
                logger.error(f"Server disconnected for URL: {input_url}. Retry {retry + 1}/{MAX_RETRIES}.")
                await asyncio.sleep(DELAY * (2 ** retry))  # Exponential backoff
            except ClientError as e:
                logger.error(f"Error fetching URL: {input_url}. Error: {e}")
                return []
        logger.error(f"Failed to fetch URL: {input_url} after {MAX_RETRIES} retries.")
        return []

    async def crawl(self):
        queue = [self.base_url]
        visited = set()  # To keep track of visited links

        for i in range(self.depth):
            logger.info(f'DEPTH = {i}')
            temp_queue = []
            results = await asyncio.gather(*(self.level_crawler(url) for url in queue if url not in visited))
            
            for url in queue:
                visited.add(url)  # Mark the URL as visited
            
            for found_pages in results:
                for link_info in found_pages:
                    if link_info['child'] not in visited:
                        temp_queue.append(link_info['child'])
            
            queue = temp_queue
        self.save_links(self.link_info_list)

    def save_links(self, links: List[Dict[str, str]]):
        """
        Save the found links to a jsonlines file.
        """
        file_path = f'./data/crawled_urls/{self.company}.jsonl'
        with jsonlines.open(file_path, mode='w') as writer:
            for link_info in links:
                writer.write({
                    'seed': link_info['seed'],
                    'parent': link_info['parent'],
                    'child': link_info['child']
                })