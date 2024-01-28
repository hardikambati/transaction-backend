from django.urls import path

# custom
from . import views


urlpatterns = [
    path('transaction/', views.TransactionAPIView.as_view()),
]
