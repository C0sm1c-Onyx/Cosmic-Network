from django.db.models.signals import post_save
from django.dispatch import receiver
from interaction_core.models import Friends

from datetime import datetime


@receiver(post_save, sender=Friends)
def create_unique_friend_code(sender, instance, created, **kwargs):
    if created:
        unique_code = abs(
            hash(instance.user.last_name) + hash(instance.friend.last_name) + int(str(datetime.now().timestamp())[11:])
        )

        instance.friend_unique_code = unique_code
        instance.save()