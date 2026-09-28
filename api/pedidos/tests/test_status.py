import pytest

from pedidos.models import Pedido
from pedidos.services import criar_pedido


def novo_pedido(cardapio, mesa=3):
    return criar_pedido(
        mesa=mesa,
        itens=[{"produto": cardapio.refri, "quantidade": 1, "adicionais": [], "observacao": ""}],
    )


def mudar(api_client, pedido_id, status):
    return api_client.patch(f"/api/pedidos/{pedido_id}/status/", {"status": status}, format="json")


def test_avanca_pela_sequencia_completa(api_client, cardapio):
    pedido = novo_pedido(cardapio)

    for status in ["EM_PREPARO", "PRONTO", "ENTREGUE"]:
        resposta = mudar(api_client, pedido.id, status)
        assert resposta.status_code == 200
        assert resposta.json()["status"] == status


@pytest.mark.parametrize(
    "atual,destino",
    [
        ("NOVO", "PRONTO"),
        ("NOVO", "ENTREGUE"),
        ("NOVO", "NOVO"),
        ("EM_PREPARO", "NOVO"),
        ("PRONTO", "EM_PREPARO"),
        ("ENTREGUE", "NOVO"),
    ],
)
def test_transicao_fora_da_ordem_retorna_409(api_client, cardapio, atual, destino):
    pedido = novo_pedido(cardapio)
    Pedido.objects.filter(pk=pedido.pk).update(status=atual)

    resposta = mudar(api_client, pedido.id, destino)

    assert resposta.status_code == 409
    assert "detail" in resposta.json()
    pedido.refresh_from_db()
    assert pedido.status == atual


def test_segundo_clique_igual_retorna_409(api_client, cardapio):
    pedido = novo_pedido(cardapio)

    assert mudar(api_client, pedido.id, "EM_PREPARO").status_code == 200
    assert mudar(api_client, pedido.id, "EM_PREPARO").status_code == 409


def test_status_desconhecido_retorna_400(api_client, cardapio):
    pedido = novo_pedido(cardapio)

    assert mudar(api_client, pedido.id, "VOANDO").status_code == 400


def test_mudar_status_de_pedido_inexistente_retorna_404(api_client, db):
    assert mudar(api_client, 999999, "EM_PREPARO").status_code == 404


def test_ativos_exclui_entregues_e_ordena_do_mais_antigo(api_client, cardapio):
    primeiro = novo_pedido(cardapio, mesa=1)
    entregue = novo_pedido(cardapio, mesa=2)
    pronto = novo_pedido(cardapio, mesa=3)
    Pedido.objects.filter(pk=entregue.pk).update(status="ENTREGUE")
    Pedido.objects.filter(pk=pronto.pk).update(status="PRONTO")

    resposta = api_client.get("/api/pedidos/ativos/")

    assert resposta.status_code == 200
    assert [p["id"] for p in resposta.json()] == [primeiro.id, pronto.id]
    assert resposta.json()[0]["itens"][0]["nome_produto"] == "Refrigerante"
