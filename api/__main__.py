from uvicorn import run
from src.logging_config import setup_logging


if __name__ == "__main__":
    setup_logging()
    run(
        app="api.app:get_application",
        host="0.0.0.0",
        port=8000,
        http="httptools",
        loop="uvloop",
        interface="asgi3",
        factory=True,
        reload=True,
    )
