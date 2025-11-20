import socketio
from fastapi import APIRouter, Depends
from typing import Dict, List, Set
import asyncio
from app.services.websocket_manager import WebSocketManager
from app.dependencies import get_websocket_manager
from app.models.schemas import WSSubscribe, WSUnsubscribe

router = APIRouter(tags=["WebSocket"])

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True
)

# Wrap with ASGI application
socket_app = socketio.ASGIApp(sio)

# Store active connections and subscriptions
active_connections: Dict[str, Set[str]] = {}  # sid -> set of symbols

@sio.event
async def connect(sid, environ, auth):
    """Handle client connection"""
    print(f"Client connected: {sid}")
    active_connections[sid] = set()
    await sio.emit("connected", {"message": "Connected to crypto stream"}, room=sid)

@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    print(f"Client disconnected: {sid}")
    if sid in active_connections:
        del active_connections[sid]

@sio.event
async def subscribe(sid, data: Dict):
    """Subscribe to crypto symbols"""
    try:
        symbols = data.get("symbols", [])
        if not symbols:
            await sio.emit("error", {"message": "No symbols provided"}, room=sid)
            return
        
        if sid not in active_connections:
            active_connections[sid] = set()
        
        active_connections[sid].update(symbols)
        await sio.emit("subscribed", {"symbols": list(active_connections[sid])}, room=sid)
        print(f"Client {sid} subscribed to: {symbols}")
    except Exception as e:
        await sio.emit("error", {"message": str(e)}, room=sid)

@sio.event
async def unsubscribe(sid, data: Dict):
    """Unsubscribe from crypto symbols"""
    try:
        symbols = data.get("symbols", [])
        if sid in active_connections:
            active_connections[sid].difference_update(symbols)
            await sio.emit("unsubscribed", {"symbols": list(active_connections[sid])}, room=sid)
            print(f"Client {sid} unsubscribed from: {symbols}")
    except Exception as e:
        await sio.emit("error", {"message": str(e)}, room=sid)

async def broadcast_updates():
    """Background task to broadcast real-time updates"""
    from app.dependencies import get_crypto_repository
    
    while True:
        try:
            # Get all subscribed symbols across all clients
            all_symbols = set()
            for symbols in active_connections.values():
                all_symbols.update(symbols)
            
            if all_symbols:
                # Fetch data for all subscribed symbols
                repo = get_crypto_repository()
                data = await repo.get_real_time_update(list(all_symbols))
                
                # Broadcast to all clients with their subscribed symbols
                for sid, symbols in active_connections.items():
                    if symbols:
                        client_data = {
                            "type": "update",
                            "data": {symbol: data.get("data", {}).get(symbol) for symbol in symbols}
                        }
                        await sio.emit("crypto_update", client_data, room=sid)
            
            await asyncio.sleep(30)  # Configurable poll interval
        except Exception as e:
            print(f"Error in broadcast task: {e}")
            await asyncio.sleep(30)

# Start broadcast task on startup
@sio.event
async def startup():
    asyncio.create_task(broadcast_updates())