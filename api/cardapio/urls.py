from django.urls import path

from .views import CardapioView

urlpatterns = [
    path("cardapio/", CardapioView.as_view()),
]
