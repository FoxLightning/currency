from django.db.models import Avg
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

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


def feedback(request):

    form = FeedbackForm(request.POST)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            result = form.cleaned_data.get('rating')
            Feedback.objects.create(rating=int(result))
            return redirect('rate:showrating')
    context = {'form': form}
    return render(request, 'rate/feedback_form.html', context=context)


def showrating(request):
    rating = round(Feedback.objects.all().aggregate(Avg('rating'))['rating__avg'], 2)
    context = {'rating': rating}
    return render(request, 'rate/rating.html', context=context)
