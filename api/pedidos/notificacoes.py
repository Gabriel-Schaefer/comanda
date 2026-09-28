import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.renderers import JSONRenderer

from .serializers import PedidoSerializer

GRUPO_COZINHA = "cozinha"


def grupo_do_pedido(pedido_id: int) -> str:
    return f"pedido-{pedido_id}"


def notificar_pedido(pedido_id: int, tipo: str) -> None:
    from .services import pedidos_com_itens

    pedido = pedidos_com_itens().get(pk=pedido_id)
    # Passa pelo JSONRenderer para converter Decimal e datas em tipos JSON simples.
    dados = json.loads(JSONRenderer().render(PedidoSerializer(pedido).data))
    mensagem = {"type": "pedido.evento", "tipo": tipo, "pedido": dados}

    camada = get_channel_layer()
    async_to_sync(camada.group_send)(GRUPO_COZINHA, mensagem)
    if tipo == "pedido_atualizado":
        async_to_sync(camada.group_send)(grupo_do_pedido(pedido_id), mensagem)
