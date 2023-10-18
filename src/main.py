from config.setup import load_config
from crawl.crawler import WebCrawler
from mine.miner import PDFMiner
from orchestrate.orchestrator import LLMOrchestrator
import jsonlines
import asyncio


DEPTH = 20

def main():
    config = load_config('./config/config.yml')
    
    data = []
    with jsonlines.open('./config/sites.jsonl') as sites:
        for site in sites:
            print(site)
            company = site['Company']
            url = site['URL']
            crawler = WebCrawler(base_url=url, depth=DEPTH, company=company)
            asyncio.run(crawler.crawl())

if __name__ == "__main__":
    main()