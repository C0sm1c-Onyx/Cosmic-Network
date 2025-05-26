from django.db import models
from django.contrib.auth.models import AbstractUser

from auth_user.managers import UserManager


class AuthUser(AbstractUser):
    username = models.CharField('username', max_length=1, blank=True, null=True)
    connection_code = models.CharField('unique_code', max_length=50, blank=True)
    first_name = models.CharField('first_name', max_length=16)
    last_name = models.CharField('last_name', max_length=16)
    email = models.EmailField('email', max_length=30, unique=True)
    date_joined = models.DateTimeField('date_joined', auto_now_add=True)
    is_active = models.BooleanField('is_active', default=False)
    is_staff = models.BooleanField('is_staff', default=False)
    is_verified = models.BooleanField('is_verified', default=False)

    object = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta(AbstractUser.Meta):
        verbose_name = 'auth_user'
        verbose_name_plural = 'auth_users'
        unique_together = ('email',)

        swappable = "AUTH_USER_MODEL"

    def __str__(self):
        return f"{self.username}"
