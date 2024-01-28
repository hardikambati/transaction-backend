import os

# env

RABBITMQ_SERVER_URL = os.environ.get('RABBITMQ_SERVER_URL')
SERVICE01_QUEUE_NAME = os.environ.get('SERVICE01_QUEUE_NAME')

# helpers

TRANSACTION_STATUS = [
    'scheduled',
    'started',
    'verifying',
    'transacting',
    'completed',
    'closed',
    'failed',
]