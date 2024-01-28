from django.db.models.signals import (
    post_save,
)
from django import dispatch
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token


User = get_user_model()


@dispatch.receiver(post_save, sender=User)
def create_auth_token(created, instance, **kwargs):
    """
    create's a unique token when a user is created
    """

    if created:
        # create a unique token object for registered user
        Token.objects.create(
            user=instance
        )