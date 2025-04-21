import asyncio
import json
from urllib.parse import parse_qs

from channels.generic.websocket import AsyncWebsocketConsumer


class GenericConsumer(AsyncWebsocketConsumer):
    session_key: str

    async def connect(self):
        query = self.scope.get("query_string", b"").decode("utf-8")
        self.session_key = parse_qs(query).get("session_key", [None])[0]
        await self.accept()

    async def send_and_flush(self, message: str, error=False):
        await self.send(text_data=json.dumps({
            'message': f"{message}",
            **({"error": True} if error else {})
        }))
        await asyncio.sleep(0.1)
