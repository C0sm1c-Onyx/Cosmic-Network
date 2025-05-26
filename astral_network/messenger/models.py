from django.db import models

from auth_user.models import AuthUser


class Chat(models.Model):
    unique_chat_code = models.CharField(max_length=1000)
    user1 = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='user2')

    def __str__(self):
        return f"{self.unique_chat_code}"


class Message(models.Model):
    sender = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=22500)
    sending_time = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sender}: {self.message}"