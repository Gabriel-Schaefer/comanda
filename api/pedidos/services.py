from decimal import Decimal

from django.db import transaction

from .models import ItemPedido, ItemPedidoAdicional, Pedido


def pedidos_com_itens():
    return Pedido.objects.prefetch_related("itens__adicionais")


@transaction.atomic
def criar_pedido(mesa: int, itens: list[dict]) -> Pedido:
    pedido = Pedido.objects.create(mesa=mesa)
    total = Decimal("0")

    for dados in itens:
        produto = dados["produto"]
        item = ItemPedido.objects.create(
            pedido=pedido,
            produto=produto,
            nome_produto=produto.nome,
            preco_unitario=produto.preco,
            quantidade=dados["quantidade"],
            observacao=dados["observacao"],
        )
        preco_adicionais = Decimal("0")
        for adicional in dados["adicionais"]:
            ItemPedidoAdicional.objects.create(
                item=item, adicional=adicional, nome=adicional.nome, preco=adicional.preco
            )
            preco_adicionais += adicional.preco
        total += (produto.preco + preco_adicionais) * dados["quantidade"]

    pedido.total = total
    pedido.save(update_fields=["total"])
    return pedido
