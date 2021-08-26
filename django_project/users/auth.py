from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.http import HttpRequest


class CustomAuthBackend(BaseBackend):
    """
    Custom Authentication Backend
    """
    def authenticate(self, request: HttpRequest, username: str = None, password: str = None):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass

        return None

    def get_user(self, user_id: int):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
