from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from cardapio.models import Adicional, Categoria, Produto

CARDAPIO = [
    ("Lanches", [
        ("X-Burger", "Pão brioche, blend 150 g, queijo e molho da casa.", "28.90",
         [("Bacon", "5.00"), ("Queijo extra", "4.00"), ("Ovo", "3.00")]),
        ("X-Salada", "Blend 150 g, queijo, alface, tomate e maionese.", "30.90",
         [("Bacon", "5.00")]),
        ("Smash Duplo", "Dois smash de 90 g, cheddar e cebola caramelizada.", "36.90",
         [("Bacon", "5.00"), ("Cheddar extra", "4.00")]),
    ]),
    ("Porções", [
        ("Batata Frita", "Porção de 400 g.", "24.90", [("Cheddar e bacon", "8.00")]),
        ("Anéis de Cebola", "Porção de 300 g com molho barbecue.", "22.90", []),
    ]),
    ("Bebidas", [
        ("Refrigerante Lata", "350 ml.", "6.50", []),
        ("Suco Natural", "500 ml. Laranja, limão ou abacaxi.", "9.90", []),
        ("Água Mineral", "500 ml.", "4.00", []),
    ]),
    ("Sobremesas", [
        ("Brownie", "Brownie de chocolate meio amargo.", "14.90", [("Bola de sorvete", "6.00")]),
    ]),
]


class Command(BaseCommand):
    help = "Cria um cardápio de exemplo (não faz nada se já existirem categorias)."

    @transaction.atomic
    def handle(self, *args, **options):
        if Categoria.objects.exists():
            self.stdout.write("Cardápio já existe; nada foi alterado.")
            return

        for ordem, (nome_categoria, produtos) in enumerate(CARDAPIO, start=1):
            categoria = Categoria.objects.create(nome=nome_categoria, ordem=ordem)
            for nome, descricao, preco, adicionais in produtos:
                produto = Produto.objects.create(
                    categoria=categoria, nome=nome, descricao=descricao, preco=Decimal(preco)
                )
                for nome_adicional, preco_adicional in adicionais:
                    Adicional.objects.create(
                        produto=produto, nome=nome_adicional, preco=Decimal(preco_adicional)
                    )

        self.stdout.write(self.style.SUCCESS("Cardápio de exemplo criado."))
