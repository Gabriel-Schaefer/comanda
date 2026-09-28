from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Pedido
from .serializers import PedidoEntradaSerializer, PedidoSerializer, StatusEntradaSerializer
from .services import STATUS_ATIVOS, TransicaoInvalida, avancar_status, criar_pedido, pedidos_com_itens


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


class PedidosAtivosView(generics.ListAPIView):
    serializer_class = PedidoSerializer
    pagination_class = None

    def get_queryset(self):
        return pedidos_com_itens().filter(status__in=STATUS_ATIVOS)


class PedidoStatusView(APIView):
    def patch(self, request, pk):
        entrada = StatusEntradaSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        try:
            avancar_status(pk, entrada.validated_data["status"])
        except Pedido.DoesNotExist:
            raise NotFound("Pedido não encontrado.")
        except TransicaoInvalida as erro:
            return Response({"detail": str(erro)}, status=status.HTTP_409_CONFLICT)
        pedido = pedidos_com_itens().get(pk=pk)
        return Response(PedidoSerializer(pedido).data)
