import requests
from bs4 import BeautifulSoup

url = 'https://www.oyeintelligence.com'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Now you can use various BeautifulSoup methods to extract data
# For example, to get all the anchor tags:
links = soup.find_all('a')

for link in links:
    print(link.get('href'))
