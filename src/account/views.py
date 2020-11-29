import os
import shutil

from currency.settings import MEDIA_ROOT

from account.forms import AvatarForm, UserRegistrationForm, UserPassChenge
from account.models import Avatar, User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView, LoginView
from django.views.generic import CreateView, UpdateView, View, ListView, DeleteView
from django.http import HttpResponseRedirect


def set_active_avatar(model, user, avatar):
    current_user_avatars = model.objects.filter(user=user)
    for i in current_user_avatars:
        i.active_avatar = None
        i.save()
    set_active_avatar = current_user_avatars.get(id=avatar)
    set_active_avatar.active_avatar = True
    set_active_avatar.save()


class MyProfile(LoginRequiredMixin, UpdateView):
    fields = ('first_name', 'last_name')
    success_url = reverse_lazy('account:myprofile')

    def get_context_data(self, **kwargs):
        kwargs['avatar'] = Avatar.objects.filter(user=self.request.user, active_avatar=True).last()
        return super().get_context_data(**kwargs)

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


class AvatarList(ListView):
    def get_queryset(self):
        breakpoint()
        return self.request.user.avatar_set.all()


class SetActiveAvatar(View):
    def dispatch(self, request, *args, **kwargs):
        set_active_avatar(Avatar, self.request.user, kwargs['pk'])
        return redirect('account:myprofile')


class DeleteAvatar(DeleteView):
    def get_object(self):
        avatar_id = self.kwargs.get('pk')
        return get_object_or_404(Avatar, id=avatar_id)

    def post(self, request, *args, **kwargs):
        delete_object = Avatar.objects.get(id=kwargs['pk'])
        delete_path = delete_object.file_path.path
        os.remove(delete_path)
        return self.delete(request, *args, **kwargs)

    success_url = reverse_lazy('account:avatar_list')


class DeleteAllAvatar(DeleteView):
    queryset = User.objects.all()
    template_name = 'account/deleteall_avatars_confirm.html'

    def delete(self, request, *args, **kwargs):
        avatar_owner = self.get_queryset().get(id=self.kwargs['pk'])
        all_user_avatars = avatar_owner.avatar_set.all()
        del_dir = MEDIA_ROOT + '/' + str(self.kwargs['pk'])
        all_user_avatars.delete()
        shutil.rmtree(del_dir)
        return HttpResponseRedirect(reverse_lazy('account:avatar_list'))
