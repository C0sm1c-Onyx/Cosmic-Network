from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from loguru import logger

from auth_user.models import AuthUser
from auth_user.utils import get_connection_code
from profile_user.models import ProfileUser


@receiver(post_save, sender=AuthUser)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        try:
            connection_code = get_connection_code(instance.first_name, instance.last_name)
            instance.connection_code = connection_code
            instance.save()

            ProfileUser.objects.create(user=instance)

            uid = urlsafe_base64_encode(force_bytes(instance.pk))
            token = default_token_generator.make_token(instance)

            mail_subject = 'Activate your account'
            activation_link = f"http://{settings.ALLOWED_HOSTS[0]}:8000/auth/email-verification/{uid}/{token}/"
            message = f"Hi {instance.email},\n\nPlease click on the link to activate your account:\n{activation_link}\n\nСopy your connection code and save it for authorization: {connection_code}"
            send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [instance.email], fail_silently=False)

        except Exception as err:
            logger.error(err)