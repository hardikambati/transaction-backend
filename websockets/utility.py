# entrypoint to send messages to users

from django.contrib.auth import get_user_model

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from accounts.models import Connections


User = get_user_model()


def send_message_to_channel(user_id: str, message: dict) -> bool:
    """
    sends transaction update message, to connected user
    accepts
    - user_id
    - message
    """

    channel_layer = get_channel_layer()
    
    connection_instances = Connections.objects.filter(
        user=User.objects.get(id=user_id)
    )

    if not connection_instances.exists():
        print(f'[INFO] connection not found')
        return False

    connection = connection_instances.first()

    try:
        async_to_sync(channel_layer.send)(
            connection.channel_id,
            {
                'type': 'transaction_update',
                'message': message
            }
        )
        return True
    except Exception as e:
        print(f'[INFO] error in sending message')
        print(f'[INFO] {e}')
        return False