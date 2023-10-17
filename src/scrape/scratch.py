import requests
from bs4 import BeautifulSoup

# URL to parse
url = "https://www.brooklinebancorp.com/rss/presentation.aspx"

# Send a GET request with a user-agent header
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
response = requests.get(url, headers=HEADERS)

# Ensure the request was successful
if response.status_code == 200:
    # Parse the RSS feed as XML
    soup = BeautifulSoup(response.content, 'lxml-xml')

    # Iterate through each item in the RSS feed
    for item in soup.find_all('item'):
        
        link = item.find('link')
        if link and link.text:
            print('=>', link.text)
        print('-' * 100)
else:
    print(f"Failed to retrieve the content. HTTP Status Code: {response.status_code}")
