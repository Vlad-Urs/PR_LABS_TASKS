import requests
from bs4 import BeautifulSoup
import re
# Replace with the URL of the web page you want to scrape
url = "https://999.md/ro/list/transport/bicycles"


reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')
 
urls = []
for link in soup.find_all('a'):
    print(link.get('href'))


'''
def scrape(site, urls, depth):
    
    # getting the request from url
    r = requests.get(site)
       
    # converting the text
    s = BeautifulSoup(r.text,"html.parser")
       
    for i in s.find_all("a"):         
        href = i.attrs['href']
        
        
               
        if depth > 0:
            urls.append(href)
            if href.startswith("https://999.md/ro/"):
                urls.append(href)   
                print(href)              
            # calling it self
            scrape(site, urls, depth-1)
        else:
            return urls


print(scrape(url, urls, 5))
'''