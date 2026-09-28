from django.contrib import admin

from .models import Adicional, Categoria, Produto


class AdicionalInline(admin.TabularInline):
    model = Adicional
    extra = 1


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["nome", "ordem"]
    list_editable = ["ordem"]


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ["nome", "categoria", "preco", "ativo"]
    list_filter = ["categoria", "ativo"]
    list_editable = ["preco", "ativo"]
    search_fields = ["nome"]
    inlines = [AdicionalInline]
