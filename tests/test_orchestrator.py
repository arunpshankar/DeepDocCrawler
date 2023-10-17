from src.orchestrate.orchestrator import LLMOrchestrator

orchestrator = LLMOrchestrator(api_key="YOUR_API_KEY")

# For testing, consider you have some sample content (this is just a placeholder)
sample_content = "Content about machine learning and GPT-3."

# Get guidance from the LLM
guidance = orchestrator.guide_crawl(sample_content)
print("LLM Guidance:", guidance)
