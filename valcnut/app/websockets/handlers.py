from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from .connection_manager import manager
from ..core.database import get_db
from sqlalchemy.orm import Session
import json

router = APIRouter()

@router.websocket("/ws/{character_id}")
async def websocket_endpoint(websocket: WebSocket, character_id: int):
    await manager.connect(websocket, character_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            # Simple Chat logic
            if message.get("type") == "chat":
                payload = {
                    "type": "chat",
                    "from_id": character_id,
                    "text": message.get("text"),
                    "scope": message.get("scope", "global")
                }
                await manager.broadcast(payload)

            # Battle turn notification logic
            elif message.get("type") == "turn_ready":
                # In a real system, we would notify the other player
                pass

    except WebSocketDisconnect:
        manager.disconnect(character_id)
        await manager.broadcast({"type": "info", "text": f"Character {character_id} left."})
