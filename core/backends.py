from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class EmailBackend(object):
    def authenticate(self, username=None, password=None, request=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            raise ValidationError("Wrong email or password")
        else:
            if getattr(user, 'is_active', False) and  user.check_password(password):
                return user
        raise ValidationError("Wrong email or password")


    def get_user(self, user_id):
       try:
          return User.objects.get(pk=user_id)
       except User.DoesNotExist:
          return None
