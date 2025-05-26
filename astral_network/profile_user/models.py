from django.db import models

from auth_user.models import AuthUser


class Gender(models.Model):
    gender = models.CharField(max_length=7)

    def __str__(self):
        return f"{self.gender}"


class ProfileUser(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    about_yourself = models.TextField(max_length=1500, blank=True, null=True)
    status = models.CharField(max_length=150, blank=True, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.user}"

