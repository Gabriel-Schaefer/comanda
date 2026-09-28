from decimal import Decimal

import pytest

from pedidos.models import Pedido


def payload(cardapio):
    return {
        "mesa": 5,
        "itens": [
            {
                "produto_id": cardapio.burger.id,
                "quantidade": 2,
                "adicionais": [cardapio.bacon.id, cardapio.queijo.id],
                "observacao": "sem cebola",
            },
            {"produto_id": cardapio.refri.id, "quantidade": 1},
        ],
    }


def criar(api_client, dados):
    return api_client.post("/api/pedidos/", dados, format="json")


def test_cria_pedido_e_calcula_total_no_servidor(api_client, cardapio):
    dados = payload(cardapio)
    dados["total"] = 1
    dados["itens"][0]["preco"] = 0.01

    resposta = criar(api_client, dados)

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["mesa"] == 5
    assert corpo["status"] == "NOVO"
    assert corpo["total"] == 67.0  # 2 x (20 + 5 + 3,50) + 1 x 10
    burger = corpo["itens"][0]
    assert burger["nome_produto"] == "X-Burger"
    assert burger["preco_unitario"] == 20.0
    assert burger["quantidade"] == 2
    assert burger["observacao"] == "sem cebola"
    assert sorted(a["nome"] for a in burger["adicionais"]) == ["Bacon", "Queijo extra"]
    assert corpo["itens"][1]["adicionais"] == []


def test_pedido_guarda_copia_do_preco(api_client, cardapio):
    pedido_id = criar(api_client, payload(cardapio)).json()["id"]
    cardapio.burger.preco = Decimal("99.00")
    cardapio.burger.save()

    detalhe = api_client.get(f"/api/pedidos/{pedido_id}/").json()

    assert detalhe["itens"][0]["preco_unitario"] == 20.0
    assert detalhe["total"] == 67.0


def test_detalhe_de_pedido_inexistente_retorna_404(api_client, db):
    assert api_client.get("/api/pedidos/999999/").status_code == 404


CASOS_INVALIDOS = {
    "sem_itens": lambda d, c: d.update(itens=[]),
    "mesa_zero": lambda d, c: d.update(mesa=0),
    "mesa_1000": lambda d, c: d.update(mesa=1000),
    "mesa_texto": lambda d, c: d.update(mesa="abc"),
    "quantidade_zero": lambda d, c: d["itens"][0].update(quantidade=0),
    "quantidade_21": lambda d, c: d["itens"][0].update(quantidade=21),
    "produto_inexistente": lambda d, c: d["itens"][0].update(produto_id=999999),
    "produto_inativo": lambda d, c: d["itens"][1].update(produto_id=c.inativo.id),
    "adicional_de_outro_produto": lambda d, c: d["itens"][1].update(adicionais=[c.bacon.id]),
    "adicional_repetido": lambda d, c: d["itens"][0].update(adicionais=[c.bacon.id, c.bacon.id]),
    "observacao_longa": lambda d, c: d["itens"][0].update(observacao="x" * 201),
    "mais_de_50_itens": lambda d, c: d.update(
        itens=[{"produto_id": c.refri.id, "quantidade": 1} for _ in range(51)]
    ),
}


@pytest.mark.parametrize("caso", CASOS_INVALIDOS)
def test_pedido_invalido_retorna_400_e_nao_grava(api_client, cardapio, caso):
    dados = payload(cardapio)
    CASOS_INVALIDOS[caso](dados, cardapio)

    resposta = criar(api_client, dados)

    assert resposta.status_code == 400
    assert Pedido.objects.count() == 0


def test_total_acima_do_limite_retorna_400_e_nao_grava(api_client, cardapio):
    cardapio.refri.preco = Decimal("999999.99")
    cardapio.refri.save()
    dados = {"mesa": 1, "itens": [{"produto_id": cardapio.refri.id, "quantidade": 20}] * 6}

    resposta = criar(api_client, dados)

    assert resposta.status_code == 400
    assert Pedido.objects.count() == 0
