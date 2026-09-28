from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from cardapio.models import Adicional, Produto


class Pedido(models.Model):
    class Status(models.TextChoices):
        NOVO = "NOVO", "Novo"
        EM_PREPARO = "EM_PREPARO", "Em preparo"
        PRONTO = "PRONTO", "Pronto"
        ENTREGUE = "ENTREGUE", "Entregue"

    mesa = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(999)])
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NOVO)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["criado_em", "id"]

    def __str__(self):
        return f"Pedido {self.id} - mesa {self.mesa}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True)
    nome_produto = models.CharField(max_length=100)
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)
    quantidade = models.PositiveSmallIntegerField()
    observacao = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["id"]


class ItemPedidoAdicional(models.Model):
    item = models.ForeignKey(ItemPedido, on_delete=models.CASCADE, related_name="adicionais")
    adicional = models.ForeignKey(Adicional, on_delete=models.SET_NULL, null=True)
    nome = models.CharField(max_length=60)
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ["id"]
