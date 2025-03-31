from urllib.parse import parse_qs

from channels.generic.websocket import AsyncWebsocketConsumer


class GenericConsumer(AsyncWebsocketConsumer):
    session_key: str

    async def connect(self):
        query_string = self.scope.get("query_string", b"").decode("utf-8")
        query_params = parse_qs(query_string)
        self.session_key = query_params.get("session_key", [None])[0]
        await self.accept()

    async def disconnect(self, close_code):
        pass
