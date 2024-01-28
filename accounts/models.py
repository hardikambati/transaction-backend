from django.db import models
from django.contrib.auth import get_user_model

# custom
from utils.helpers import generate_key


User = get_user_model()


def _generate_access_token():
    token = generate_key(size=35)
    while AccessToken.objects.filter(value=token).exists():
        token = generate_key(size=35)
    return token


class AccessToken(models.Model):
    """
    AccessToken for microservices
    """

    name       = models.CharField(max_length=36)
    value      = models.CharField(max_length=36, default=_generate_access_token, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active  = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class Connections(models.Model):
    """
    Connections for channels
    """

    user       = models.ForeignKey(to=User, on_delete=models.CASCADE)
    channel_id = models.CharField(max_length=299)

    def __str__(self):
        return self.user.username
