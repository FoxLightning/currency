from django.db.models import Avg
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

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
    fields = ('rating',)

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if self.request.user.id in [i.user_id for i in Feedback.objects.all()]:
            self.error = 'you are allready voted'
            return redirect('rate:error')
        else:
            Feedback.objects.create(
                rating=form.cleaned_data['rating'],
                user_id=self.request.user.id,
                )
            return redirect('rate:showrating')


class FeedbackShowView(TemplateView):
    template_name = 'rate/feedback_list.html'

    def get_context_data(self, **kwargs):
        kwargs['avg'] = Feedback.objects.all().aggregate(Avg('rating'))['rating__avg']
        kwargs['count'] = Feedback.objects.all().count()
        return super().get_context_data(**kwargs)


class ErrorView(TemplateView):
    template_name = 'rate/error.html'

    def get_context_data(self, **kwargs):
        kwargs['error'] = 'You are allready voted'
        return super().get_context_data(**kwargs)
