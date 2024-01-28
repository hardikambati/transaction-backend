from django.db import models
from django.contrib.auth import get_user_model

# custom
from utils.helpers import generate_key


User = get_user_model()


TRANSACTION_STATUS = (
    ('scheduled', 'scheduled'),
    ('started', 'started'),
    ('verifying', 'verifying'),
    ('transacting', 'transacting'),
    ('completed', 'completed'),
    ('closed', 'closed'),
    ('failed', 'failed'),
)


def _generate_txn_id():
    key = generate_key(30)
    while Transaction.objects.filter(txn_id=key).exists():
        key = generate_key(30)
    return key


class Transaction(models.Model):

    name       = models.CharField(max_length=365)
    user       = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    txn_id     = models.CharField(max_length=36, default=_generate_txn_id, unique=True)
    status     = models.CharField(max_length=36, choices=TRANSACTION_STATUS, default='scheduled')
    metadata   = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    