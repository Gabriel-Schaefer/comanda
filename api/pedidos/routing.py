from django.urls import path

from .consumers import CozinhaConsumer, PedidoConsumer

websocket_urlpatterns = [
    path("ws/cozinha/", CozinhaConsumer.as_asgi()),
    path("ws/pedidos/<int:pedido_id>/", PedidoConsumer.as_asgi()),
]
