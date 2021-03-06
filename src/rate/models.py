from django.db import models
from django.utils.timezone import now

from . import choices


class Rate(models.Model):
    currency = models.PositiveSmallIntegerField(choices=choices.CURRENCY_CHOICES, verbose_name='Currency')
    source = models.PositiveSmallIntegerField(choices=choices.SOURCE_CHOICES, verbose_name='Bank')
    buy = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Buy')
    sale = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Sale')
    created = models.DateTimeField(verbose_name='Update time', default=now)

    def __str__(self):
        # max recursion depth if i try to use get_source_display
        # по индексу обращаться тоже не особо круто, TODO довести до ума
        return f"{choices.SOURCE_CHOICES[self.source-1][0]} {choices.CURRENCY_CHOICES[self.currency-1]}"

    class Meta:
        verbose_name = "Rate"
        verbose_name_plural = "Rates"
        permissions = [
            ("full_edit", "full edit")
        ]


class ContactUs(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=128)
    massage = models.TextField()

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Massage"
        verbose_name_plural = "Massages"


class Feedback(models.Model):
    rating = models.PositiveSmallIntegerField(choices=choices.OPTIONS)
    user = models.OneToOneField('account.User', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.rating)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"


class Subscription(models.Model):
    banks = models.PositiveSmallIntegerField(choices=choices.SOURCE_CHOICES)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
