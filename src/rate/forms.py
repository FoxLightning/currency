from django import forms

from rate import choices

from .models import Subscription
OPTIONS = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
           (6, 6), (7, 7), (8, 8), (9, 9), (10, 10),)


class SubscriptionForm(forms.Form):
    banks = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=choices.SOURCE_CHOICES)
