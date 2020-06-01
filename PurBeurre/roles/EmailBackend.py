"""This file is used to customize the authentication process"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """
    The purpose of this class and its function is to
    allow the authentication using the email
    instead of the username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """It will accept the provided email as a username"""
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
