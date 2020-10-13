from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, View

from .forms import SubscriptionForm
from .models import ContactUs, Feedback, Rate, Subscription
from .tasks import send_email_async
from .utils import create_xml, last_rates


class RateListView(ListView):
    queryset = Rate.objects.all().order_by('-id')


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
        if Feedback.objects.filter(user_id=self.request.user.id).exists():
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


class SubListView(ListView):
    queryset = None
    pk_url_kwarg = ('pk', 'id')

    def get_queryset(self):
        if self.queryset is None:
            queryset = Subscription.objects.filter(user=self.request.user)
        return queryset


def subdel(request, pk):
    Subscription.objects.filter(id=pk, user=request.user).delete()
    return redirect('rate:sublist')


class AddSubView(CreateView):
    success_url = reverse_lazy('rate:sublist')
    model = Subscription
    fields = ('banks',)
    template_name = 'rate/addsubscription_create.html'

    def form_valid(self, form):
        bunks = form.cleaned_data['banks']
        self.model.objects.create(
            user=self.request.user,
            banks=bunks,
            )
        return redirect('rate:sublist')


def addsub(request):
    form = SubscriptionForm(request.POST or None)
    context = {'form': form}
    if request.POST:
        if form.is_valid():
            user = request.user
            choices = form.cleaned_data.get("banks")
            sub_banks = [i.banks for i in Subscription.objects.filter(user=user)]
            for bank in map(int, choices):
                if bank not in sub_banks:
                    Subscription.objects.create(
                        user=user,
                        banks=bank,
                    )
        return redirect('rate:sublist')
    return render(
        request,
        'rate/addsubscription_create.html',
        context=context
    )


class LatestRates(View):
    def get(self, request):
        context = {'rate_list': last_rates()}
        return render(request, 'rate/latest-rates.html', context=context)


class DownloadLatestRates(View):
    def get(self, request):
        file = create_xml(last_rates())
        response = HttpResponse(file.getvalue(), content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename=rate_list.xml'
        return response


class DownloadAllRates(View):
    def get(self, request):
        file = create_xml(Rate.objects.all())
        response = HttpResponse(file.getvalue(), content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename=rate_list.xml'
        return response
