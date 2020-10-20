from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView


class MyProfile(LoginRequiredMixin, UpdateView):
    fields = ('first_name', 'last_name')
    success_url = reverse_lazy('account:myprofile')

    def get_object(self, queryset=None):
        return self.request.user
