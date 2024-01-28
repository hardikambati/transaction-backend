from django.urls import path

from . import views


urlpatterns = [
    path('update-transaction/', views.TransactionStatusAPIView.as_view()),
]