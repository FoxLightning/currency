from django.contrib import admin

from .models import ContactUs, Feedback, Rate, Subscription


admin.site.register(Rate)
admin.site.register(ContactUs)
admin.site.register(Feedback)
admin.site.register(Subscription)
