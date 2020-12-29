import os

from account.forms import AvatarForm, UserPassChenge, UserRegistrationForm
from account.models import Avatar, User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View


def set_active_avatar(model, user, avatar):
    model.objects.filter(user=user, active_avatar=True).update(active_avatar=None)
    model.objects.filter(user=user).filter(id=avatar).update(active_avatar=True)


class MyProfile(LoginRequiredMixin, UpdateView):
    fields = ('first_name', 'last_name')
    success_url = reverse_lazy('account:myprofile')

    def get_context_data(self, **kwargs):
        kwargs['avatar'] = Avatar.objects.filter(user=self.request.user, active_avatar=True).last()
        return super().get_context_data(**kwargs)

    def get_object(self, queryset=None):
        return self.request.user


class SignOut(LoginRequiredMixin, LogoutView):
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


class UserPasswordChange(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserPassChenge
    template_name = os.path.join('account', 'user_password_change.html')
    success_url = reverse_lazy('index')


class CreateUserAvatar(LoginRequiredMixin, CreateView):
    model = Avatar
    form_class = AvatarForm
    success_url = reverse_lazy('account:avatar_list')

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['request'] = self.request
        return form_kwargs

    def get_success_url(self):
        set_active_avatar(model=Avatar, user=self.request.user, avatar=Avatar.objects.last().id)
        return super().get_success_url()


class AvatarList(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return self.request.user.avatar_set.all()


class SetActiveAvatar(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        set_active_avatar(Avatar, self.request.user, kwargs['pk'])
        return redirect('account:myprofile')


class DeleteAvatar(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('account:avatar_list')

    def get_object(self):
        avatar_id = self.kwargs.get('pk')
        avatar = get_object_or_404(Avatar, id=avatar_id)
        if avatar.user.id == self.request.user.id:
            return avatar


class DeleteAllAvatar(LoginRequiredMixin, DeleteView):
    queryset = User.objects.all()
    template_name = 'account/deleteall_avatars_confirm.html'
    success_url = reverse_lazy('account:avatar_list')

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        all_user_avatars = user.avatar_set.all()
        all_user_avatars.delete()
        return HttpResponseRedirect(self.success_url)
