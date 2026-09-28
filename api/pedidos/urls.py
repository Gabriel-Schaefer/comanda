from django.urls import path

from .views import PedidoCriarView, PedidoDetalheView, PedidosAtivosView, PedidoStatusView

urlpatterns = [
    path("pedidos/", PedidoCriarView.as_view()),
    path("pedidos/ativos/", PedidosAtivosView.as_view()),
    path("pedidos/<int:pk>/", PedidoDetalheView.as_view()),
    path("pedidos/<int:pk>/status/", PedidoStatusView.as_view()),
]
