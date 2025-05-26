from django.db.models.signals import post_migrate
from django.dispatch import receiver

from profile_user.models import Gender


@receiver(post_migrate)
def create_gender(**kwargs):
    if not Gender.objects.all():
        Gender.objects.bulk_create([
            Gender(id=1, gender='Man'),
            Gender(id=2, gender='Woman'),
        ])