from django.urls import path

from . import consumers


ws_urlpatterns = [
    path('ws/transaction/', consumers.Consumer.as_asgi()),
]