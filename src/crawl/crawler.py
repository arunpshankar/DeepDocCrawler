from urllib.request import urljoin 
from bs4 import BeautifulSoup 
import requests 
from urllib.request import urlparse 
from src.config.logging import setup_logger
import jsonlines
import yaml

logger = setup_logger()

# Set for storing URLs with the same domain 
links_intern = set() 

# Set for storing URLs with different domains 
links_extern = set() 

# Load configuration
def load_config(config_path="./config/config.yml") -> dict:
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

config = load_config()

def level_crawler(input_url): 
    current_url_domain = urlparse(input_url).netloc 
    beautiful_soup_object = BeautifulSoup(requests.get(input_url).content, "lxml") 
    temp_urls = set()

    for anchor in beautiful_soup_object.findAll("a"): 
        href = anchor.attrs.get("href") 
        if(href != "" and href is not None): 
            href = urljoin(input_url, href) 
            href_parsed = urlparse(href) 
            is_valid = bool(href_parsed.scheme) and bool(href_parsed.netloc) 
            if is_valid: 
                if current_url_domain not in href and href not in links_extern: 
                    logger.info("Extern - {}".format(href)) 
                    links_extern.add(href) 
                if current_url_domain in href and href not in links_intern: 
                    logger.info("Intern - {}".format(href)) 
                    links_intern.add(href) 
                    temp_urls.add(href) 
    return temp_urls 

def bfs_crawler(seed_url):
    # BFS queue
    queue = [seed_url]
    
    while queue:
        url = queue.pop(0)
        urls_from_page = level_crawler(url)
        for new_url in urls_from_page:
            if new_url not in links_intern:
                queue.append(new_url)
                links_intern.add(new_url)

    return links_intern

def save_links(links, filename="./data/crawled_links.jsonl"):
    structured_links = [{"seed": seed_url, "subsite": link} for link in links]
    with jsonlines.open(filename, mode='w') as writer:
        for link in structured_links:
            writer.write(link)

if __name__ == "__main__":
    for site in config["sites"]:
        seed_url = site["url"]
        bfs_crawler(seed_url)

    save_links(links_intern)
    logger.info(f"Successfully crawled {len(links_intern)} links and saved to 'crawled_links.jsonl'.")
