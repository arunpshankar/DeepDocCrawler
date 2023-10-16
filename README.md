# DocDive

Deep web exploration tool tailored for mining PDF document links from specified sites based on contextual queries.

## Table of Contents
- [Features](#features)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Deep crawling of specified websites.
- Contextual query-based PDF document mining.
- Scalable and efficient design.

## Installation & Setup

### Prerequisites
- [Python 3.9+](https://www.python.org/downloads/)
- [VSCode](https://code.visualstudio.com/)

### Setup Instructions
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/DocDive.git
    cd DocDive
    ```

2. **Setting up Virtual Environment in VSCode**:
    - Open the project folder in VSCode.
    - Press `Ctrl+Shift+P` to open the command palette.
    - Type and select "Python: Select Interpreter".
    - Choose "Enter interpreter path" > "Find...".
    - Navigate to the Python executable you want to use, or simply use the one VSCode suggests.
    - After selecting the interpreter, click on the Python version on the bottom-left of the status bar.
    - Choose "Create Virtual Environment".
    - Provide a name for the virtual environment (e.g., `venv`) and choose a location. Ideally, store it inside the project directory.
    - Wait for VSCode to create the virtual environment.

3. **Activating the Virtual Environment**:
    - Open the integrated terminal in VSCode (`Ctrl+~`).
    - Navigate to the virtual environment directory (e.g., `cd venv/Scripts` on Windows or `cd venv/bin` on Linux/Mac).
    - Activate the virtual environment:
        - **Windows**: `.\Activate`
        - **Linux/Mac**: `source activate`

4. **Install Dependencies**:
    Once the virtual environment is activated, navigate back to the root of the project directory and run:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

```bash
python crawler.py --urls [URL_LIST_FILE] --queries [QUERY_FILE]
```