# 📜 DeepDocCrawler

A deep web exploration tool tailored for crawling a list of provided website URLs and mining deep links that point to PDFs. DeepDocCrawler uses context-based queries to decide which PDFs to download from the specified sites. It leverages Large Language Models (LLM) to smartly filter and prune the crawled URLs.

## 📌 Table of Contents

- [Features](#features)
- [Installation & Setup](#installation--setup)
- [Credentials Setup](#credentials-setup)
- [Usage](#usage)

## 🌟 Features

- **Deep Web Crawling**: Utilizes breadth-first search to deeply crawl specified websites up to a provided depth.
- **Smart PDF Selection**: Selects PDFs to download based on provided metadata and URL content type (.pdf). Uses LLMs to contextually decide whether to download a PDF.
- **Asynchronous Operations**: Works asynchronously, with most processes parallelized to run on multiple cores.

## 🛠 Installation & Setup

### Prerequisites

- [Python 3.9+](https://www.python.org/downloads/)
- [VSCode](https://code.visualstudio.com/)

### Setup Instructions

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/your-username/DeepDocCrawler.git
    cd DeepDocCrawler
    ```

2. **Setting up a Virtual Environment in VSCode**:
    - Open the project folder in VSCode.
    - Open the command palette with `Ctrl+Shift+P`.
    - Search for "Python: Select Interpreter" and select it.
    - Choose "Enter interpreter path" > "Find...".
    - Navigate to the Python executable you wish to use or select the one suggested by VSCode.
    - After selecting the interpreter, click the Python version at the bottom-left of the status bar.
    - Select "Create Virtual Environment" and provide a name (e.g., `venv`). Ideally, store it within the project directory.

3. **Activate the Virtual Environment**:
    - Open the integrated terminal in VSCode with `Ctrl+~`.
    - Navigate to the virtual environment directory (`cd venv/Scripts` on Windows or `cd venv/bin` on Linux/Mac).
    - Activate the virtual environment:
        - **Windows**: `.\Activate`
        - **Linux/Mac**: `source activate`

4. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

5. Set up the Python path:

    ```bash
    export PYTHONPATH=$PYTHONPATH:.
    ```

## 🔐 Credentials Setup

To utilize some advanced features, especially when integrating with Vertex AI, follow these steps:

1. Create a `credentials` folder in the root directory.
2. Place your Vertex AI project-specific service account key JSON file inside the `credentials` folder.

🚫 **Important**: Ensure your service account key and other sensitive data remain confidential. Always add the `credentials` folder to your `.gitignore` file.

## 🚀 Usage

1. Configure your crawl settings:
    - Under the `config` directory, populate `sites.jsonl` with the URLs you want to crawl.
    - Fill `topics.jsonl` with topics that will aid in pruning the PDF URLs.

2. Kick-off the crawling process:

    ```bash
    python src/main.py
    ```

    Note: Crawling can take several hours, depending on the initial configuration (number of sites and depth for BFS).

3. Once crawling completes, the tool processes the URLs to prune potential PDF candidates. It leverages Vertex AI's chat-bison LLM, using metadata from `topics.jsonl` to contextually evaluate PDF content. If the content aligns with specified topics, the PDF is considered for download.

4. The pruner classifies PDF URLs and saves them in a JSONL file (one per website) under the `selected_urls` directory. Example format:

    ```json
    {
      "company": "BANKHAUS J",
      "filename": "Offenlegungsbericht_2022",
      "classification": "Corporate Governance and Charter",
      "rationale": "The page content includes sections such as ..."
    }
    ```

5. Finally, the tool downloads the PDFs from the selected URLs and saves them in the `collected_pdfs` directory.

---
**Notes:**

- The default Breadth-First Search (BFS) depth is set to 3. Adjust as needed, but be aware that a higher depth will result in longer crawling times.
- PDFs saved in `collected_pdfs` under the `data` directory are ignored by Git to prevent unintentional pushes. Ensure to backup or persist your data as needed.