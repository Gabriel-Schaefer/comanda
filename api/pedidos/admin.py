from django.contrib import admin

from .models import ItemPedido, Pedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    fields = ["nome_produto", "preco_unitario", "quantidade", "observacao"]
    readonly_fields = fields


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ["id", "mesa", "status", "total", "criado_em"]
    list_filter = ["status"]
    inlines = [ItemPedidoInline]
