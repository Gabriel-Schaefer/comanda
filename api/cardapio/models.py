from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

PRECO_MINIMO = [MinValueValidator(Decimal("0"))]


class Categoria(models.Model):
    nome = models.CharField(max_length=60)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordem", "nome"]

    def __str__(self):
        return self.nome


class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="produtos")
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2, validators=PRECO_MINIMO)
    imagem_url = models.URLField(blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Adicional(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="adicionais")
    nome = models.CharField(max_length=60)
    preco = models.DecimalField(max_digits=8, decimal_places=2, validators=PRECO_MINIMO)

    class Meta:
        ordering = ["nome"]
        verbose_name_plural = "adicionais"

    def __str__(self):
        return f"{self.nome} ({self.produto.nome})"
