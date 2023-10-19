from src.config.logging import setup_logger
from crawl.crawler import WebCrawler
from src.prune.pruner import Pruner
import jsonlines
import asyncio


# Constants
DEPTH = 3
SITES_CONFIG_PATH = './config/sites.jsonl'

# Setting up the logger
logger = setup_logger()


def crawl_sites():
    """
    Crawls the websites specified in the sites configuration file.
    """
    with jsonlines.open(SITES_CONFIG_PATH) as sites:
        for site in sites:
            company = site['Company']
            url = site['URL']

            logger.info(f"Starting crawl for {company} at {url}...")
            crawler = WebCrawler(base_url=url, depth=DEPTH, company=company)
            asyncio.run(crawler.crawl())
            logger.info(f"Completed crawl for {company}.")


def prune_files():
    """
    Processes and prunes the files resulting from the crawl.
    """
    pruner = Pruner()
    pruner.process_files()


def main():
    """
    Main execution function: Crawls the specified sites and then processes the resulting files.
    """
    logger.info("Starting the web crawling process...")
    crawl_sites()
    
    logger.info("Starting the file pruning process...")
    prune_files()

    logger.info("All processes completed successfully!")


if __name__ == '__main__':
    main()