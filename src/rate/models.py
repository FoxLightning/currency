from django.db import models


class Rate(models.Model):
    CURRENCY_CHOICES = (
        (1, 'USD'),
        (2, 'UER'),
    )

    SOURCE_CHOICES = (
        (1, 'PrivatBank'),
        (2, 'MonoBank'),
        (3, 'Vkurse'),
        (4, 'fixer'),
        (5, 'oschadbank'),
        (6, 'prostobank'),
        (7, 'minfin'),
        (8, 'ukrgazbank'),
        (9, 'pumb'),
        (10, 'pravex'),
        (11, 'alphabank'),
    )

    currency = models.PositiveSmallIntegerField(choices=CURRENCY_CHOICES)
    source = models.PositiveSmallIntegerField(choices=SOURCE_CHOICES)
    buy = models.DecimalField(max_digits=6, decimal_places=2)
    sale = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
