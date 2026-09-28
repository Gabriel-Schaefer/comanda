from django.urls import path

from .views import PedidoCriarView, PedidoDetalheView

urlpatterns = [
    path("pedidos/", PedidoCriarView.as_view()),
    path("pedidos/<int:pk>/", PedidoDetalheView.as_view()),
]
