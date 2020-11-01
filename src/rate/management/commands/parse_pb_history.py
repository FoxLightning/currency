import sys
from datetime import date, datetime, timedelta
from decimal import Decimal
from time import sleep

from django.core.management.base import BaseCommand

from rate.choices import TWOPLACES
from rate.models import Rate

import requests

from tqdm import tqdm


def rate_exist(date) -> bool:
    rate1 = Rate.objects.filter(source=1, currency=1, created=date).last()
    rate2 = Rate.objects.filter(source=1, currency=2, created=date).last()
    return True if rate1 or rate2 else False


def parse_privatbank_legacy(date):
    # check before query up performance when rate is exist
    if rate_exist(date):
        sys.stdout.write('rate allready exist')
        return None
    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date.strftime("%d.%m.%Y")}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    source = 1  # 1 = PrivatBank
    currency_map = {
        'USD': 1,
        'EUR': 2,
    }

    for row in filter(lambda x: x.get('currency') in currency_map.keys(), data["exchangeRate"][1:]):
        buy, sale = (row.get(i) for i in ('purchaseRate', 'saleRate',))
        if not (buy or sale):
            sys.stdout.write('Rate not exist in source')
            continue
        buy, sale = (Decimal(i).quantize(TWOPLACES) for i in (buy, sale))
        currency = currency_map[row['currency']]
        # sys.stdout.write(source, currency, buy, sale, f'{date} 00:00')
        Rate.objects.create(
            currency=currency,
            source=source,
            sale=sale,
            buy=buy,
            created=f'{date} 00:00:00',
        )


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

    total_iterations = (end_date - start_date).days//step

    for i in tqdm(range(total_iterations)):
        # Except 503
        while True:
            try:
                parse_privatbank_legacy(start_date)
                break
            except requests.exceptions.HTTPError:
                sleep(10)
                continue
        start_date += delta_time


class Command(BaseCommand):
    help = 'Parse legacy rates in privat bank'  # noqa

    def add_arguments(self, parser):
        parser.add_argument('-b', '--begin', type=str, help='Start date dd.mm.yyyy')
        parser.add_argument('-e', '--end', type=str, help='Finish date dd.mm.yyyy, default: today')
        parser.add_argument('-s', '--step', type=int, help='Step *d, default: 1 day')

    def handle(self, *args, **kwargs):
        step = kwargs['step'] if kwargs['step'] else 1
        start = kwargs['begin']
        if not start:
            return 'Error: -b --begin must be not None'
        period(
            start,
            kwargs['end'],
            step,
        )
