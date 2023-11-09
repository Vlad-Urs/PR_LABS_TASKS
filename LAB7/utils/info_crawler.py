import requests
from bs4 import BeautifulSoup




def scrap_info(url):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    info = {
    "url" : '',
    "name" : '',
    "price" : '',
    "seller" : '',
    "date" : '',
    "transaction type" : '',
    "views" : ''
    }

    info["url"] = url

    # get the name
    info["name"] = soup.find('h1').get_text()

    # get seller
    try:
        info["seller"] = soup.find('a', {'class' : 'adPage__aside__stats__owner__login buyer_experiment'}).get_text()
    except:
        pass

    # get time update
    info["date"] = soup.find('div', {'class' : 'adPage__aside__stats__date'}).get_text()[19:]

    # get transaction tipe
    info["transaction type"] = soup.find('div', {'class' : 'adPage__aside__stats__type'}).get_text()[7:]

    # get views
    info["views"] = soup.find('div', {'class' : 'adPage__aside__stats__views'}).get_text()[13:]

    # get price and currency
    info["price"] = soup.find('span', {'class' : 'adPage__content__price-feature__prices__price__value'}).get_text()
    currency = soup.find('span', {'class' : 'adPage__content__price-feature__prices__price__currency'})
    if currency:
        info["price"] += currency.get_text()
        
    # extract characteristics
    characteristics = []
    for div in soup.findAll('div', {'class' : 'adPage__content__features'}):

        # get the characteristics
        for characteristics_div in div.findAll('div', {'class' : 'adPage__content__features__col grid_9 suffix_1'}):
            for ul in characteristics_div.findAll('ul'):
                for link in ul.findAll('span'):
                    characteristics.append(link.text.lstrip().rstrip())
            
            for i in range(0,len(characteristics)-1,2):
                info.update({characteristics[i] : characteristics[i+1]})

    
    # get description
    try:
        info.update({"description" : soup.find('div', {'class' : 'adPage__content__description grid_18'}).get_text()})
    except:
        info.update({"description" : "no user description"})


    return info