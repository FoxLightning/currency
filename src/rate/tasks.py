from decimal import Decimal

from bs4 import BeautifulSoup

from celery import shared_task

from rate.choices import TWOPLACES
from rate.utils import send_xml_to_all

import requests


@shared_task
def send_email_async(subject, text):
    from django.core.mail import send_mail
    send_mail(
        subject,
        text,
        'battlefieldblo@gmail.com',
        ['bogdanlisichenko@gmail.com'],
        fail_silently=False,
    )


def check_and_write(currency, source, sale, buy):
    from rate.models import Rate
    last_rate = Rate.objects.filter(source=source, currency=currency).last()
    if last_rate is None or buy != last_rate.buy or sale != last_rate.sale:
        Rate.objects.create(
            currency=currency,
            source=source,
            sale=sale,
            buy=buy,
            )


@shared_task
def parse_privatbank():
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    source = 1  # 1 = PrivatBank
    currency_map = {
        'USD': 1,
        'EUR': 2,
    }

    for row in filter(lambda x: x['ccy'] in currency_map, data):
        buy, sale = (Decimal(row[i]).quantize(TWOPLACES) for i in ('buy', 'sale',))
        currency = currency_map[row['ccy']]
        check_and_write(currency, source, sale, buy)


@shared_task
def parse_monobank():
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    source = 2  # 2 = MonoBank
    allow_currency = {
        840: 1,
        978: 2,
    }

    for dct in filter(lambda x: x['currencyCodeA'] in allow_currency and x['currencyCodeB'] == 980, data):
        buy, sale = (Decimal(dct[i]).quantize(TWOPLACES) for i in ('rateBuy', 'rateSell'))
        currency = allow_currency[dct['currencyCodeA']]
        check_and_write(currency, source, sale, buy)


@shared_task
def parse_vkurse():
    url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    source = 3
    currency_map = {
        'Dollar': 1,
        'Euro': 2,
    }

    for key, currency in currency_map.items():
        dct = data[key]
        buy, sale = (Decimal(dct[i]).quantize(TWOPLACES) for i in ('buy', 'sale'))
        check_and_write(currency, source, sale, buy)


@shared_task
def parse_fixer():
    url = 'http://data.fixer.io/api/latest?access_key=9373480f27e621ad817348c5dff35ed3'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()['rates']

    source = 4
    currency_map = {
        'USD': 1,
        'EUR': 2,
    }
    UAH = Decimal(data['UAH']).quantize(TWOPLACES)  # EUR -> UAH

    for key, currency in currency_map.items():
        nominal = UAH/Decimal(data[key]).quantize(TWOPLACES)
        check_and_write(currency, source, nominal, nominal)


@shared_task
def parse_oschadbank():
    url = 'https://www.oschadbank.ua/ua/private/currency'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.find_all('td', attrs={'class': 'text-right'})
    array = [i.text for i in rows]

    source = 5
    allow_currency = {
        '840': 1,
        '978': 2,
    }

    for key, currency in allow_currency.items():
        currency_index = array.index(key)
        buy, sell = (Decimal(array[currency_index+4+i]).quantize(TWOPLACES) for i in range(2))
        check_and_write(currency, source, buy, sell)


@shared_task
def parse_prostobank():
    html_doc = requests.get('https://www.prostobank.ua/spravochniki/kursy_valyut')
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    rows = soup.find_all('p')
    array = [i.text for i in rows]

    def conver_to_decimal(x):
        return Decimal(x.replace(' ', '').replace(',', '.')).quantize(TWOPLACES)
    # 18, 19, 25, 26 elements in bsoup list
    usd_buy, usd_sele, eur_buy, eur_sele = (conver_to_decimal(array[i]) for i in (18, 19, 25, 26))

    source = 6

    check_and_write(1, source, usd_buy, usd_sele)
    check_and_write(2, source, eur_buy, eur_sele)


@shared_task
def parse_minfin():
    source = 7
    for num, var in enumerate(('usd', 'eur',), start=1):
        html = requests.get(f'https://minfin.com.ua/currency/banks/{var}')
        soup = BeautifulSoup(html.text, 'html.parser')
        rows = soup.find('td', {'class': 'mfm-text-nowrap', 'data-title': 'Средний курс'})

        buy, sale = (Decimal(str(i.string).replace('\n', '')).quantize(TWOPLACES) for i in list(rows)[::2])
        check_and_write(num, source, buy, sale)


@shared_task
def parse_ukrgasbank():
    source = 8
    html_doc = requests.get('https://ukrgasbank.com/kurs/')
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    rows = soup.find_all('td', {'class': 'val'})

    usd_buy, usd_sele, eur_buy, eur_sele = [Decimal(i.text).quantize(TWOPLACES)/100 for i in rows[:2] + rows[3:5]]
    check_and_write(1, source, usd_buy, usd_sele)
    check_and_write(2, source, eur_buy, eur_sele)


@shared_task
def parse_pumb():
    source = 9

    html_doc = requests.get('https://about.pumb.ua/info/currency_converter')
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    for currency, name in enumerate(('USD', 'EUR'), start=1):
        rows = soup.find('td', string=name)
        array = []
        for i in range(7):
            rows = rows.next
            if i in (3, 6):
                array.append(Decimal(rows).quantize(TWOPLACES))
        buy, sele = array
        check_and_write(currency, source, buy, sele)


@shared_task
def parse_pravex():
    source = 10

    html_doc = requests.get('https://www.pravex.com.ua/kursy-valyut')
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    rows = soup.find_all('div', {'class': 'value'})

    usd_buy, usd_sele, eur_buy, eur_sele = (Decimal(i.text).quantize(TWOPLACES) for i in rows[2:6])

    check_and_write(1, source, usd_buy, usd_sele)
    check_and_write(2, source, eur_buy, eur_sele)


@shared_task
def parse_alpha():
    source = 11

    html_doc = requests.get('https://alfabank.ua/currency-exchange')
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    rows = soup.find_all('span', {'class': 'rate-number'})
    usd_buy, usd_sale, eur_buy, eur_sale = [float(i.text) for i in rows][:4]

    check_and_write(1, source, usd_buy, usd_sale)
    check_and_write(2, source, eur_buy, eur_sale)


@shared_task
def send_xml_to_all_async():
    send_xml_to_all()
