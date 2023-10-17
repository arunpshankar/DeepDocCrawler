from src.miner.pdf_miner import PDFMiner

miner = PDFMiner(["machine learning", "GPT-3"])

# For testing, consider you have some sample links (these are just placeholders)
sample_links = ["https://example.com/doc1.pdf", "https://example.com/doc2.doc", "https://example.com/presentation.pptx"]

# Filter PDF, DOC, and PPTX links
filtered_links = miner.filter_pdf_links(sample_links)
print("Filtered Document Links:", filtered_links)
