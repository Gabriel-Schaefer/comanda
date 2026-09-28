from decimal import Decimal
from types import SimpleNamespace

import pytest
from rest_framework.test import APIClient

from cardapio.models import Adicional, Categoria, Produto


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def cardapio(db):
    lanches = Categoria.objects.create(nome="Lanches", ordem=1)
    bebidas = Categoria.objects.create(nome="Bebidas", ordem=2)
    vazia = Categoria.objects.create(nome="Vazia", ordem=3)
    burger = Produto.objects.create(categoria=lanches, nome="X-Burger", preco=Decimal("20.00"))
    bacon = Adicional.objects.create(produto=burger, nome="Bacon", preco=Decimal("5.00"))
    queijo = Adicional.objects.create(produto=burger, nome="Queijo extra", preco=Decimal("3.50"))
    refri = Produto.objects.create(categoria=bebidas, nome="Refrigerante", preco=Decimal("10.00"))
    inativo = Produto.objects.create(
        categoria=vazia, nome="Fora de linha", preco=Decimal("1.00"), ativo=False
    )
    return SimpleNamespace(
        lanches=lanches,
        bebidas=bebidas,
        vazia=vazia,
        burger=burger,
        bacon=bacon,
        queijo=queijo,
        refri=refri,
        inativo=inativo,
    )
