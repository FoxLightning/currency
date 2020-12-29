from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import redirect, render, render_to_response
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView, View

from django_filters.views import FilterView

from rate.filters import RateFilter

from .forms import SubscriptionForm
from .models import ContactUs, Feedback, Rate, Subscription
from .tasks import send_email_async
from .utils import create_xml, last_rates


class RateListView(FilterView):
    queryset = Rate.objects.all()
    paginate_by = 10
    filterset_class = RateFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        for key, value in self.request.GET.items():
            context[key] = value
        context['GET_PARAMS'] = '&'.join(
            f'{key}={value}'
            for key, value in self.request.GET.items()
            if key != 'page'
        )
        context['object_count'] = context['object_list'].count()
        return context


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


# TODO rework
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


# TODO rework
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


class DeleteRate(DeleteView):
    queryset = Rate.objects.all()
    success_url = reverse_lazy('rate:list')

    def delete(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().delete(self, request, *args, **kwargs)


class UpdateRate(UpdateView):
    model = Rate
    success_url = reverse_lazy('rate:list')
    fields = ['currency', 'source', 'buy', 'sale', 'created']

    def form_valid(self, form):
        if self.request.user.is_superuser:
            return super().form_valid(form)


def handler404(request, exception):
    response = render_to_response('error/404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('/error/500.html', {})
    response.status_code = 500
    return render(response, 'rate/500.html', locals())
