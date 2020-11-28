import os

from account.forms import UserRegistrationForm
from account.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, View


class MyProfile(LoginRequiredMixin, UpdateView):
    fields = ('first_name', 'last_name')
    success_url = reverse_lazy('account:myprofile')

    def get_object(self, queryset=None):
        return self.request.user


class SignOut(LogoutView):
    success_url = reverse_lazy('index')
    template_name = os.path.join('account', 'user_sign_out.html')


class SignIn(LoginView):
    success_url = reverse_lazy('index')
    template_name = os.path.join('account', 'user_sign_in.html')


class SignUp(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('index')
    template_name = os.path.join('account', 'user_sign_up.html')


class ActivateUser(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        if user.is_active:
            pass
        else:
            user.is_active = True
            user.save(update_fields=('is_active', ))
        return redirect('index')


class UserPasswordChange(UpdateView):
    model = User
    form_class = UserPassChenge
    template_name = os.path.join('account', 'user_password_change.html')
    success_url = reverse_lazy('index')
