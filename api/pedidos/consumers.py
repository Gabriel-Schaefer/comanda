from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .notificacoes import GRUPO_COZINHA, grupo_do_pedido


class CozinhaConsumer(AsyncJsonWebsocketConsumer):
    """Somente envia avisos; mensagens recebidas do navegador são ignoradas."""

    def nome_do_grupo(self) -> str:
        return GRUPO_COZINHA

    async def connect(self):
        self.grupo = self.nome_do_grupo()
        await self.channel_layer.group_add(self.grupo, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.grupo, self.channel_name)

    async def receive_json(self, content, **kwargs):
        pass

    async def pedido_evento(self, evento):
        await self.send_json({"tipo": evento["tipo"], "pedido": evento["pedido"]})


class PedidoConsumer(CozinhaConsumer):
    def nome_do_grupo(self) -> str:
        return grupo_do_pedido(self.scope["url_route"]["kwargs"]["pedido_id"])
