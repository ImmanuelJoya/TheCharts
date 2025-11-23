from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.config import get_settings
from app.routers import market, exchange, conversion, historical, websocket

def create_app() -> FastAPI:
    settings = get_settings()
    
    app = FastAPI(
        title="Crypto Real-Time Monitoring Platform",
        description="FastAPI backend for FreeCryptoAPI with WebSocket support",
        version="1.0.0"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers with /api prefix
    app.include_router(market.router, prefix="/api")
    app.include_router(exchange.router, prefix="/api")
    app.include_router(conversion.router, prefix="/api")
    app.include_router(historical.router, prefix="/api")
    
    # WebSocket - Mount for socket.io compatibility
    app.mount("/socket.io", websocket.socket_app)
    
    @app.get("/")
    async def root():
        return {
            "message": "Crypto Real-Time Monitoring Platform API",
            "docs": "/docs",
            "websocket": "ws://localhost:8000/ws"
        }
    
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
    
    return app

app = create_app()

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_env == "development"
    )