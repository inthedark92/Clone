from typing import List, Dict, Any
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # character_id -> WebSocket
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, character_id: int):
        await websocket.accept()
        self.active_connections[character_id] = websocket

    def disconnect(self, character_id: int):
        if character_id in self.active_connections:
            del self.active_connections[character_id]

    async def send_personal_message(self, message: Any, character_id: int):
        if character_id in self.active_connections:
            await self.active_connections[character_id].send_json(message)

    async def broadcast(self, message: Any):
        for connection in self.active_connections.values():
            await connection.send_json(message)

manager = ConnectionManager()
