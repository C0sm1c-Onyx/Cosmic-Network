from django.core.exceptions import ObjectDoesNotExist

from auth_user.models import AuthUser


class AuthBackend:
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def get_user(self, user_id):
        try:
            return AuthUser.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None

    def authenticate(self, connection_code, password):
        try:
            user = AuthUser.objects.get(connection_code=connection_code)
        except ObjectDoesNotExist:
            return None

        return user if user.check_password(password) else None