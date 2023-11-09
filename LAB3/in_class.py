import requests
from bs4 import BeautifulSoup
import re
# Replace with the URL of the web page you want to scrape
url = "https://999.md/ro/list/sports-health-and-beauty/trainers-and-equipment"


def scrape_links(site, urls, depth):
    if site[-1] not in '0123456789':
        site = site + '?page=1'
    valid_page = False

    page_number = int(site[site.index("=")+1:])
    print(f"page {page_number}")
    reqs = requests.get(site)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    
    for link in soup.find_all('a'):
        href = link.get('href')
        if re.search(r"/ro/[0-9][0-9]", str(href)) and href not in urls:
            urls.append(href)
            valid_page = True
    
    if page_number < depth and valid_page:
        page_number += 1
        scrape_links(site[:-6] + "page=" + str(page_number), urls, depth)
    return urls

def scrape_info():
    pass

urls = []
scrape_links(url, urls, 10)

print(f"number of links: {len(urls)}")

with open('LAB3/urls.txt', 'w') as f:
    for lnk in urls:
        f.write("https://999.md" + lnk + "\n")