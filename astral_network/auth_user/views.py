from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import JsonResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from auth_user.forms import UserRegisterForm, LoginForm
from auth_user.models import AuthUser


class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'auth_user/register.html'

    def get_success_url(self):
        return reverse_lazy('pre-activate')


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'auth_user/login.html'

    def get_success_url(self):
        return reverse_lazy('profile', args=(self.request.user.id,))


def logout_user(request):
    logout(request)
    return redirect('login')


def pre_activate_user(request):
    return JsonResponse(
        {
            "Warning!": "go to the e-mail you specified during registration and click on the activation link that we sent - it is mandatory to be able to use the site."
        }
    )


def activate_email(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = AuthUser.objects.get(pk=uid)

    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.is_active = True
        user.save()
        return redirect('login')

    return JsonResponse({"ERROR 404": "Fatal connection... :/"})


