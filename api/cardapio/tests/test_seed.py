from django.core.management import call_command

from cardapio.models import Adicional, Categoria, Produto


def test_seed_cria_cardapio_e_nao_duplica(db):
    call_command("seed_cardapio")

    total_produtos = Produto.objects.count()
    assert Categoria.objects.count() == 4
    assert total_produtos == 9
    assert Adicional.objects.filter(produto__nome="X-Burger").count() == 3

    call_command("seed_cardapio")

    assert Produto.objects.count() == total_produtos
