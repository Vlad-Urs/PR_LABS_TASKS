import socket
import html_text
import json

def tcp_parser(url):  
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 8080))

    s.send(f"GET {url} HTTP/1.1\r\nHost:127.0.0.1\r\n\r\n".encode())
    response = s.recv(4096)
    s.close()

    return response.decode()


info = dict()

info["home_page"] = html_text.extract_text(tcp_parser('/')).replace('HTTP/1.1 200 OK Content-Type: text/html', '').splitlines()
info["about_page"] = html_text.extract_text(tcp_parser('/about')).replace('HTTP/1.1 200 OK Content-Type: text/html', '').splitlines()
info["contacts_page"] = html_text.extract_text(tcp_parser('/contacts')).replace('HTTP/1.1 200 OK Content-Type: text/html', '').splitlines()
products_page_raw = tcp_parser('/products')
info["products_page"] = html_text.extract_text(tcp_parser('/products')).replace('HTTP/1.1 200 OK Content-Type: text/html', '').splitlines()


products_number = products_page_raw.count('/prod')
product_links = []

# extract the links from products page
for i in range(products_number):
    pos = products_page_raw.find('/prod')
    print(f'pos = {pos}')
    link = ''
    while products_page_raw[pos] != '>':
        link += products_page_raw[pos]
        pos += 1
    products_page_raw = products_page_raw.replace("/prod"," ",1)
    product_links.append(link)

for prod in product_links:

    info[f"product_page {prod[-1]}"] = html_text.extract_text(tcp_parser(prod)).replace('HTTP/1.1 200 OK Content-Type: text/html', '').splitlines()

print(product_links)

for key in info:
    print(f'{key} : {info[key]}')

with open("scrapped_pages.json", "w") as outfile:
    json.dump(info, outfile)
    
