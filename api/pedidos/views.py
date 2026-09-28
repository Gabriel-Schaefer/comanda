from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PedidoEntradaSerializer, PedidoSerializer
from .services import criar_pedido, pedidos_com_itens


class PedidoCriarView(APIView):
    def post(self, request):
        entrada = PedidoEntradaSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        pedido = criar_pedido(**entrada.validated_data)
        pedido = pedidos_com_itens().get(pk=pedido.pk)
        return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)


class PedidoDetalheView(generics.RetrieveAPIView):
    serializer_class = PedidoSerializer

    def get_queryset(self):
        return pedidos_com_itens()
