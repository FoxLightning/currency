from account.models import User
from account.tasks import send_sign_up_email

from django import forms


class UserLoginForm(forms.ModelForm):
    model = User

    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )

    def clean(self):
        cleaned_data: dict = super().clean()
        if not self.errors:  # additional checks if form does not have anu errors
            # check that both passwords are equal
            if cleaned_data['password1'] != cleaned_data['password2']:
                raise forms.ValidationError("Passwords do not match.")
                # self.add_error('password1', 'Passwords do not match.')
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            self.add_error('email', 'User already exists.')
        return email

    def save(self, commit=True):
        instance: User = super().save(commit=False)
        instance.is_active = False
        # instance.password = self.cleaned_data['password1']  WRONG
        instance.set_password(self.cleaned_data['password1'])
        instance.save()
        # send_sign_up_email.delay(instance.id)
        send_sign_up_email.apply_async(args=[instance.id], countdown=5)
        return instance


class UserUpdatePassword(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = (
            'password1',
            'password2',
        )
