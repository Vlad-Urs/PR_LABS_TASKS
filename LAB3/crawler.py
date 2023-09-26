import requests
from bs4 import BeautifulSoup
import re
# Replace with the URL of the web page you want to scrape
url = "https://999.md/ro/list/transport/bicycles?page=1"

def scrape(site, urls, depth):
    print("page " + site[-1])
    reqs = requests.get(site)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    
    for link in soup.find_all('a'):
        href = link.get('href')
        if re.search(r"/ro/[0-9][0-9]", str(href)) and href not in urls:
            urls.append(href)
    
    if int(site[-1]) <= depth:
        scrape("https://999.md/ro/list/transport/bicycles?page=" + str(int(site[-1]) + 1), urls, depth)
    return urls

urls = []
scrape(url, urls, 3)
for lnk in urls:
    print("https://999.md" + lnk)

