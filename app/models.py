from django.contrib.auth.models import User
from django.db import models
from django.core.cache import cache
from django.utils import timezone


class Content(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=10000)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    music = models.FileField(upload_to='musics/%Y/%m/%d', blank=True, null=True)
    video = models.FileField(upload_to='videos/%Y/%m/%d', blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    status = models.TextField(max_length=100, null=True, blank=True)
    birthdate = models.DateField(blank=True, null=True)
    sex = models.ForeignKey('Gender', on_delete=models.PROTECT, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def is_online(self, user_id):
        last_seen = cache.get(f'last-seen-{user_id}')
        if last_seen and timezone.now() < last_seen + timezone.timedelta(seconds=300):
            return True
        return False


class Followers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')


class Likes(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)


class Gender(models.Model):
    genders = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return self.genders


class Messanger(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    datetime = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=10000)
    image = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    video = models.FileField(upload_to='videos/%Y/%m/%d', blank=True)
    music = models.FileField(upload_to='musics/%Y/%m/%d', blank=True)


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos/%Y/%m/%d')


class Music(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music = models.FileField(upload_to='musics/%Y/%m/%d')


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.FileField(upload_to='photos/%Y/%m/%d')