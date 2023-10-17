from config.setup import load_config
from crawl.crawler import WebCrawler
from mine.miner import PDFMiner
from orchestrate.orchestrator import LLMOrchestrator

def main():
    config = load_config('./config/config.yml')
    crawler = WebCrawler(base_url='https://www.brooklinebancorp.com/', depth=10)
    crawler.crawl()

if __name__ == "__main__":
    main()