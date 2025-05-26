from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from auth_user.backends import AuthBackend
from auth_user.models import AuthUser


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label='first name', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='last name', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='e-mail', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='repeat password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = AuthUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')



class LoginForm(AuthenticationForm):
    connection_code = forms.CharField(
        label='Connection Code',
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)

    def clean(self):
        connection_code = self.cleaned_data.get('connection_code')
        password = self.cleaned_data.get('password')

        if connection_code and password:
            self.user_cache = AuthBackend.authenticate(
                self,
                connection_code=connection_code,
                password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Please enter a correct connection code and password."
                )
            elif not self.user_cache.is_verified:
                raise forms.ValidationError(
                    "Please verify your email before logging in."
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data