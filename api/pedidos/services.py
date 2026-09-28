from decimal import Decimal

from django.db import transaction

from .models import ItemPedido, ItemPedidoAdicional, Pedido
from .notificacoes import notificar_pedido


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
    transaction.on_commit(lambda: notificar_pedido(pedido.id, "pedido_criado"))
    return pedido


PROXIMO_STATUS = {
    Pedido.Status.NOVO: Pedido.Status.EM_PREPARO,
    Pedido.Status.EM_PREPARO: Pedido.Status.PRONTO,
    Pedido.Status.PRONTO: Pedido.Status.ENTREGUE,
}

STATUS_ATIVOS = [Pedido.Status.NOVO, Pedido.Status.EM_PREPARO, Pedido.Status.PRONTO]


class TransicaoInvalida(Exception):
    pass


@transaction.atomic
def avancar_status(pedido_id: int, novo_status: str) -> Pedido:
    pedido = Pedido.objects.select_for_update().get(pk=pedido_id)
    if PROXIMO_STATUS.get(pedido.status) != novo_status:
        raise TransicaoInvalida(
            f"Não é possível mudar o pedido {pedido.id} de {pedido.status} para {novo_status}."
        )
    pedido.status = novo_status
    pedido.save(update_fields=["status", "atualizado_em"])
    transaction.on_commit(lambda: notificar_pedido(pedido.id, "pedido_atualizado"))
    return pedido
