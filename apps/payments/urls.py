from django.urls import path
from .views import PaymeWebhookView

urlpatterns = [
    path("payme/", PaymeWebhookView.as_view()),
]