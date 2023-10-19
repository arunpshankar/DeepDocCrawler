from src.config.logging import setup_logger
from crawl.crawler import WebCrawler
from src.prune.pruner import Pruner
import jsonlines
import asyncio


logger = setup_logger()
DEPTH = 3

def main():
    with jsonlines.open('./config/sites.jsonl') as sites:
        for site in sites:
            company = site['Company']
            url = site['URL']
            crawler = WebCrawler(base_url=url, depth=DEPTH, company=company)
            asyncio.run(crawler.crawl())
    pruner = Pruner()
    pruner.process_files()

if __name__ == '__main__':
    main()