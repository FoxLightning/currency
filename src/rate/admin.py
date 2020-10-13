from django.contrib import admin

from .models import ContactUs, Feedback, Rate


admin.site.register(Rate)
admin.site.register(ContactUs)
admin.site.register(Feedback)
