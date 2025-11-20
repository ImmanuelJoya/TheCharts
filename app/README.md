## File structure 

crypto-monitor-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Configuration management
│   ├── dependencies.py         # Dependency injection
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── market.py           # Market data endpoints
│   │   ├── exchange.py         # Exchange data endpoints
│   │   ├── conversion.py       # Conversion endpoints
│   │   ├── historical.py       # Historical data endpoints
│   │   └── websocket.py        # WebSocket/Socket.IO endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── freecrypto_api.py   # API client service
│   │   └── websocket_manager.py # WebSocket connection manager
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── crypto_repository.py # Business logic layer
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic models
│   └── utils/
│       ├── __init__.py
│       └── cache.py            # Simple caching utility
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Test configuration
│   └── test_smoke.py           # Smoke tests
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md