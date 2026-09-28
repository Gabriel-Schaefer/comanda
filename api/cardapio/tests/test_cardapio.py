def test_cardapio_lista_categorias_com_produtos_ativos_e_adicionais(api_client, cardapio):
    resposta = api_client.get("/api/cardapio/")

    assert resposta.status_code == 200
    dados = resposta.json()
    assert [c["nome"] for c in dados] == ["Lanches", "Bebidas"]
    assert dados[0]["produtos"] == [
        {
            "id": cardapio.burger.id,
            "nome": "X-Burger",
            "descricao": "",
            "preco": 20.0,
            "imagem_url": "",
            "adicionais": [
                {"id": cardapio.bacon.id, "nome": "Bacon", "preco": 5.0},
                {"id": cardapio.queijo.id, "nome": "Queijo extra", "preco": 3.5},
            ],
        }
    ]


def test_produto_inativo_nao_aparece(api_client, cardapio):
    cardapio.refri.ativo = False
    cardapio.refri.save()

    dados = api_client.get("/api/cardapio/").json()

    assert [c["nome"] for c in dados] == ["Lanches"]
