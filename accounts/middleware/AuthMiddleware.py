from urllib.parse import parse_qs
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

# 3rd party
import jwt
from channels.db import database_sync_to_async


User = get_user_model()


@database_sync_to_async
def returnUser(user_id: str):
    try:
        user = User.objects.get(id=user_id)
    except:
        user = AnonymousUser()
    return user


class TokenAuthMiddleware:
    """
    JWT Token authentication middleware for websockets
    """

    def __init__(self, app):
        self.app = app

    @database_sync_to_async
    def authenticate(self, token) -> dict:
        try:
            decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except:
            print(f'[MIDDLEWARE] Invalid token!')
            decoded_payload = {}
        return decoded_payload

    async def __call__(self, scope, receive, send):
        query_str = scope['query_string']
        query_params = query_str.decode()
        query_dict = parse_qs(query_params)
        try:
            token = query_dict['token'][0]
        except:
            token = None

        print(f'[MIDDLEWARE] Token : {token}')

        decoded_payload = await self.authenticate(token=token)
        user = await returnUser(decoded_payload.get('user_id'))

        scope['user'] = user
        return await self.app(scope, receive, send)
