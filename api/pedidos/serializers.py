from decimal import Decimal

from rest_framework import serializers

from cardapio.models import Produto

from .models import ItemPedido, ItemPedidoAdicional, Pedido


class ItemPedidoAdicionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedidoAdicional
        fields = ["nome", "preco"]


class ItemPedidoSerializer(serializers.ModelSerializer):
    adicionais = ItemPedidoAdicionalSerializer(many=True, read_only=True)

    class Meta:
        model = ItemPedido
        fields = ["id", "nome_produto", "preco_unitario", "quantidade", "observacao", "adicionais"]


class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ["id", "mesa", "status", "total", "criado_em", "atualizado_em", "itens"]


class ItemEntradaSerializer(serializers.Serializer):
    produto_id = serializers.IntegerField()
    quantidade = serializers.IntegerField(min_value=1, max_value=20)
    adicionais = serializers.ListField(child=serializers.IntegerField(), required=False, default=list)
    observacao = serializers.CharField(max_length=200, required=False, allow_blank=True, default="")

    def validate(self, dados):
        try:
            produto = Produto.objects.get(pk=dados["produto_id"], ativo=True)
        except Produto.DoesNotExist:
            raise serializers.ValidationError({"produto_id": "Produto inexistente ou indisponível."})

        ids = dados["adicionais"]
        if len(ids) != len(set(ids)):
            raise serializers.ValidationError({"adicionais": "Adicional repetido."})
        adicionais = list(produto.adicionais.filter(pk__in=ids))
        if len(adicionais) != len(ids):
            raise serializers.ValidationError({"adicionais": "Adicional não pertence a este produto."})

        return {
            "produto": produto,
            "quantidade": dados["quantidade"],
            "adicionais": adicionais,
            "observacao": dados["observacao"].strip(),
        }


TOTAL_MAXIMO = Decimal("99999999.99")  # limite de Pedido.total (max_digits=10)


class PedidoEntradaSerializer(serializers.Serializer):
    mesa = serializers.IntegerField(min_value=1, max_value=999)
    itens = ItemEntradaSerializer(many=True, allow_empty=False, max_length=50)

    def validate(self, dados):
        total = sum(
            (item["produto"].preco + sum(a.preco for a in item["adicionais"])) * item["quantidade"]
            for item in dados["itens"]
        )
        if total > TOTAL_MAXIMO:
            raise serializers.ValidationError("O valor do pedido ultrapassa o limite permitido.")
        return dados


class StatusEntradaSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Pedido.Status.choices)
