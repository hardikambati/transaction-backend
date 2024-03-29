"""
ASGI config for main project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.urls import path
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter, ProtocolTypeRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

django_asgi_app = get_asgi_application()


from websockets import routing
from accounts.middleware.AuthMiddleware import TokenAuthMiddleware


application = ProtocolTypeRouter({
    'http': django_asgi_app,
    # 'websocket': AuthMiddlewareStack(URLRouter(routing.ws_urlpatterns)),
    'websocket': TokenAuthMiddleware(
        AllowedHostsOriginValidator(
            URLRouter(
                (routing.ws_urlpatterns)
            )
        )
    )
})