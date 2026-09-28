from rest_framework import serializers

from .models import Adicional, Categoria, Produto


class AdicionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adicional
        fields = ["id", "nome", "preco"]


class ProdutoSerializer(serializers.ModelSerializer):
    adicionais = AdicionalSerializer(many=True, read_only=True)

    class Meta:
        model = Produto
        fields = ["id", "nome", "descricao", "preco", "imagem_url", "adicionais"]


class CategoriaSerializer(serializers.ModelSerializer):
    produtos = ProdutoSerializer(many=True, read_only=True)

    class Meta:
        model = Categoria
        fields = ["id", "nome", "produtos"]
