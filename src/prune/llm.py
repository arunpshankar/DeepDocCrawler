from langchain.prompts.chat import SystemMessagePromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain.prompts.chat import ChatPromptTemplate
from src.config.setup import set_google_credentials
from langchain.chat_models import ChatVertexAI
from src.config.logging import setup_logger
import json


logger = setup_logger()

MODEL_NAME = 'chat-bison'


class LLM:
    def __init__(self):
        # Initialize topics list
        self.topics = []
        
        # Set up Google credentials for Vertex AI
        set_google_credentials('./credentials/vai-key.json')
        
        # Load the model
        self.model = self.load_model()
        
        # Load topics from the provided JSONL file
        self.load_jsonl('./config/topics.jsonl')

    def load_model(self):
        """Load the chat model from Vertex AI."""
        model = ChatVertexAI(model_name=MODEL_NAME, temperature=0, max_output_tokens=512, verbose=True)
        return model

    def load_jsonl(self, filepath):
        """Load the topics from the provided JSONL file."""
        with open(filepath, 'r') as file:
            for line in file:
                self.topics.append(json.loads(line))

    def construct_prompt(self, page_content, pdf_url):
        """
        Construct a text prompt based on the loaded topics.
        
        Parameters:
        - page_content: HTML content of the page
        - pdf_url: URL of the accompanying PDF
        
        Returns:
        - prompt: Text prompt for classification
        """
        # Create topics details for prompt
        topics_details = []
        for topic in self.topics:
            topic_info = f"Topic: {topic['type']}\n" \
                         f"Definition: {topic['definition']}\n" \
                         f"Synonyms: {topic['synonyms']}\n"
            topics_details.append(topic_info)
        
        topics_text = '\n'.join(topics_details)

        # Constructing system and human message prompts
        system_template = f"""You are a research analyst. 
Use the Topics info given below and classify the HTML page content and the accompanying PDF URL into relevant topics.
If the PDF url has any words or tokens that are related to the topic information mentioned above, consider that as classified.
If you cannot classify, use 'unclassified'.

==Topics==
{topics_text}
"""
        system_message_prompt = SystemMessagePromptTemplate.from_template(template=system_template)
        
        human_template = f"""==Page HTML Content==\n{page_content}\n===PDF URL==={pdf_url}
Please elucidate on the rationale behind your classification. Highlight any specific elements from the page content or PDF URL that influenced your decision. If unclassified, explain why.
Convey your classification and reasoning in a structured JSON with 2 fields `classification` and `rationale` ONLY."""
        human_message_prompt = HumanMessagePromptTemplate.from_template(template=human_template)  
        
        chat_prompt = ChatPromptTemplate(messages=[system_message_prompt, human_message_prompt])
        
        prompt = chat_prompt.format_messages()
        
        return prompt

    def classify(self, prompt):
        """
        Get the model's classification based on the prompt.
        
        Parameters:
        - prompt: Text prompt for classification
        
        Returns:
        - completion: Model's response
        """
        response = self.model(prompt)
        completion = response.content.strip()
        return completion
