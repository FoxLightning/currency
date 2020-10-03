from django.db import models


class Rate(models.Model):
    CURRENCY_CHOICES = (
        (1, 'USD'),
        (2, 'UER'),
    )

    SOURCE_CHOICES = (
        (1, 'PrivatBank'),
    )

    currency = models.PositiveSmallIntegerField(choices=CURRENCY_CHOICES)
    source = models.PositiveSmallIntegerField(choices=SOURCE_CHOICES)
    buy = models.DecimalField(max_digits=6, decimal_places=2)
    sale = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
