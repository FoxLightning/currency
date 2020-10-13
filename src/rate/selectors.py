from time import sleep

from django.core.cache import cache

from rate import choices
from rate.models import Rate


def get_latest_rates():
    key = str(get_latest_rates.__name__)
    # TO CACHE
    if key in cache:
        rates = cache.get(key)
    else:
        sleep(5)
        rates = []
        for source_int, _ in choices.SOURCE_CHOICES:
            for currency_int, _ in choices.CURRENCY_CHOICES:
                rate = Rate.objects \
                    .filter(source=source_int, currency=currency_int) \
                    .order_by('created') \
                    .last()

                # if rate is not None:
                if rate:
                    rates.append(rate)
        cache.set(key, rates, 120)
        # CACHE

    return rates
