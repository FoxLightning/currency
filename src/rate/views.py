from django.db.models import Avg
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from django.contrib.auth.models import User

from .forms import FeedbackForm
from .models import ContactUs, Feedback, Rate
from .tasks import send_email_async


class RateListView(ListView):
    queryset = Rate.objects.all().order_by('sale')


class ContactUsListView(ListView):
    queryset = ContactUs.objects.all()


class CreateContactUsView(CreateView):
    success_url = reverse_lazy('index')
    model = ContactUs
    fields = ('email', 'subject', 'massage')

    def form_valid(self, form):
        if form.is_valid():
            data = form.cleaned_data
            send_email_async.delay(data['subject'], f"sander:{data['email']}\n{data['massage']}")
        return super().form_valid(form)


class FeedbackView(CreateView):
    success_url = reverse_lazy('index')
    model = Feedback
    fields = ('rating', 'user_id')

    # def form_valid(self, form):
    #     if form.is_valid():
    #         FeedbackForm.objects.create(rating=form.rating, user_id=user.id)
    #     return super().form_valid(form)


class FeedbackShowView(ListView):
    queryset = Feedback.objects.all()


def showrating(request):
    queryset = Feedback.objects.all()
    rating = round(queryset.aggregate(Avg('rating'))['rating__avg'], 2)
    count_rate = queryset.count()
    context = {
        'rating': rating,
        'count': count_rate,
        }
    return render(request, 'rate/rating.html', context=context)
