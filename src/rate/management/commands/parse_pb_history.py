from decimal import Decimal

from django.core.management.base import BaseCommand

from rate.models import Rate

import requests

from datetime import datetime, date, timedelta


import pytz

TWOPLACES = Decimal(10) ** -2


def check_and_write_legacy(currency, source, sale, buy, date):
    rate = Rate.objects.filter(source=source, currency=currency, created=date).last()
    if not rate:
        Rate.objects.create(
            currency=currency,
            source=source,
            sale=sale,
            buy=buy,
            created=date,
        )


def parse_privatbank_legacy(date):
    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date.strftime("%d.%m.%Y")}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    source = 1  # 1 = PrivatBank
    currency_map = {
        'USD': 1,
        'EUR': 2,
    }

    for row in filter(lambda x: x['currency'] in currency_map.keys(), data["exchangeRate"][1:]):
        buy, sale = (Decimal(row[i]).quantize(TWOPLACES) for i in ('purchaseRate', 'saleRate',))
        currency = currency_map[row['currency']]
        print(source, currency, buy, sale, f'{date} 00:00')
        check_and_write_legacy(currency, source, sale, buy, f'{date} 00:00:00')


def period(start, end=None, step=1):
    """
    start format: dd.mm.yyyy :str
    end format: dd.mm.yyyy (default = today) :str
    step format: *d (default = 1 day) :str or int
    """
    sday, smonth, syear = map(int, start.split('.'))
    start_date = date(syear, smonth, sday)

    if end:
        eday, emonth, eyear = map(int, end.split('.'))
        end_date = start_date = datetime(eyear, emonth, eday)
    else:
        end_date = date.today()

    delta_time = timedelta(days=step)

    while start_date < end_date:
        parse_privatbank_legacy(start_date)
        start_date += delta_time


class Command(BaseCommand):
    help = 'Parse legacy rates in privat bank'  # noqa

    def add_arguments(self, parser):
        parser.add_argument('-b', '--begin', type=str, help='Start date dd.mm.yyyy')
        parser.add_argument('-e', '--end', type=str, help='Finish date dd.mm.yyyy, default: today')
        parser.add_argument('-s', '--step', type=int, help='Step *d, default: 1 day')

    def handle(self, *args, **kwargs):
        step = kwargs['step']
        start = kwargs['begin']
        if not start:
            return 'Error: -b --begin must be not None'
        period(
            start,
            kwargs['end'],
            step if step else 1,
        )
