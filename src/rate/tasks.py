from decimal import Decimal

from celery import shared_task

import requests


@shared_task
def parse_privatbank():
    from rate.models import Rate

    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)

    # raise error if response.status_code != 200
    response.raise_for_status()

    data = response.json()
    source = 1
    currency_map = {
        'USD': 1,
        'EUR': 2,
    }

    TWOPLACES = Decimal(10) ** -2

    for row in data:
        if row['ccy'] in currency_map:
            buy = Decimal(row['buy']).quantize(TWOPLACES)
            sale = Decimal(row['sale']).quantize(TWOPLACES)
            currency = currency_map[row['ccy']]

            last_rate = Rate.objects.filter(source=source, currency=currency).last()
            # save rate if record was not found or sale or buy was changed
            if last_rate is None or buy != last_rate.buy or sale != last_rate.sale:
                Rate.objects.create(
                    currency=currency,
                    source=source,
                    sale=sale,
                    buy=buy,
                )
