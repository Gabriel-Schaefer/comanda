from django.db.models import Prefetch
from rest_framework import generics

from .models import Categoria, Produto
from .serializers import CategoriaSerializer


class CardapioView(generics.ListAPIView):
    serializer_class = CategoriaSerializer
    pagination_class = None

    def get_queryset(self):
        produtos_ativos = Produto.objects.filter(ativo=True).prefetch_related("adicionais")
        return (
            Categoria.objects.filter(produtos__ativo=True)
            .distinct()
            .prefetch_related(Prefetch("produtos", queryset=produtos_ativos))
        )
