from decimal import Decimal


TWOPLACES = Decimal(10) ** -2

CURRENCY_USD = 1
CURRENCY_EUR = 2

CURRENCY_CHOICES = (
    (1, 'USD'),
    (2, 'UER'),
)

PRIVATBANK = 1
MONOBANK = 2
VKURSE = 3
FIXER = 4
OSCHADBANK = 5
PROSTOBANK = 6
MINFIN = 7
UKRGAZBANK = 8
PUMB = 9
PRAVEX = 10
ALPHABANK = 11

SOURCE_CHOICES = (
    (PRIVATBANK, 'PrivatBank'),
    (MONOBANK, 'MonoBank'),
    (VKURSE, 'Vkurse'),
    (FIXER, 'Fixer'),
    (OSCHADBANK, 'Oschadbank'),
    (PROSTOBANK, 'Prostobank'),
    (MINFIN, 'Minfin'),
    (PROSTOBANK, 'Ukrgazbank'),
    (PUMB, 'Pumb'),
    (PRAVEX, 'Pravex'),
    (ALPHABANK, 'Alphabank'),
)

OPTIONS = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
)
