from llm.selector import LLMSelector
from crawl.crawler import WebCrawler
from config.setup import load_config
from mine.miner import PDFMiner
import jsonlines
import asyncio


DEPTH = 2

def main():
    with jsonlines.open('./config/sites.jsonl') as sites:
        for site in sites:
            print(site)
            company = site['Company']
            url = site['URL']
            crawler = WebCrawler(base_url=url, depth=DEPTH, company=company)
            asyncio.run(crawler.crawl())

if __name__ == '__main__':
    main()