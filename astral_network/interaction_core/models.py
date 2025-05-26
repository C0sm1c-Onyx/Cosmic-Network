from django.db import models

from auth_user.models import AuthUser


class Music(models.Model):
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    music = models.FileField(upload_to='music/%Y/%m/%d', blank=True, null=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} {self.title}"


class Friends(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='friend')
    status = models.BooleanField(blank=True, default=False)
    friend_unique_code = models.CharField(max_length=1000, blank=True, default=False)

    def __str__(self):
        return f"{self.friend}"