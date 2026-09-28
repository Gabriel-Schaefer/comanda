from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def saude(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/saude/", saude),
    path("api/", include("cardapio.urls")),
]
