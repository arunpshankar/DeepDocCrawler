from src.config.logging import setup_logger
from multiprocessing import cpu_count
from multiprocessing import Pool
from bs4 import BeautifulSoup
from src.prune.llm import LLM
import requests
import json
import os


class Pruner:
    def __init__(self):
        pass
    
    def is_pdf_url(self, url):
        """Check if the URL points to a PDF."""
        return url.lower().endswith('.pdf')
    
    def classify_content(self, content, child_url):
        """Classify the content into one of the specified topics using the LLM prompt."""
        prompt = self.llm.construct_prompt(content, child_url)
        response_str = self.llm.classify(prompt)
        clean_response_str = response_str.replace('```JSON\n', '').replace('```', '').strip()
        classification_json = json.loads(clean_response_str)
        classification = classification_json['classification']
        rationale = classification_json['rationale']
        return classification, rationale

    def download_pdf(self, url, company_name, file_name):
        """Download the PDF from the given URL and save it with the specified filename."""
        response = requests.get(url)
        with open(f'./data/collected_pdfs/{company_name}/{file_name}.pdf', 'wb') as file:
            file.write(response.content)
    
    def save_metadata(self, metadata, company_name):
        """Save the classification and rationale as metadata."""
        with open(f'./data/selected_urls/{company_name}_metadata.jsonl', 'w') as file:
            json.dump(metadata, file)

    def process_single_line(self, line, file_name):
        logger = setup_logger()
        llm = LLM()

        data = json.loads(line)
        child_url = data['child']
        if self.is_pdf_url(child_url):
            logger.info(f'URL to classify: {child_url}') 
            response = requests.get(data['parent'])
            soup = BeautifulSoup(response.text, 'html.parser')
            prompt = llm.construct_prompt(soup.text, child_url)  # Use llm here
            response_str = llm.classify(prompt)  # Use llm here
            clean_response_str = response_str.replace('```JSON\n', '').replace('```', '').strip()
            classification_json = json.loads(clean_response_str)
            classification = classification_json['classification']
            rationale = classification_json['rationale']
            if classification != 'Unclassified':
                self.download_pdf(child_url, file_name)
                metadata = {
                    'classification': classification,
                    'rationale': rationale
                }
                self.save_metadata(metadata, file_name)
    
    def process_files(self):
        """Process all the JSONL files in the data/crawled_urls/ directory."""
        # Ensure the collected_pdfs directory exists
        if not os.path.exists('./data/collected_pdfs'):
            os.makedirs('./data/collected_pdfs')
        
        # Use a Pool of workers
        with Pool(cpu_count()) as pool:
            # Iterate over all the JSONL files in the directory
            for filename in os.listdir('./data/crawled_urls/'):
                with open(f'./data/crawled_urls/{filename}', 'r') as file:
                    # Use starmap to pass multiple arguments to process_single_line
                    pool.starmap(self.process_single_line, [(line, filename) for line in file])

if __name__ == '__main__':
    pruner = Pruner()
    pruner.process_files()
