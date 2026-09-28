import pytest
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator

from config.asgi import application
from pedidos.services import avancar_status, criar_pedido

pytestmark = pytest.mark.django_db(transaction=True)

ORIGEM_PERMITIDA = [(b"origin", b"http://localhost:5173")]


def novo_pedido(cardapio):
    return criar_pedido(
        mesa=7,
        itens=[{"produto": cardapio.refri, "quantidade": 1, "adicionais": [], "observacao": ""}],
    )


async def conectar(caminho, headers=ORIGEM_PERMITIDA):
    comunicador = WebsocketCommunicator(application, caminho, headers=headers)
    conectado, _ = await comunicador.connect()
    return comunicador, conectado


async def test_cozinha_recebe_pedido_criado(cardapio):
    cozinha, conectado = await conectar("/ws/cozinha/")
    assert conectado

    pedido = await sync_to_async(novo_pedido)(cardapio)
    mensagem = await cozinha.receive_json_from(timeout=2)

    assert mensagem["tipo"] == "pedido_criado"
    assert mensagem["pedido"]["id"] == pedido.id
    assert mensagem["pedido"]["total"] == 10.0
    assert mensagem["pedido"]["itens"][0]["nome_produto"] == "Refrigerante"
    await cozinha.disconnect()


async def test_cliente_e_cozinha_recebem_mudanca_de_status(cardapio):
    pedido = await sync_to_async(novo_pedido)(cardapio)
    cliente, conectado_cliente = await conectar(f"/ws/pedidos/{pedido.id}/")
    cozinha, conectado_cozinha = await conectar("/ws/cozinha/")
    assert conectado_cliente and conectado_cozinha

    await sync_to_async(avancar_status)(pedido.id, "EM_PREPARO")

    for comunicador in (cliente, cozinha):
        mensagem = await comunicador.receive_json_from(timeout=2)
        assert mensagem["tipo"] == "pedido_atualizado"
        assert mensagem["pedido"]["status"] == "EM_PREPARO"
        await comunicador.disconnect()


async def test_cliente_nao_recebe_aviso_de_outro_pedido(cardapio):
    meu = await sync_to_async(novo_pedido)(cardapio)
    outro = await sync_to_async(novo_pedido)(cardapio)
    cliente, _ = await conectar(f"/ws/pedidos/{meu.id}/")

    await sync_to_async(avancar_status)(outro.id, "EM_PREPARO")

    assert await cliente.receive_nothing(timeout=0.5)
    await cliente.disconnect()


async def test_origem_nao_permitida_e_recusada():
    _, conectado = await conectar("/ws/cozinha/", headers=[(b"origin", b"http://site-malicioso.com")])

    assert not conectado
