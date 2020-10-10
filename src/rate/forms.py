from django import forms

from rate import choices

from .models import Subscription
OPTIONS = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
           (6, 6), (7, 7), (8, 8), (9, 9), (10, 10),)


class FeedbackForm(forms.Form):
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=OPTIONS)


# class SubscriptionForm(forms.Form):
#     sources = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=choices.SOURCE_CHOICES)

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['user', 'banks']
        widgets = {
            'Ingredient': forms.CheckboxSelectMultiple,
        }
