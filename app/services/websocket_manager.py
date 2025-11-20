from typing import Dict, List, Set
import asyncio
import socketio

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[str]] = {}
        self.sio = None
    
    def set_socketio(self, sio: socketio.AsyncServer):
        self.sio = sio
    
    async def broadcast_crypto_update(self, symbol: str, data: Dict):
        """Broadcast update to all clients subscribed to a symbol"""
        if not self.sio:
            return
        
        for sid, symbols in self.active_connections.items():
            if symbol in symbols:
                await self.sio.emit("crypto_update", {
                    "symbol": symbol,
                    "data": data
                }, room=sid)