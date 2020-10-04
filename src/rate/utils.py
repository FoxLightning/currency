# from bs4 import BeautifulSoup, NavigableString


# import requests


# html_doc = requests.get('https://alfabank.ua/currency-exchange')

# soup = BeautifulSoup(html_doc.text, 'html.parser')

# rows = soup.find_all('span', {'class': 'rate-number'})

# usd_buy, usd_sale, eur_buy, eur_sale = [float(i.text) for i in rows][:4]
