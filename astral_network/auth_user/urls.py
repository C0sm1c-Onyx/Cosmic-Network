from django.urls import path

from auth_user.views import (
    LoginUser, RegisterUser, logout_user, activate_email,
    pre_activate_user,
)


urlpatterns = [
    path('auth/login/', LoginUser.as_view(), name='login'),
    path('auth/register/', RegisterUser.as_view(), name='register'),
    path('auth/pre-activate/', pre_activate_user, name='pre-activate'),
    path('auth/email-verification/<str:uidb64>/<str:token>/', activate_email, name='verify'),

    path('logout/', logout_user, name='logout'),
]